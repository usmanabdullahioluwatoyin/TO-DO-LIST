from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SignupForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[
            DataRequired('This field is compulsory.'), 
            Length(min=2, max=100, message='Username should be minimum of 2 characters at least.')
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            DataRequired('This field is compulsory.'),
            Email('Enter a valid email address.')
        ]
    )
    password = PasswordField(
        "Create Password",
        validators=[
            DataRequired('This field is compulsory.'),
            Length(min=8, message='Password should be at least 8 characters long.')
        ]
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired('This field is compulsory.'),
            EqualTo(fieldname='password', message='Passwords do not match')
        ]
    )

class SigninForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired('This field is compulsory.'),
            Email('Enter a valid email address.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired('This field is compulsory.')
        ]
    )
   