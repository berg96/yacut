from flask import redirect, render_template, url_for

from . import app
from .constants import REDIRECT_FUNC_NAME
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = URLMap.create(form.original_link.data, form.custom_id.data).short
    short_url = f'{url_for(REDIRECT_FUNC_NAME, _external=True, short=short)}'
    return render_template('index.html', form=form, short_url=short_url)


@app.route('/<string:short>')
def redirect_to_original_url(short):
    return redirect(URLMap.get_original_link(short))
