from flask import request
from app.utils import render, response, json_response


http_error_status_codes = [400, 401, 403, 404, 405, 500, 503]


class BaseError:
    """
    Flask error handler class.

    Returns json if the request is xmlhttp else :class:Response.
    """

    def __call__(self, error):

        self.status_code = error.code
        self.message = error.description
        self.is_json = request.is_xhr

        error_handler_func = getattr(self, 'error_' + str(self.status_code),
                                     None)

        if error_handler_func:
            return error_handler_func()

        error = dict(
            code=self.status_code,
            message=self.message
        )

        if self.is_json:
            return json_response(error, self.status_code)

        return response(render('errors/http_error.html', error=error),
                        self.status_code)


def url_404():
    error = dict(
        code=404,
        message='We couldn\'t find the page you are looking for.'
    )
    return response(render('errors/http_error.html', error=error), 404)


def url_503():
    return response(render('errors/http_503.html'), 503)
