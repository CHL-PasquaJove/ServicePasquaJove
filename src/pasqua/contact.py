import falcon
from db import pascuadb
from framework import *


class ContactModel(PascuaModel):
    def __init__(self, obj=None, errors=[]):
        super(ContactModel, self).__init__(obj, errors)

    @staticmethod
    def get_fields():
        return {
            'name': PascuaString(mandatory=True),
            'email': PascuaMail(mandatory=True),
            'comment': PascuaString(mandatory=True)
        }


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of pasqua and state
# transitions, which map to HTTP verbs.
class NewContactResource(BaseResource):
    def __init__(self):
        super(NewContactResource, self).__init__(
            ('\nNew Contact:\n'
             '   - Insert a contact into database.\n'), model=ContactModel)

    def process(self, req, resp, data=None, errors=[]):
        contact = ContactModel(data, errors=errors)

        insert_contact = contact.copy()
        pascuadb.contact.insert_one(insert_contact)
        contact['_id'] = str( insert_contact['_id'] )

        resp.status = falcon.HTTP_201
        return contact


class GetContactsResource(BaseResource):
    def __init__(self):
        super(GetContactsResource, self).__init__(
            ('\nGet Contacts:\n'
             '   - Get all contacts from the database. Login needed\n'), content_type=None)

    def process(self, req, resp, data=None, errors=[]):
        users = []
        docs = pascuadb.contact.find()
        for doc in docs:
            user = ContactModel(doc)
            user['_id'] = str ( doc['_id'] )
            users.append(user)

        return users
