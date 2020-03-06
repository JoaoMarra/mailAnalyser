import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailReader:
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
            self.thread = self.service.users().threads();

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

    def readThreads(self, dateStart, dateEnd):
        self.validate()

        query = "before: {0} after: {1}".format(dateEnd.strftime('%Y/%m/%d'),dateStart.strftime('%Y/%m/%d'))

        print('Loading threads: '+query)
        threads = self.thread.list(userId='me',
            labelIds='INBOX',
            q=query
            ).execute().get('threads', []);
        threadArray = []
        for thread in threads:
            tObj = self.thread.get(userId='me',id=thread['id']).execute()
            tObj['messages'] = list(filter(lambda x: (datetime.fromtimestamp(int(x['internalDate'])/1000.0) > dateStart and datetime.fromtimestamp(int(x['internalDate'])/1000.0) < dateEnd), tObj['messages']))
            
            threadArray.append(tObj)

        return threadArray

    def readEmails(self, dateStart, dateEnd):
        self.validate()

        query = "before: {0} after: {1}".format(dateEnd.strftime('%Y/%m/%d'),dateStart.strftime('%Y/%m/%d'))

        print('Loading emails: '+query)

        messages = self.mail.list(userId='me',
            labelIds='INBOX',
            q=query
            ).execute().get('messages', []);

        return messages

    # def calculateResponseArray(self, mail):
        # tService = self.service.users().threads().get(userId='me', id=mail.thread).execute()
        # messages = tService.get('messages', [])

        # lastMail = Email(messages[0])
        # fromUser = lastMail.fromUser
        # responses = []
        # turn = 0
        # for i in range(1,len(messages)):
        #     m = Email(messages[i])
        #     if turn == 0:
        #         if m.fromUser.mail == self.me:
        #             responses.append({
        #                 'index' : i,
        #                 'seconds' : lastMail.difTime(m),
        #                 'from' : fromUser
        #                 })
        #             turn = 1
        #     elif turn == 1:
        #         if m.fromUser.mail != self.me:
        #             lastMail = m
        #             turn = 0
        #             fromUser = m.fromUser
        # mail.responseArray = responses