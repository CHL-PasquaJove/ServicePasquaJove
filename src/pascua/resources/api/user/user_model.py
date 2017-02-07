from pascua.framework import PascuaModel, PascuaString, PascuaMail, PascuaDate, \
                             PascuaPhone, PascuaArray, PascuaDomain


class UserModel(PascuaModel):
    def __init__(self, obj=None, errors=[]):
        super(UserModel, self).__init__(obj, errors)

    @staticmethod
    def get_fields():
        return {
            'name': PascuaString(mandatory=True),
            'surname': PascuaString(),
            'email': PascuaMail(mandatory=True),
            'birth': PascuaDate(mandatory=True, years_before=0),
            'phone': PascuaPhone(mandatory=True),
            'group': PascuaString(mandatory=True),
            'invitedBy': PascuaString(mandatory=False),
            'food': PascuaArray(
                PascuaDomain(["diabetes", "celiac", "allergies", "other"]),
                mandatory=True
            )
        }

    def full_name(self):
        if 'surname' in self:
            return self['name'] + ' ' + self['surname']
        return self['name']
