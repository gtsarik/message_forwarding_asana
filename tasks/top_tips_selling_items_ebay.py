# -*- coding: utf-8 -*-
import imaplib
import email

from asana27 import asana


asana_api = asana.AsanaAPI('id_asana_user', debug=True)

# Login and Password Emeil
username = 'your@mail.com'
password = 'password'

# Connect the gmail.com through imap4_ssl
gmail = imaplib.IMAP4_SSL('imap.gmail.com', '993')

try:
    gmail.login(username, password)

    # Selects from the Inbox unread messages
    typ, count = gmail.select('INBOX')

    # The number of unread messages in your Inbox
    typ, unseen = gmail.status('INBOX', "(UNSEEN)")

    # Main unit
    typ, data = gmail.search(None, '(UNSEEN)')

    for i in data[0].split():
        typ, message = gmail.fetch(i, '(RFC822)')

        for n in message:
            mail = email.message_from_string(n[1])
            subject = mail.get('Subject')
            header = email.Header.decode_header(subject)[0]
            subject_asana = header[0]

            if subject_asana == 'Subject message for to forwarding to Sasna':
                # Get message body
                msg_parts = [
                    (part.get_filename(), part.get_payload(decode=True))
                    for part in mail.walk() if part.get_content_type() == 'text/plain']

                for name, data in msg_parts:
                    udata = str(data)
                    # msg_body = udata.decode('koi8-r').encode('utf-8')
                    # msg_body = udata.decode('koi8-u').encode('utf-8')

                # see workspaces
                myspaces = asana_api.list_workspaces()

                # Create task
                asana_api.create_task(
                    subject_asana,
                    myspaces[0]['id'],
                    assignee_status='Activity',
                    notes=udata)
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
finally:
    # Disconnected from the gmail.com
    gmail.close()
    gmail.logout()
