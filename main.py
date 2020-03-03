from utils.emailReader import EmailReader
from datetime import datetime, timedelta

reader = EmailReader()

now = datetime.today() - timedelta(days=0)
yesterday = datetime.today() - timedelta(days=6)

mails = reader.readEmails(yesterday, now)
print(len(mails))
mails = reader.removeRepeatedThread(mails)
print(len(mails))

for m in mails:
    reader.calculateResponseArray(m)
    print(str(m.id)+' - '+str(m.fromUser))
    print('response'+str(m.responseArray))