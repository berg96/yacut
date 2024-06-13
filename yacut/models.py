import re
from datetime import datetime
from random import choice

from flask import url_for

from settings import CHARACTERS_FOR_SHORT, SHORT_PATTERN
from . import db, constants
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String(constants.ORIGINAL_LINK_MAX_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(constants.SHORT_MAX_LENGTH),
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
                constants.REDIRECT_FUNC_NAME, _external=True, short=self.short
            )
        )

    @staticmethod
    def get_urlmap(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def is_short_exists(short):
        return bool(URLMap.get_urlmap(short))

    @staticmethod
    def get_unique_short():
        for _ in range(constants.MAX_TRY):
            random_string = ''.join(
                choice(CHARACTERS_FOR_SHORT)
                for _ in range(constants.SHORT_LENGTH)
            )
            if not URLMap.is_short_exists(random_string):
                return random_string

    @staticmethod
    def create(original, short):
        if short:
            if (
                not re.match(SHORT_PATTERN, short)
                or len(short) > constants.SHORT_MAX_LENGTH
            ):
                raise InvalidAPIUsage(constants.SHORT_INVALID)
        else:
            short = URLMap.get_unique_short()
        if URLMap.is_short_exists(short):
            raise InvalidAPIUsage(constants.SHORT_SAME_ERROR_MESSAGE)
        urlmap = URLMap(original=original, short=short)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def get_original_link(short):
        return URLMap.query.filter_by(short=short).first_or_404().original
