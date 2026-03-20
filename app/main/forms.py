"""WTForms fuer Projekt- und Task-Eingaben im UI."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Optional


class ProjectForm(FlaskForm):
    # Name eines Projekts, max. 140 Zeichen.
    name = StringField('Projektname', validators=[DataRequired(), Length(max=140)])
    submit = SubmitField('Speichern')


class TaskForm(FlaskForm):
    # Neue Task mit optionaler Beschreibung und optionalem Faelligkeitsdatum.
    title = StringField('Titel', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Beschreibung', validators=[Optional(), Length(max=2000)])
    due_date = DateField('Fällig am', validators=[Optional()])
    submit = SubmitField('Task hinzufügen')
