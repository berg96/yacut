from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, URLField
from wtforms.validators import (
    URL, DataRequired, Length, Optional, Regexp, ValidationError
)

from .models import SHORT_INVALID, SHORT_SAME_ERROR_MESSAGE, URLMap
from settings import ORIGINAL_LINK_MAX_LENGTH, SHORT_MAX_LENGTH, SHORT_PATTERN

ORIGINAL_LINK_LABEL = 'Длинная ссылка'
ORIGINAL_LINK_VALIDATOR_REQUIRED_MESSAGE = 'Обязательное поле'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
SUBMIT_LABEL = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(
                message=ORIGINAL_LINK_VALIDATOR_REQUIRED_MESSAGE
            ),
            Length(max=ORIGINAL_LINK_MAX_LENGTH),
            URL()
        ]
    )
    custom_id = StringField(
        SHORT_LABEL,
        validators=[
            Length(max=SHORT_MAX_LENGTH),
            Optional(),
            Regexp(
                regex=SHORT_PATTERN, message=SHORT_INVALID
            )
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)

    @staticmethod
    def validate_custom_id(form, field):
        if URLMap.get(field.data):
            raise ValidationError(SHORT_SAME_ERROR_MESSAGE)
