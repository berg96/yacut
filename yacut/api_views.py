import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import SAME_SHORT_ERROR_MESSAGE, get_unique_short_id

PATTERN_URL = r'^(https?://)?[\w.\-]*\.[a-z]{2,6}.*'
PATTERN_SHORT_ID = r'[a-zA-Z0-9]{1,16}$'

EMPTY_REQUEST = 'Отсутствует тело запроса'
REQUIRED_FIELD_URL = '"url" является обязательным полем!'
INVALID_URL = 'URL не является ссылкой'
INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
SHORT_ID_NOT_FOUND = 'Указанный id не найден'


def is_url(url):
    return re.match(PATTERN_URL, url)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage(SHORT_ID_NOT_FOUND, 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_id():
    try:
        data = request.get_json()
    except Exception:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(REQUIRED_FIELD_URL)
    short_id = data.get('custom_id')
    url = data.get('url')
    if URLMap.query.filter_by(short=short_id).first() is not None:
        raise InvalidAPIUsage(SAME_SHORT_ERROR_MESSAGE)
    if not is_url(url):
        raise InvalidAPIUsage(INVALID_URL)
    if short_id:
        if not re.match(PATTERN_SHORT_ID, short_id):
            raise InvalidAPIUsage(INVALID_SHORT_ID)
    else:
        short_id = get_unique_short_id()
    url = URLMap(original=url, short=short_id)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201
