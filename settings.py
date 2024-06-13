import os
import re
import string

CHARACTERS_FOR_SHORT = string.ascii_letters + string.digits
SHORT_PATTERN = (
    f'^[{re.escape(CHARACTERS_FOR_SHORT)}]+$'
)


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
