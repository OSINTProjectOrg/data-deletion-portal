# auth/forms.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    EmailField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError
)
from .models import User


class mft_LoginForm(FlaskForm):
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class mft_SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=25)],
    )
    email = EmailField(
        "E-mail",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)],
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Create Account")

    # Custom validators
    def mft_ValidateMail(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("This e-mail is already registered.")

    def mft_ValidateUsername(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken.")
