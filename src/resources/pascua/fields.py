from field import PascuaModelField
import re
from datetime import datetime
from errors import PascuaError
from base_error_codes import pascua_error_codes
import error_types


# ################################################## PASCUA STRING ################################################### #

class PascuaString(PascuaModelField):
    def __init__(self, mandatory=False):
        super(PascuaString, self).__init__('String',
                                           mandatory=mandatory)

    def validate(self, value, key, errors=None):
        if not isinstance(value, basestring) or value == "":
            self.add_errors(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The field ' + str(key) + ' with value "' + str(value) + '" is not ' + self.name,
                field=key,
                code=pascua_error_codes['WRONG_TYPE']
            ), errors)
            return False

        return True


class PascuaMail(PascuaString):
    def __init__(self, mandatory=False):
        super(PascuaString, self).__init__('Mail',
                                           mandatory=mandatory)

    def validate(self, value, key, errors=None):
        if not super(PascuaMail, self).validate(value) or not re.match('^.+@.+\..+$', value):
            self.add_errors(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The field ' + str(key) + ' with value "' + str(value) + '" is not ' + self.name,
                field=key,
                code=pascua_error_codes['WRONG_TYPE']
            ), errors)
            return False

        return True


class PascuaPhone(PascuaString):
    def __init__(self, mandatory=False):
        super(PascuaString, self).__init__('Phone',
                                           mandatory=mandatory)


class PascuaDomain(PascuaString):
    def __init__(self, possible_values, mandatory=False):
        super(PascuaString, self).__init__('Domain',
                                           mandatory=mandatory)
        self.prepare(possible_values)

    def validate(self, value, key, errors=None):
        if not super(PascuaDomain, self).validate(value, key, errors) or not re.match(self.domain_regex, value):
            self.add_errors(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The field ' + str(key) + ' with value "' + str(value) + '" is not ' + self.name,
                field=key,
                code=pascua_error_codes['WRONG_TYPE']
            ), errors)
            return False

        return True

    def prepare(self, possible_values):
        self.domain_regex = "^" + "|".join(possible_values) + "$"
        self.domain_description = ", ".join(possible_values)

    def description(self):
        return {
            "domain": self.domain_description
        }


class PascuaDate(PascuaString):
    def __init__(self, mandatory=False, yearsBefore=0):
        super(PascuaString, self).__init__('Date',
                                           mandatory=mandatory)
        self.yearsBefore = yearsBefore

    def validate(self, value, key, errors=None):
        try:
            datetime.strptime(value, '%d/%m/%Y')
            return True
        except ValueError:
            self.add_errors(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The field ' + str(key) + ' with value "' + str(value) + '" is not ' + self.name,
                field=key,
                code=pascua_error_codes['WRONG_TYPE']
            ), errors)
            return False

# ################################################ End of PASCUA STRINGS ############################################# #


# ################################################## PASCUA NUMBERS ################################################## #

class PascuaInteger(PascuaModelField):
    def __init__(self, mandatory=False):
        super(PascuaInteger, self).__init__('Integer',
                                            mandatory=mandatory)

# ################################################ End of PASCUA NUMBERS ############################################# #


# ################################################### PASCUA ARRAY ################################################### #

class PascuaArray(PascuaModelField):
    def __init__(self, field, mandatory=False):
        super(PascuaArray, self).__init__('Array',
                                          mandatory=mandatory)
        self.field = field

    def validate(self, value, key, errors=None):
        if not isinstance(value, list):
            self.add_errors(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The field ' + str(key) + ' with value "' + str(value) + '" is not ' + self.name,
                field=key,
                code=pascua_error_codes['WRONG_TYPE']
            ), errors)
            return False

        if errors is not None:
            child_errors = []
        else:
            child_errors = None

        if self.field.mandatory and len(value) == 0:
            self.add_errors(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The array ' + str(key) + ' is emtpy and it''s mandatory',
                field=key,
                code=pascua_error_codes['WRONG_TYPE']
            ), errors)
            return False

        i = 0
        for v in value:
            self.field.validate(v, i, child_errors)
            i += 1

        if len(child_errors):
            self.add_errors(PascuaError(
                type=error_types.WRONG_FIELD,
                description='The field ' + str(key) + ' with value contains an item with errors',
                field=key,
                code=pascua_error_codes['WRONG_TYPE'],
                errors=child_errors
            ), errors)
            return False

        return True

    def description(self):
        return {
            "contains": self.field.full_description()
        }


# ################################################# End of PASCUA ARRAY ############################################## #
