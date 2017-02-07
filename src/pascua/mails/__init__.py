import os
import smtplib
from email.mime.text import MIMEText
from pascua.config import mail_address, mail_password, mail_from


def send_mail(mail_name, to, subject='No subject'):

    # Read email file
    text_file = os.path.dirname(__file__) + '/' + mail_name + '.html'
    fp = open(text_file, 'rb')
    content = fp.read()
    fp.close()

    # Prepare email
    msg = MIMEText(content, 'html')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = to

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(mail_address, mail_password)
    server.sendmail(mail_address, [to], msg.as_string())
    server.quit()
