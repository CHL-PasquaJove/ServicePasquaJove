from abc import ABCMeta, abstractmethod


class PascuaModelField(dict):
    __metaclass__ = ABCMeta

    def __init__(self, name, mandatory=False):
        self.name = name
        self.mandatory = mandatory

    def description(self):
        return {}

    @abstractmethod
    def validate(self, value):
        pass
