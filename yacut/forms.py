from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'), Length(1, 256), URL()
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
