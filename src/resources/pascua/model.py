from abc import ABCMeta, abstractmethod
from errors import PascuaError
import error_types
from exceptions import PascuaFieldError
from base_error_codes import pascua_error_codes


class PascuaModel(dict):
    __metaclass__ = ABCMeta

    def __init__(self, obj=None, errors=None):
        self.fields = self.get_fields()
        if obj is not None:
            for key in self.fields:
                field = self.fields[key]
                if key in obj:
                    self.validate_field(key, obj[key], field, errors)
                elif errors is not None and field.mandatory:
                    errors.append(PascuaError(
                        type=error_types.WRONG_FIELD,
                        description='The field ' + key + ' is mandatory ',
                        field=key,
                        code=pascua_error_codes['MANDATORY_FIELD']
                    ))

        if errors is not None and len(errors) > 0:
            raise PascuaFieldError()

    def validate_field(self, key, value, field, errors=None):
        if field.validate(value):
            self.add_attr(key, value)
        elif errors is not None:
            errors.append(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The field ' + key + ' with value "' + str(value) + '" is not ' + field.name,
                field=key,
                code=pascua_error_codes['WRONG_TYPE']
            ))

    def add_attr(self, key, value):
        self[key] = value

    @abstractmethod
    def get_fields(self):
        pass

    def descrive(self):
        model_desc = {}

        for key in self.fields:
            field = self.fields[key]
            base_description = field.description()
            base_description['type'] = field.name
            base_description['mandatory'] = field.mandatory
            model_desc[key] = base_description

        return model_desc