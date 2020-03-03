import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class Email:
    def __init__(self, message):
        self.id = message['id']
        self.thread = message['threadId']
        self.date = datetime.datetime.fromtimestamp(int(message['internalDate'])/1000.0)
        toUsers = self.searchHeader(message['payload']['headers'], 'To').split(',')
        self.toUsers = []
        for user in toUsers:
            self.toUsers.append(MailUser(user))
        self.fromUser = MailUser(self.searchHeader(message['payload']['headers'], 'From'))
        self.subject = self.searchHeader(message['payload']['headers'], 'Subject')
        self.responseArray = []

    def searchHeader(self, headers, key):
        for h in headers:
            if key == h['name']:
                return h['value']

        return None

    def difTime(self, mail):
        return abs((mail.date - self.date).total_seconds())


class MailUser:
    def __init__(self,user):
        split = user.split('<')
        self.name = split[0].replace('"','')
        self.mail = split[1].replace('>','')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.name+' ('+self.mail+')')

class EmailReader:
    def __init__(self):
        self.creds = None
        self.validate()

    def buildCredential(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        if self.creds:
            self.service = build('gmail', 'v1', credentials=self.creds)
            self.mail = self.service.users().messages();

    def validate(self):
        if not self.creds or not self.creds.valid:
            self.buildCredential()
            self.loadLabels()
            self.buildMe()

    def loadLabels(self):
        self.validate()

        results = self.service.users().labels().list(userId='me').execute()
        self.labels = results.get('labels', [])

    def buildMe(self):
        self.validate()

        self.me = self.service.users().getProfile(userId='me').execute()['emailAddress']

    def readEmails(self, dateStart, dateEnd):
        self.validate()

        query = "before: {0} after: {1}".format(dateEnd.strftime('%Y/%m/%d'),dateStart.strftime('%Y/%m/%d'))

        print('Loading emails: '+query)

        messages = self.mail.list(userId='me',
            labelIds='INBOX',
            q=query
            ).execute().get('messages', []);

        mails = []
        for message in messages:
            email = self.mail.get(userId='me',id=message['id']).execute()
            mails.append(Email(email))

        return mails

    def removeRepeatedThread(self, mails):
        cleanMails = []
        threads = {}
        for mail in mails:
            if mail.thread not in threads:
                cleanMails.append(mail)
                threads[mail.thread] = True

        return cleanMails

    def calculateResponseArray(self, mail):
        tService = self.service.users().threads().get(userId='me', id=mail.thread).execute()
        messages = tService.get('messages', [])

        lastMail = Email(messages[0])
        fromUser = lastMail.fromUser
        responses = []
        turn = 0
        for i in range(1,len(messages)):
            m = Email(messages[i])
            if turn == 0:
                if m.fromUser.mail == self.me:
                    responses.append({
                        'index' : i,
                        'seconds' : lastMail.difTime(m),
                        'from' : fromUser
                        })
                    turn = 1
            elif turn == 1:
                if m.fromUser.mail != self.me:
                    lastMail = m
                    turn = 0
                    fromUser = m.fromUser
        mail.responseArray = responses

