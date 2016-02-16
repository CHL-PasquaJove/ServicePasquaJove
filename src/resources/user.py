import falcon
import json
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
            'email': PascuaMail(mandatory=True)
        }


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class NewUserResource(BaseResource):
    def __init__(self):
        super(NewUserResource, self).__init__(
            ('\nNew User:\n'
             '   - Insert a user into database.\n'), model=UserModel)

    def process(self, req, resp, errors):
        data = json.loads(req.stream.read())
        user = UserModel(data, errors=errors)

        resp.status = falcon.HTTP_201
        return user


class GetUsersResource(BaseResource):
    def __init__(self):
        super(GetUsersResource, self).__init__(
            ('\nGet Users:\n'
             '   - Get all users from the database. Login needed.\n'))

    def process(self, req, resp):
        pass