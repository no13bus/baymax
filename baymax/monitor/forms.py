# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm 
from wtforms import ValidationError, HiddenField, StringField
from wtforms.validators import (Length, EqualTo, Email, NumberRange, 
        URL, AnyOf, Optional)
from flask_login import current_user

from ..user import User
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, AGE_MIN, AGE_MAX, DEPOSIT_MIN, DEPOSIT_MAX
from ..utils import allowed_file, ALLOWED_AVATAR_EXTENSIONS
from ..utils import SEX_TYPE


class RescuetimeForm(FlaskForm):
    key = StringField(u'key', [Length(max=64)])

