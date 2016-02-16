from field import PascuaModelField


class PascuaString(PascuaModelField):
    def __init__(self, mandatory=False):
        super(PascuaString, self).__init__('String',
                                           mandatory=mandatory)

    def validate(self, value):
        return isinstance(value, basestring)


class PascuaMail(PascuaString):
    def __init__(self, mandatory=False):
        super(PascuaString, self).__init__('Mail',
                                           mandatory=mandatory)


class PascuaInteger(PascuaModelField):
    def __init__(self, mandatory=False):
        super(PascuaInteger, self).__init__('Integer',
                                            mandatory=mandatory)

    def validate(self, value):
        return isinstance(value, int)

