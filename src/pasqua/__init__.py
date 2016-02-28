from user import NewUserResource, GetUsersResource
from contact import GetContactsResource, NewContactResource
from login import LoginResource
from error_codes import ErrorCodesResource


def init(app):
    # User pasqua
    app.add_route('/api/newUser', NewUserResource())
    app.add_route('/api/getUsers', GetUsersResource())

    # Contact pasqua
    app.add_route('/api/newContact', NewContactResource())
    app.add_route('/api/getContacts', GetContactsResource())

    # Login pasqua
    app.add_route('/api/login', LoginResource())

    # Login pasqua
    app.add_route('/error-codes.js', ErrorCodesResource())
