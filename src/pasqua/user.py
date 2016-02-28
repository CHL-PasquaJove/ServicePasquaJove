import smtplib
from email.mime.text import MIMEText

import falcon
import os
from db import pascuadb
from framework import *


class UserModel(PascuaModel):
    def __init__(self, obj=None, errors=[]):
        super(UserModel, self).__init__(obj, errors)

    @staticmethod
    def get_fields():
        return {
            'name': PascuaString(mandatory=True),
            'surname': PascuaString(),
            'email': PascuaMail(mandatory=True),
            'birth': PascuaDate(mandatory=True, yearsBefore=0),
            'phone': PascuaPhone(mandatory=True),
            'group': PascuaString(mandatory=True),
            'invitedBy': PascuaString(mandatory=True),
            'food': PascuaArray(
                PascuaDomain(["diabetes", "celiac", "allergies", "other"]),
                mandatory=True
            )
        }

    def full_name(self):
        if 'surname' in self:
            return self['name'] + ' ' + self['surname']
        return self['name']


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of pasqua and state
# transitions, which map to HTTP verbs.
class NewUserResource(BaseResource):
    def __init__(self):
        super(NewUserResource, self).__init__(
            ('\nNew User:\n'
             '   - Insert a user into database.\n'), model=UserModel)

    def process(self, req, resp, data=None, errors=[]):
        user = UserModel(data, errors=errors)

        insert_user = user.copy()
        check_duplied_mail = pascuadb.register.find_one({ 'email': insert_user['email'] })
        if check_duplied_mail is not None:
            errors.append(PascuaError(
                type=pascua_error_types.WRONG_FIELD,
                field='email',
                description='Duplicated email.',
                code=pascua_error_codes['DUPLICATED_USER_EMAIL']
            ))
            resp.status = falcon.HTTP_409
            return

        pascuadb.register.insert_one(insert_user)
        user['_id'] = str( insert_user['_id'] )

        # Send an email
        self.send_registration_mail(user)

        resp.status = falcon.HTTP_201
        return user

    @staticmethod
    def send_registration_mail(user):
        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        textfile = os.path.dirname(__file__) + '/mails/registro.html'
        toaddrs = user['email']

        username = os.environ['PASQUAJOVE_MAIL_ADDRESS']
        password = os.environ['PASQUAJOVE_MAIL_PASSWORD']

        # Read mail
        fp = open(textfile, 'rb')
        content = fp.read()
        fp.close()

        # Prepare email
        msg = MIMEText(content, 'html')
        msg['Subject'] = 'Registro completado'
        msg['From'] = 'Responsables Pasqua Jove'
        msg['To'] = toaddrs

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(username, [toaddrs], msg.as_string())
        server.quit()


class GetUsersResource(BaseResource):
    def __init__(self):
        super(GetUsersResource, self).__init__(
            ('\nGet Users:\n'
             '   - Get all users from the database. Login needed.\n'), content_type=None)

    def process(self, req, resp, data=None, errors=[]):
        users = []
        docs = pascuadb.register.find()
        for doc in docs:
            user = UserModel(doc)
            user['_id'] = str ( doc['_id'] )
            users.append(user)

        return users
