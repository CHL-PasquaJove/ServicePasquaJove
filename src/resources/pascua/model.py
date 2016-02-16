from abc import ABCMeta, abstractmethod
from errors import PascuaError
import error_types


class PascuaModel(dict):
    __metaclass__ = ABCMeta

    def __init__(self, obj=None, errors=[]):
        self.fields = self.get_fields()
        if obj is not None:
            self.errors = errors
            for key in self.fields:
                field = self.fields[key]
                if key in obj:
                    self.validate_field(key, obj[key], field)
                elif field.mandatory:
                    self.add_err(PascuaError(
                        type=error_types.WRONG_FIELD,
                        description='The field ' + key + ' is mandatory ',
                        field=key
                    ))

    def validate_field(self, key, value, field):
        if field.validate(value):
            self.add_attr(key, value)
        else:
            self.add_err(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The field ' + key + ' with value "' + str(value) + '" is not ' + field.name,
                field=key
            ))

    def add_attr(self, key, value):
        self[key] = value

    def add_err(self, error):
        self.errors.append(error)

    @abstractmethod
    def get_fields(self):
        pass

    def descrive(self):
        model_desc = {}

        for key in self.fields:
            field = self.fields[key]
            model_desc[key] = {
                'type': field.name,
                'mandatory': field.mandatory
            }

        return model_desc