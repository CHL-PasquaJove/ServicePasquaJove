import falcon


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class NewUserResource(object):
    def __init__(self):
        self.version = 0
        self.description = ('\nNew User:\n'
                            '   - Insert a user into database.\n')

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = self.description


class GetUsersResource(object):
    def __init__(self):
        self.version = 0
        self.description = ('\nGet Users:\n'
                            '   - Get all users from the database. Login needed.\n')

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = self.description
