import error_types


class PascuaError(dict):
    def __init__(self, type=error_types.GENERAL_ERROR, description=None, field=None):
        self.set_non_none('type', type)
        self.set_non_none('description', description)
        self.set_non_none('field', field)

    def set_non_none(self, key, value):
        if value is not None:
            self[key] = value