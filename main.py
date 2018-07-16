import base64
import threading
from email.mime.text import MIMEText
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from httplib2 import Http

import check

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(
        'client_secret_804152642149-49tnvklbemduaa8ab1p2tol5rs04vkcd.apps.googleusercontent.com.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))


def send_email(recipient, subject, body):
    mail = MIMEText(body)
    mail['to'] = recipient
    mail['from'] = 'openutclass@gmail.com'
    mail['subject'] = subject

    message = {'raw': base64.urlsafe_b64encode(mail.as_string().encode()).decode()}

    message = (service.users().messages().send(userId='openutclass@gmail.com', body=message)
               .execute())

    return message


def check_status():
    status = check.get_course_status(16150)

    if status != "closed":
        send_email('jspspike@gmail.com', 'Class has opened', '{0} is now {1}'.format(16150, status))

    threading.Timer(1, check_status).start()


check_status()
