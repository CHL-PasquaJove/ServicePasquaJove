# Import smtplib for the actual sending function
import smtplib
import os

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
textfile = 'mail.html'
toaddrs  = 'fer.roman92@gmail.com'

username = os.environ['PASQUAJOVE_MAIL_ADDRESS']
password = os.environ['PASQUAJOVE_MAIL_PASSWORD']

fp = open(textfile, 'rb')
# Create a text/plain message
msg = MIMEText(fp.read(), 'html')
fp.close()

# me == the sender's email address
# you == the recipient's email address
# msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = 'Responsables Pasqua Jove'
msg['Subject'] = 'Test'
msg['To'] = toaddrs

# Send the message via our own SMTP server, but don't include the
# envelope header.
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username, password)
server.sendmail(username, [toaddrs], msg.as_string())
server.quit()
