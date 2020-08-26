import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
import pickle
from googleapiclient.discovery import build

from apiclient import errors

def create_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    with open(os.path.join('.credentials','token.pickle'), 'rb') as token:
        creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(message_text):
    message = MIMEText(message_text)
    message['to'] = 'microgreensnw@gmail.com'
    message['from'] = 'microgreensnw@gmail.com'
    message['subject'] = 'New Message From Website'
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(message):

  service = create_service()
  try:
    message = (service.users().messages().send(userId='microgreensnw@gmail.com', body=create_message(message))
               .execute())
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

