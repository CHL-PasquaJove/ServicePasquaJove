import falcon

from pascua.db import pascuadb
from pascua.framework import ModelResource, PascuaError, pasqua_error_types, pasqua_error_codes
from pascua.resources.api.user.user_model import UserModel
from pascua.mails import send_mail


class NewUserResource(ModelResource):
    def __init__(self):
        super(NewUserResource, self).__init__(
            ('\nNew User:\n'
             '   - Insert a user into database.\n'), model=UserModel)

    def process(self, req, resp, data=None, errors=[]):
        user = UserModel(data, errors=errors)

        insert_user = user.copy()
        # check_duplied_mail = pascuadb.register.find_one({ 'email': insert_user['email'] })
        # if check_duplied_mail is not None:
        #     errors.append(PascuaError(
        #         type=pasqua_error_types.QUERY_ERROR,
        #         field='email',
        #         description='Duplicated email.',
        #         code=pasqua_error_codes['DUPLICATED_USER_EMAIL']
        #     ))
        #     resp.status = falcon.HTTP_409
        #     return

        pascuadb.register.insert_one(insert_user)
        user['_id'] = str(insert_user['_id'])

        # Send an email
        self.send_registration_mail(user)

        resp.status = falcon.HTTP_201
        return user

    @staticmethod
    def send_registration_mail(user):
        send_mail("register", user['email'], subject='Registro completado')


class GetUsersResource(ModelResource):
    def __init__(self):
        super(GetUsersResource, self).__init__(
            ('\nGet Users:\n'
             '   - Get all users from the database. Login needed.\n'), content_type=None)

    def process(self, req, resp, data=None, errors=[]):
        users = []
        docs = pascuadb.register.find()
        self.logger.debug('There are "' + str(docs.count()) + '" users registered')
        for doc in docs:
            user = UserModel(doc, errors=errors)
            user['_id'] = str(doc['_id'])
            users.append(user)

        return users
