from abc import ABCMeta, abstractmethod
import falcon
import json
from errors import PascuaError
import error_types
from exceptions import PascuaFieldError
from base_error_codes import pasqua_error_codes
import re


class BaseResource(object):
    pass


class ModelResource(BaseResource):
    __metaclass__ = ABCMeta

    def __init__(self, description, version=0, model=None, content_type='application/json', res_content_type='application/json'):
        self.version = version
        self.description = self.build_description(description, model)
        self.content_type = content_type
        self.res_content_type=res_content_type

    @staticmethod
    def build_description(description, model):
        if model is not None:
            m = model()
            description += "\nModel structure:\n" + json.dumps(m.descrive(), sort_keys=True, indent=2)

        return description

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.set_header(
            'Content-Type',
            'text/plain'
        )
        resp.body = self.description

    def on_post(self, req, resp):
        errors = []
        response = None

        data = self.get_data(req, resp, errors)
        if len(errors) == 0:
            try:
                response = self.process (req, resp, data=data, errors=errors)
            except PascuaFieldError:
                resp.status = falcon.HTTP_400
                pass

        self.respond (req, resp, response, errors)

    def get_data(self, req, resp, errors):
        if self.content_type is None:
            return None

        content_type = re.search("(" + self.content_type + ")", req.content_type, re.IGNORECASE)
        if content_type is None:
            resp.status = falcon.HTTP_400
            errors.append(PascuaError(
                type=error_types.WRONG_REQUEST,
                description='Content-Type must be ' + self.content_type + '.',
                code=pasqua_error_codes['INVALID_CONTENT_TYPE']
            ))
            return None

        if content_type.group() == 'application/json':
            try:
                data = json.loads(req.stream.read())
                return data
            except ValueError:
                resp.status = falcon.HTTP_400
                errors.append(PascuaError(
                    type=error_types.WRONG_REQUEST,
                    description="Invalid JSON file.",
                    code=pasqua_error_codes['INVALID_JSON']
                ))

    @abstractmethod
    def process(self, req, resp, data=None, errors=[]):
        pass

    def respond(self, req, resp, response, errors):
        resp.set_header(
            'Content-Type',
            self.res_content_type
        )

        if len(errors) == 0:
            if response is not None:
                resp.body = json.dumps(response)
        else:
            resp.body = json.dumps({ 'errors': errors })
