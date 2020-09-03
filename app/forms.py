from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class DetailsForm(FlaskForm):
    description = StringField('Description', validators=[])
    headquarters = StringField('Headquarters', validators=[])
    industry = StringField('Industry', validators=[])

    submit = SubmitField('Submit')