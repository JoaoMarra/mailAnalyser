from .email import EmailThread, MailUser
import datetime

class GmailParser:

    @staticmethod
    def parseThreads(threads):
        parsedArray = []
        for thread in threads:
            parsedArray.append(EmailThread(GmailParser.__gmalThreadToDictionary(thread)))

        return parsedArray;

    @staticmethod
    def __gmalThreadToDictionary(thread):
        obj = {}

        obj['id'] = thread['id']
        messages = thread['messages']
        obj['messages'] = []
        for message in messages:
            to = GmailParser.__searchHeader(message['payload']['headers'], 'To').split(',')
            users = []
            for user in to:
                split = user.split('<')
                users.append({
                    'name' : split[0],
                    'email' : split[1]
                })
            fromUser = GmailParser.__searchHeader(message['payload']['headers'], 'From')
            obj['messages'].append({
                'id' : message['id'],
                'subject' : GmailParser.__searchHeader(message['payload']['headers'], 'Subject'),
                'users' : users,
                'from' : {
                    'name' : fromUser[0],
                    'email' : fromUser[1]
                },
                'date' : datetime.datetime.fromtimestamp(int(message['internalDate'])/1000.0)
            })

        return obj

    @staticmethod
    def __searchHeader(headers, key):
        for h in headers:
            if key == h['name']:
                return h['value']

        return None