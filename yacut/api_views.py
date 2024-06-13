from http import HTTPStatus

from flask import jsonify, request

from . import app, constants
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    urlmap = URLMap.get_urlmap(short)
    if urlmap is None:
        raise InvalidAPIUsage(constants.SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    if not request.data:
        raise InvalidAPIUsage(constants.EMPTY_REQUEST)
    if 'url' not in (data := request.get_json()):
        raise InvalidAPIUsage(constants.URL_REQUIRED_FIELD)
    short = data.get('custom_id')
    url = data.get('url')
    urlmap = URLMap.create(original=url, short=short)
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED
