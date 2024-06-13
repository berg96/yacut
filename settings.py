import os
import re
import string

ORIGINAL_LINK_MAX_LENGTH = 80000
SHORT_MAX_LENGTH = 16
SHORT_LENGTH = 6
SHORT_CHARACTERS = string.ascii_letters + string.digits
SHORT_PATTERN = (
    f'^[{re.escape(SHORT_CHARACTERS)}]+$'
)


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
