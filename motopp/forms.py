from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class AddBikeForm(FlaskForm):
    """
    A FlaskForm subclass for the bike adding form.

    :param name: The name of the bike.
    :param make: The make of the bike.
    :param model: The model of the bike.
    :param year: The year of the bike.
    """
    name: StringField = StringField('Name', validators=[DataRequired()])
    make: TextAreaField = TextAreaField('Make', validators=[DataRequired()])
    model: TextAreaField = TextAreaField('Model', validators=[DataRequired()])
    year: IntegerField = IntegerField('Year', validators=[DataRequired()])
    submit: SubmitField = SubmitField('Submit')
