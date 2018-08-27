from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class LocationForm(FlaskForm):

    location = StringField("Locatie", validators=[DataRequired()])
    submit = SubmitField("Zoeken")
