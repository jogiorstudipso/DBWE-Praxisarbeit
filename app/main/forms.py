from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Optional


class ProjectForm(FlaskForm):
    name = StringField('Projektname', validators=[DataRequired(), Length(max=140)])
    submit = SubmitField('Speichern')


class TaskForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Beschreibung', validators=[Optional(), Length(max=2000)])
    due_date = DateField('Fällig am', validators=[Optional()])
    submit = SubmitField('Task hinzufügen')