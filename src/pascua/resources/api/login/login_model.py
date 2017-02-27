# NOT IMPLEMENTED!
import jwt
from datetime import datetime

from pascua.config import jwt_secret
from pascua.framework import PascuaModel, PascuaString


class LoginModel(PascuaModel):
    def __init__(self, obj=None, errors=[]):
        super(LoginModel, self).__init__(obj, errors)
        self['timestamp'] = datetime.now().strftime('%d-%m-%Y')

    @staticmethod
    def get_fields():
        return {
            'email': PascuaString(),
            'password': PascuaString()
        }

    def encode(self):
        return jwt.encode(self, jwt_secret, algorithm='HS256')
