# Let's import all the shit, IDK what is it
from flask_wtf import FlaskForm
from wtforms import StringField
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
# (chapter 3)

from flask import request


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
