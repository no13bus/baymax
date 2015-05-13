# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from wtforms import (ValidationError, HiddenField, TextField, HiddenField,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField)
from wtforms.validators import (Required, Length, EqualTo, Email, NumberRange, 
        URL, AnyOf, Optional)
from flask.ext.login import current_user

from ..user import User
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, AGE_MIN, AGE_MAX, DEPOSIT_MIN, DEPOSIT_MAX
from ..utils import allowed_file, ALLOWED_AVATAR_EXTENSIONS
from ..utils import SEX_TYPE


class RescuetimeForm(Form):
    key = TextField(u'key', [Length(max=64)])

