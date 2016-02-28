# NOT IMPLEMENTED!
import falcon
import jwt
import os
from db import pascuadb
from framework import *
from security import digest
from user import UserModel


class LoginModel(PascuaModel):
    def __init__(self, obj=None, errors=[]):
        super(LoginModel, self).__init__(obj, errors)
        self['timestamp'] = datetime.now().strftime('%d-%m-%Y')

    @staticmethod
    def get_fields():
        return {
            'email': PascuaString(mandatory=True),
            'password': PascuaString(mandatory=True)
        }

    def encode(self):
        return jwt.encode(self, os.environ['PASQUAJOVE_JWT_SECRET'], algorithm='HS256')


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of pasqua and state
# transitions, which map to HTTP verbs.
class LoginResource(BaseResource):
    def __init__(self):
        super(LoginResource, self).__init__(
            ('\nLogin:\n'
             '   - Authentication process. It gives you a token.\n'), model=LoginModel)
        self.version = 0
        self.description = ()

    def process(self, req, resp, data=None, errors=[]):
        login = LoginModel(data, errors=errors)
        user = pascuadb.register.find_one( { 'email': login['email'] } )
        if not user:
            errors.append(PascuaError(
                type=pascua_error_types.WRONG_FIELD,
                field='email',
                description='User not found.',
                code=pascua_error_codes['WRONG_PASSWORD']
            ))
            resp.status = falcon.HTTP_403
            return

        user = UserModel(user)
        password = digest(user)
        print password
        if not 'password' in user:
            errors.append(PascuaError(
                type=pascua_error_types.WRONG_FIELD,
                field='email',
                description='Non responsable.',
                code=pascua_error_codes['NON_RESPONSABLE']
            ))
            resp.status = falcon.HTTP_403
            return

        resp.status = falcon.HTTP_200
        return { 'auth-token' : login.encode() }
