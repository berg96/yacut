from flask_wtf import FlaskForm
from settings import SHORT_PATTERN
from wtforms.fields.simple import StringField, SubmitField, URLField
from wtforms.validators import (
    URL, DataRequired, Length, Optional, Regexp, ValidationError
)

from . import constants
from .models import URLMap


class URLMapForm(FlaskForm):
    original_link = URLField(
        constants.ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(
                message=constants.ORIGINAL_LINK_VALIDATOR_REQUIRED_MESSAGE
            ),
            Length(max=constants.ORIGINAL_LINK_MAX_LENGTH),
            URL()
        ]
    )
    custom_id = StringField(
        constants.SHORT_LABEL,
        validators=[
            Length(max=constants.SHORT_MAX_LENGTH),
            Optional(),
            Regexp(
                regex=SHORT_PATTERN, message=constants.SHORT_INVALID
            )
        ]
    )
    submit = SubmitField(constants.SUBMIT_LABEL)

    @staticmethod
    def validate_custom_id(form, field):
        if URLMap.is_short_exists(field.data):
            raise ValidationError(constants.SHORT_SAME_ERROR_MESSAGE)
