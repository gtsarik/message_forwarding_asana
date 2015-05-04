"""Get a list of Messages from the user's mailbox
    and send to Asana.
"""

import base64
from asana27 import asana

import sys
sys.path.append('/data/work/virtualenvs/asana/src/ezoffer-taskflow-bridge/library/')

from quickstart import gmail_service
from gmail_get_messages import ListMessagesWithLabelsQuery, GetMessage
from modify_label_messages import CreateMsgLabels, ModifyMessage


unread_label = None
query = 'subject:Top tips for selling your items on eBay: is:unread'
url = 'https://mail.google.com/mail/u/0/#inbox/'
mobile_url = 'https://mail.google.com/mail/mu/mp/638/#cv/Inbox/'
subject = ''
body = ''
id = None

try:
    # Initialization Asana Api for User
    asana_api = asana.AsanaAPI('98V2yZO0.ZuOc40xBAhbJ8k3N1qCWCjN', debug=True)

    # Get list Labels from Gmail account
    labels = gmail_service.users().labels().list(userId='me').execute()

    # Search tags unread
    for label in labels['labels']:
        print 'LABELS ==>> ', label['name']
        # Get id tags unread
        if label['name'] == 'UNREAD':
            unread_label = label['id']

    # Get all unread messages by label
    unread_messages = ListMessagesWithLabelsQuery(
        gmail_service, 'me', query, unread_label)

    # Get letter from an Unread
    for u_msg in unread_messages:
        print 'ID ===>> ', u_msg['id']
        u_messages = GetMessage(gmail_service, 'me', u_msg['id'])

        # print 'END MSG ==>> ', u_messages['payload']
        # print 'END MSG ==>> ', u_messages['payload']['headers']

        # Get Subject of letter
        for u_header in u_messages['payload']['headers']:
            if u_header['name'] == 'Subject':
                subject = u_header['value']

        # Get Body of letter
        for u_part in u_messages['payload']['parts']:
            if u_part['partId'] == '0':
                body = base64.b64decode(u_part['body']['data'])

                # Adds a reference to a letter
                body += '\n\nUrl: ' + url + u_msg['id']
                body += '\nMobile Url: ' + mobile_url + u_msg['id']

        # Asana: See workspaces
        myspaces = asana_api.list_workspaces()

        # Asana: Create task
        asana_api.create_task(
            subject,
            myspaces[0]['id'],
            assignee_status='Activity',
            notes=body)

        msg_labels = ['UNREAD']

        # ModifyMessage(gmail_service, 'me', u_msg['id'], msg_labels)

        # gmail_service.users().modify('me', u_msg['id'], body='INBOX')
        change_lable = gmail_service.users().messages().modify('UNREAD').execute()
except Exception, e:
    print 'ERROR ==>> ', e
