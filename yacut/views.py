from flask import flash, redirect, render_template, url_for

from . import app
from .forms import URLMapForm
from .models import REDIRECT_FUNC_NAME, URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                REDIRECT_FUNC_NAME,
                _external=True,
                short=URLMap.create(
                    original=form.original_link.data,
                    short=form.custom_id.data,
                    validate=True
                ).short
            )
        )
    except RuntimeError as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_to_original_url(short):
    return redirect(URLMap.get_original_link_or_404(short))
