import falcon
from db import pascuadb
from pascua import *
from base_resource import BaseResource
from datetime import datetime


class UserModel(PascuaModel):
    def __init__(self, obj=None, errors=[]):
        super(UserModel, self).__init__(obj, errors)
        self['timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    @staticmethod
    def get_fields():
        return {
            'name': PascuaString(mandatory=True),
            'surname': PascuaString(),
            'email': PascuaMail(mandatory=True),
            'birth': PascuaDate(mandatory=True, yearsBefore=0),
            'phone': PascuaPhone(mandatory=True),
            'group': PascuaString(mandatory=True),
            'invitedBy': PascuaString(mandatory=True),
            'food': PascuaArray(
                PascuaDomain(["diabetes", "celiac", "allergies", "other"]),
                mandatory=True
            )
        }


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class NewUserResource(BaseResource):
    def __init__(self):
        super(NewUserResource, self).__init__(
            ('\nNew User:\n'
             '   - Insert a user into database.\n'), model=UserModel)

    def process(self, req, resp, data=None, errors=[]):
        user = UserModel(data, errors=errors)

        insert_user = user.copy()
        check_duplied_mail = pascuadb.register.find_one({ 'email': insert_user['email'] })
        if check_duplied_mail is not None:
            errors.append(PascuaError(
                type=pascua_error_types.WRONG_FIELD,
                field='email',
                description='Duplicated email.',
                code=pascua_error_codes['DUPLICATED_USER_EMAIL']
            ))
            return

        pascuadb.register.insert_one(insert_user)
        user['_id'] = str( insert_user['_id'] )

        resp.status = falcon.HTTP_201
        return user


class GetUsersResource(BaseResource):
    def __init__(self):
        super(GetUsersResource, self).__init__(
            ('\nGet Users:\n'
             '   - Get all users from the database. Login needed.\n'))

    def process(self, req, resp, errors):
        pass
