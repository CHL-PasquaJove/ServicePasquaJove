import falcon
from pascua import pascua_error_codes

pascua_error_codes['INVALID_JSON'] = 1 | pascua_error_codes['NON_BASIC_ERROR']
pascua_error_codes['INVALID_CONTENT_TYPE'] = 2 | pascua_error_codes['NON_BASIC_ERROR']
pascua_error_codes['DUPLICATED_USER_EMAIL'] = 3 | pascua_error_codes['NON_BASIC_ERROR']


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ErrorCodesResource(object):
    def __init__(self):
        self.js_vars = 'var pascua_error_codes={'
        for key in pascua_error_codes:
            value = pascua_error_codes[key]
            self.js_vars += '"' + key + '":' + str(value) + ","

        self.js_vars = self.js_vars[:-1] + "};"

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.content_type='text/javascript'
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = self.js_vars
