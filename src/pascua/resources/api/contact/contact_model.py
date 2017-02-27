from pascua.framework import PascuaModel, PascuaMail, PascuaString


class ContactModel(PascuaModel):
    def __init__(self, obj=None, errors=[]):
        super(ContactModel, self).__init__(obj, errors)

    @staticmethod
    def get_fields():
        return {
            'name': PascuaString(),
            'email': PascuaMail(),
            'comment': PascuaString()
        }
