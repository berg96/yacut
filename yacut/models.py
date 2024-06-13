import re
from datetime import datetime
from random import choices

from flask import url_for

from . import db
from settings import (
    ORIGINAL_LINK_MAX_LENGTH, SHORT_CHARACTERS, SHORT_LENGTH, SHORT_MAX_LENGTH,
    SHORT_PATTERN
)

SHORT_INVALID = 'Указано недопустимое имя для короткой ссылки'
SHORT_SAME_ERROR_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
ORIGINAL_LINK_INVALID = 'Указана недопустимая url'
REDIRECT_FUNC_NAME = 'redirect_to_original_url'
SHORT_UNIQUE_NOT_FOUND = 'Не нашлось свободной уникальной короткой ссылки'


class URLMap(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String(ORIGINAL_LINK_MAX_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(SHORT_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_FUNC_NAME, _external=True, short=self.short
            )
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        for _ in range(len(SHORT_CHARACTERS)**SHORT_LENGTH):
            random_string = ''.join(choices(SHORT_CHARACTERS, k=SHORT_LENGTH))
            if not URLMap.get(random_string):
                return random_string
        raise RuntimeError(SHORT_UNIQUE_NOT_FOUND)

    @staticmethod
    def create(original, short, flag: bool):
        if short:
            if not flag:
                if (
                    len(short) > SHORT_MAX_LENGTH
                    or not re.match(SHORT_PATTERN, short)
                ):
                    raise ValueError(SHORT_INVALID)
                if URLMap.get(short):
                    raise ValueError(SHORT_SAME_ERROR_MESSAGE)
                if len(original) > ORIGINAL_LINK_MAX_LENGTH:
                    raise ValueError(ORIGINAL_LINK_INVALID)
        else:
            short = URLMap.get_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_original_link_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original
