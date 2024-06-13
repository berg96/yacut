from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

SHORT_NOT_FOUND = 'Указанный id не найден'
EMPTY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    if not request.data:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    if 'url' not in (data := request.get_json()):
        raise InvalidAPIUsage(URL_REQUIRED_FIELD)
    try:
        return jsonify(
            URLMap.create(
                original=data['url'], short=data.get('custom_id'), flag=False
            ).to_dict()
        ), HTTPStatus.CREATED
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    except RuntimeError as error:
        raise InvalidAPIUsage(str(error))
