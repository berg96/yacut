from flask_wtf import FlaskForm
from wtforms.fields.simple import URLField, SubmitField, StringField
from wtforms.validators import Length, Optional, DataRequired, URL


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
