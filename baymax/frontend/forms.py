# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import (ValidationError, HiddenField, BooleanField, TextField,
        PasswordField, SubmitField)
from wtforms.validators import Required, Length, EqualTo, Email

from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)


class LoginForm(FlaskForm):
    next = HiddenField()
    login = TextField(u'Username or email', [Required()])
    password = PasswordField('Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')
