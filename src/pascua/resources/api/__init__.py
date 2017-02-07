from pascua.resources.api.contact import NewContactResource, GetContactsResource
from pascua.resources.api.user import GetUsersResource, NewUserResource
from pascua.resources.api.login import LoginResource


def load_api(app, base_url):
    # User
    app.add_route(base_url + '/newUser', NewUserResource())
    app.add_route(base_url + '/getUsers', GetUsersResource())

    # Login (NOT IMPLEMENTED!)
    app.add_route(base_url + '/login', LoginResource())

    # Contact
    app.add_route(base_url + '/newContact', NewContactResource())
    app.add_route(base_url + '/getContacts', GetContactsResource())
