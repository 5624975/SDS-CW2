from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from wtforms import TextAreaField, SelectField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    recovery_code = StringField('Recovery Code', validators=[DataRequired()])
    submit = SubmitField('Register')
    role = SelectField('Role', choices=[('manager', 'Project Manager'), ('member', 'Team Member')])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recovery_code = StringField('Recovery Code', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    assigned_to = SelectMultipleField('Assign To', coerce=int)
    submit = SubmitField('Create Task')
