import falcon

from pascua.db import pascuadb
from pascua.framework import ModelResource, PascuaError, pasqua_error_codes, pasqua_error_types
from pascua.security import digest
from pascua.resources.api.login.login_model import LoginModel
from pascua.resources.api.user.user_model import UserModel


class LoginResource(ModelResource):
    def __init__(self):
        super(LoginResource, self).__init__(
            ('\nLogin:\n'
             '   - Authentication process. It gives you a token.\n'), model=LoginModel)
        self.version = 0
        # self.description = ()

    def process(self, req, resp, data=None, errors=[]):
        login = LoginModel(data, errors=errors)
        user = pascuadb.register.find_one( { 'email': login['email'] } )
        if not user:
            errors.append(PascuaError(
                type=pasqua_error_types.WRONG_FIELD,
                field='email',
                description='User not found.',
                code=pasqua_error_codes['WRONG_PASSWORD']
            ))
            resp.status = falcon.HTTP_403
            return

        user = UserModel(user)
        password = digest(user)
        print password
        if not 'password' in user:
            errors.append(PascuaError(
                type=pasqua_error_types.WRONG_FIELD,
                field='email',
                description='Non responsable.',
                code=pasqua_error_codes['NON_RESPONSABLE']
            ))
            resp.status = falcon.HTTP_403
            return

        resp.status = falcon.HTTP_200
        return { 'auth-token' : login.encode() }
