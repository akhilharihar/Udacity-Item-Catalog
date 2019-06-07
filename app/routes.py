from .utils import Path, url
from .controllers import auth_controller
from flask import redirect


def index():
    return redirect(url('catalog.catalog'))


url_rules = [
     Path(rule='/', endpoint='index', view_func=index),
     Path(rule='/login', endpoint='login',
          view_func=auth_controller.login_form, methods=['GET', 'POST']),
     Path(rule='/logout', endpoint='logout', view_func=auth_controller.logout,
          methods=['POST']),
     Path(rule='/login/<name>', endpoint='login_oauth',
          view_func=auth_controller.login_oauth),
     Path(rule='/authorise/<name>', endpoint='authorise_oauth',
          view_func=auth_controller.authorise_oauth)
]
