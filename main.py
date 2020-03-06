from readers.gmailReader import GmailReader
from parsers.gmailParser import GmailParser
from utils.emailAnalyser import EmailAnalyser
from datetime import datetime, timedelta

reader = GmailReader()

now = datetime.today() - timedelta(days=0)
yesterday = datetime.today() - timedelta(days=6)

threads = reader.readThreads(yesterday, now)
parsed = GmailParser.parseThreads(threads)

for p in parsed:
    print(p.messages[0])
    response = EmailAnalyser.calculateResponseArrayForThread(p, reader.me)
    print(response)
