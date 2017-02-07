from abc import ABCMeta, abstractmethod
from errors import PascuaError
import error_types
from exceptions import PascuaFieldError
from base_error_codes import pasqua_error_codes
from datetime import datetime


class PascuaModel(dict):
    __metaclass__ = ABCMeta

    def __init__(self, obj=None, errors=None, has_timestamp=True):
        self.fields = self.get_fields()

        if has_timestamp:
            if obj is not None and 'timestamp' in obj:
                self['timestamp'] = obj['timestamp']
            else:
                self.__set_timestamp__()

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
                        code=pasqua_error_codes['MANDATORY_FIELD']
                    ))

        if errors is not None and len(errors) > 0:
            raise PascuaFieldError()

    def __set_timestamp__(self):
        self['timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    def validate_field(self, key, value, field, errors=None):
        if field.validate(value, key, errors):
            self[key] = value

    @abstractmethod
    def get_fields(self):
        pass

    def descrive(self):
        model_desc = {}

        for key in self.fields:
            field = self.fields[key]
            model_desc[key] = self.fields[key].full_description()

        return model_desc