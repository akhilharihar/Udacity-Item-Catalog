from flask import redirect, url_for, request, session, flash
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, login_required, logout_user
from app.utils import response, render
from app.forms.auth import LoginForm
from app.models.user import create_oauth_user, User
from app.auth import auth_providers


def failed_login():
    return redirect(url_for('login'))


def login_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    next_page = request.args.get('next')

    if next_page and url_parse(next_page).netloc == '':
        session['next_page'] = next_page

    if request.method == 'GET':
        return response(render('auth/login.html'))

    loginform = LoginForm()

    if not loginform.validate():
        flash(loginform.errors, category='form_error')
        return failed_login()

    user = User.by_email_address(loginform.email_id.data)

    if user is None:
        flash('Could not locate your email address', 'login_info')
        return failed_login()

    if not user.check_password(loginform.password.data):
        flash('invalid password', 'login_info')
        return failed_login()

    return _login(user, loginform.remember_me.data)


def _login(user, remember_me):
    if not login_user(user, remember=remember_me):
        return failed_login()

    next = session.pop('next_page', None)

    if next:
        return redirect(next)
    else:
        return redirect(url_for('index'))


@login_required
def logout():
    logout_user()
    session.clear()

    return redirect('/')


def login_oauth(name):
    if name not in auth_providers:
        return redirect(url_for('404'))

    auth = auth_providers[name]()
    client = auth.client

    return client.authorize_redirect(auth.redirect_uri)


def authorise_oauth(name):
    if name not in auth_providers:
        return redirect(url_for('404'))

    if request.args.get('error'):
        return failed_login()

    auth = auth_providers[name]()
    client = auth.client
    token = client.authorize_access_token()

    user_id = auth.user_id
    internal_user_email = '{}@{}'.format(str(user_id), name)

    user = User.by_email_address(internal_user_email)

    if not user:
        user = create_oauth_user(user_id, name)

    if not user:
        flash('Cannot create your account. Please try again after some time.',
              'login_info')
        return failed_login()

    if user.add_or_update_token(name, token):
        return _login(user, False)
    else:
        flash('Cannot create your account. Please try again after some time.',
              'login_info')
        return failed_login()
