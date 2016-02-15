import user
import contact
import login


def init(app):
    # User resources
    app.add_route('/api/newUser', user.NewUserResource())
    app.add_route('/api/getUsers', user.GetUsersResource())

    # Contact resources
    app.add_route('/api/newContact', contact.NewContactResource())
    app.add_route('/api/getContacts', contact.GetContactsResource())

    # Login resources
    app.add_route('/api/login', login.LoginResource())
