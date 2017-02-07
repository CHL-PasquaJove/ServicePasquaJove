import falcon
from pascua.framework import pasqua_error_codes, BaseResource

pasqua_error_codes['INVALID_JSON'] = 1 | pasqua_error_codes['NON_BASIC_ERROR']
pasqua_error_codes['INVALID_CONTENT_TYPE'] = 2 | pasqua_error_codes['NON_BASIC_ERROR']
pasqua_error_codes['DUPLICATED_USER_EMAIL'] = 3 | pasqua_error_codes['NON_BASIC_ERROR']
pasqua_error_codes['NON_RESPONSABLE'] = 4 | pasqua_error_codes['NON_BASIC_ERROR']
pasqua_error_codes['WRONG_PASSWORD'] = 5 | pasqua_error_codes['NON_BASIC_ERROR']


class ErrorCodesResource(BaseResource):
    def __init__(self):
        self.js_vars = 'var pascua_error_codes={'
        for key in pasqua_error_codes:
            value = pasqua_error_codes[key]
            self.js_vars += '"' + key + '":' + str(value) + ","

        self.js_vars = self.js_vars[:-1] + "};"

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.content_type='text/javascript'
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = self.js_vars
