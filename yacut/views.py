import string
from random import choice

from flask import flash, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


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
                flash(
                    'Предложенный вариант короткой ссылки уже существует.',
                    'same_short'
                )
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
            'success_url'
        )
    return render_template('index.html', form=form)
