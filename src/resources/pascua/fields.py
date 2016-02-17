from field import PascuaModelField
import re
from datetime import datetime


# ################################################## PASCUA STRING ################################################### #

class PascuaString(PascuaModelField):
    def __init__(self, mandatory=False):
        super(PascuaString, self).__init__('String',
                                           mandatory=mandatory)

    def validate(self, value):
        return isinstance(value, basestring) and value != ""


class PascuaMail(PascuaString):
    def __init__(self, mandatory=False):
        super(PascuaString, self).__init__('Mail',
                                           mandatory=mandatory)

    def validate(self, value):
        return super(PascuaMail, self).validate(value) and \
               re.match('^.+@.+\..+$', value)


class PascuaPhone(PascuaString):
    def __init__(self, mandatory=False):
        super(PascuaString, self).__init__('Phone',
                                           mandatory=mandatory)


class PascuaDomain(PascuaString):
    def __init__(self, mandatory=False, possible_values=[]):
        super(PascuaString, self).__init__('Domain',
                                           mandatory=mandatory)
        self.prepare(possible_values)

    def validate(self, value):
        return super(PascuaDomain, self).validate(value) and \
               re.match(self.domain_regex, value)

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

    def validate(self, value):
        try:
            datetime.strptime(value, '%d/%m/%Y')
            return True
        except ValueError:
            return False

# ################################################ End of PASCUA STRINGS ############################################# #

# ################################################## PASCUA NUMBERS ################################################## #

class PascuaInteger(PascuaModelField):
    def __init__(self, mandatory=False):
        super(PascuaInteger, self).__init__('Integer',
                                            mandatory=mandatory)

# ################################################ End of PASCUA NUMBERS ############################################# #
