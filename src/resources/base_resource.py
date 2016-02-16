from abc import ABCMeta, abstractmethod
import falcon
import json
from pascua import PascuaError, pascua_error_types


class BaseResource(object):
    __metaclass__ = ABCMeta

    def __init__(self, description, version=0, model=None):
        self.version = version
        self.description = self.build_description(description, model)

    @staticmethod
    def build_description(description, model):
        if model is not None:
            m = model()
            description += "\nModel structure:\n" + json.dumps(m.descrive(), sort_keys=True, indent=2)

        return description


    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = self.description

    def on_post(self, req, resp):
        errors = []
        response = None

        if self.validate(req, resp, errors):
            response = self.process (req, resp, errors)

        self.respond (req, resp, response, errors)

    def validate(self, req, resp, errors):
        if req.content_type != 'application/json':
            errors.append(PascuaError(
                type=pascua_error_types.WRONG_REQUEST,
                description='Content-Type must be application/json.'
            ))
            return False

        return True

    @abstractmethod
    def process(self, req, resp):
        pass

    def respond(self, req, resp, response, errors):
        if len(errors) == 0:
            if response is not None:
                resp.body = json.dumps(response)
        else:
            resp.body = json.dumps({ 'errors': errors })
