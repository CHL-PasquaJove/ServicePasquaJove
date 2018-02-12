from pascua.framework import PascuaModel, PascuaString, PascuaMail, PascuaDate, \
                             PascuaPhone, PascuaArray, PascuaDomain


class UserModel(PascuaModel):
    def __init__(self, obj=None, errors=[]):
        super(UserModel, self).__init__(obj, errors)

    @staticmethod
    def get_fields():
        return {
            'name': PascuaString(),
            'surname': PascuaString(),
            'email': PascuaMail(),
            'birth': PascuaDate(years_before=0),
            'phone': PascuaPhone(),
            'group': PascuaString(mandatory=False),
            'invitedBy': PascuaString(),
            'comments': PascuaString(mandatory=False),
            'food': PascuaArray(
                PascuaDomain(["diabetes", "celiac", "allergies", "other"], mandatory=False),
                mandatory=False
            )
        }

    def full_name(self):
        if 'surname' in self:
            return self['name'] + ' ' + self['surname']
        return self['name']
