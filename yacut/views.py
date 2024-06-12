import string
from random import choice

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap

SAME_SHORT_ERROR_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
SAME_SHORT_FLASH_CATEGORY = 'same_short'
SUCCESS_FLASH_CATEGORY = 'success_url'


def get_unique_short_id():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(choice(characters) for _ in range(6))
    if URLMap.query.filter_by(short=random_string).first():
        random_string = get_unique_short_id()
    return random_string


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_url_from_user = form.custom_id.data
        if short_url_from_user:
            if URLMap.query.filter_by(
                    short=short_url_from_user
            ).first():
                flash(SAME_SHORT_ERROR_MESSAGE, SAME_SHORT_FLASH_CATEGORY)
                return render_template('index.html', form=form)
            short_id = short_url_from_user
        else:
            short_id = get_unique_short_id()
        db.session.add(URLMap(
            original=form.original_link.data,
            short=short_id,
        ))
        db.session.commit()
        flash(
            f'{url_for("index_view", _external=True) + short_id}',
            SUCCESS_FLASH_CATEGORY
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original_url(short_id):
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original
    )
