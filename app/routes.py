from .utils import Path
from .controllers import auth_controller
from flask_login import login_required


@login_required
def index():
    return 'flask app'


url_rules = [
    Path(rule='/', endpoint='index', view_func=index),
    Path(rule='/login/', endpoint='login',
         view_func=auth_controller.login_form, methods=['GET', 'POST']),
    Path(rule='/logout', endpoint='logout', view_func=auth_controller.logout,
         methods=['POST'])
]
