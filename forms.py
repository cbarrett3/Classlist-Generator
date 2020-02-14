from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length
# Responsible for the input fields in the form, and input validation

# Form with inputs and a submit field (each item consisting of a label, type, and optional  validator)
#[VARIABLE] = [FIELD TYPE]('[LABEL]', [
#        validators=[VALIDATOR TYPE](message=('[ERROR MESSAGE'))
#    ])
class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    # TODO: do a better email address check
    email = StringField('Email', [
        # Email(message=('Not a valid email address.')),
        DataRequired()])
    body = TextField('Message', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


# class LoginForm(FlaskForm):
#     email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
#     excel = FileField('Excel', validators=[
#         FileRequired(),
#         FileAllowed(['xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'], 'Excel Spreadsheets only!')
#     ])