import falcon

from pascua.db import pascuadb
from pascua.framework import ModelResource
from pascua.resources.api.contact.contact_model import ContactModel


class NewContactResource(ModelResource):
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


class GetContactsResource(ModelResource):
    def __init__(self):
        super(GetContactsResource, self).__init__(
            ('\nGet Contacts:\n'
             '   - Get all contacts from the database. Login needed\n'))

    def process(self, req, resp, data=None, errors=[]):
        users = []
        docs = pascuadb.contact.find()
        for doc in docs:
            user = ContactModel(doc)
            user['_id'] = str ( doc['_id'] )
            users.append(user)

        return users
