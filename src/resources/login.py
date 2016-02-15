import falcon


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class LoginResource(object):
    def __init__(self):
        self.version = 0
        self.description = ('\nLogin:\n'
                            '   - Authentication process. It gives you a token.\n')

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = self.description
