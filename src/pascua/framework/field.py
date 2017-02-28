from abc import ABCMeta, abstractmethod


class PascuaModelField(dict):
    __metaclass__ = ABCMeta

    def __init__(self, name, mandatory=True):
        self.name = name
        self.mandatory = mandatory

    def description(self):
        return {}

    def full_description(self):
        base_description = self.description()
        base_description['type'] = self.name
        base_description['mandatory'] = self.mandatory
        return base_description

    def add_errors(self, error, errors):
        if errors is not None:
            errors.append(error)

    @abstractmethod
    def validate(self, value, key, errors=None):
        print 'SHIT'
        pass
