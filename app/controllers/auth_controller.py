from flask import redirect, url_for, request, session, flash
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, login_required, logout_user
from app.utils import response, render
from app.forms.auth import LoginForm
from app.models import User


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
