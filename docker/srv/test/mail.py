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
msg = MIMEText(fp.read(), 'html')
fp.close()

msg['Subject'] = 'Test'
msg['From'] = 'Responsables Pasqua Jove'
msg['To'] = toaddrs
print str(msg)

# Send the message via our own SMTP server, but don't include the
# envelope header.
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
print "Login with '%s' and password: '%s'" % (username, password)
server.login(username, password)
server.sendmail(username, [toaddrs], msg.as_string())
server.quit()
