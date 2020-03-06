import datetime

class EmailThread:
    def __init__(self, thread):
        self.id = thread['id']
        self.messages = []
        self.users = []
        userMap = {}
        for message in thread['messages']:
            threadMessage = EmailThreadMessage(message)
            self.messages.append(threadMessage)
            for user in threadMessage.toUsers:
                if user.email not in userMap:
                    userMap[user.email] = True
                    self.users.append(user)
        self.messages.sort(key=lambda x: x.date)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = str(self.id)+'\n'
        string += 'Start at: '+str(self.messages[0].date)+'\n'
        string += 'Messages: '+str(len(self.messages))+'\n'
        string += 'Users: '+str(len(self.users))
        return string

class EmailThreadMessage:
    def __init__(self, message):
        self.id = message['id']
        self.subject = message['subject']
        self.toUsers = []
        for user in message['users']:
            self.toUsers.append(MailUser(user))
        self.fromUser = MailUser(message['from'])
        self.date = message['date']

    def difTime(self, email):
        return abs((email.date - self.date).total_seconds())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = self.subject+'\n'
        string += 'Date: '+str(self.date)+'\n'
        string += 'From: '+str(self.fromUser)+'\n'
        string += 'Users: '+str(len(self.toUsers))
        return string

class MailUser:
    def __init__(self,user):
        self.name = user['name']
        self.email = user['email']

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.name+' ('+self.email+')')