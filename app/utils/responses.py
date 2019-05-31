from flask import render_template, make_response, jsonify

render = render_template  # shortcut for render_template


def response(body, status=200, headers=None):
    """
    Returns a flask json response :class: flask.wrappers.Response
    params:
    body: server response,
    status(int): http status code
    headers: custom headers for the response
    """
    return make_response(body, status, headers)


def json_response(body, status=200, headers=None):
    """
    Returns a flask json response :class: flask.wrappers.Response
    params:
    body: server response,
    status(int): http status code
    headers: custom headers for the response
    """
    return make_response(jsonify(body), status, headers)
