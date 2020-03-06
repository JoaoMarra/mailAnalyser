from readers.gmailReader import GmailReader
from parsers.gmailParser import GmailParser
from utils.emailAnalyser import EmailAnalyser
from datetime import datetime, timedelta

reader = GmailReader()

now = datetime.today() - timedelta(days=0)
yesterday = datetime.today() - timedelta(days=6)

threads = reader.readThreads(yesterday, now)
parsed = GmailParser.parseThreads(threads)

response = EmailAnalyser.calculateReponseForUserForThreads(parsed, reader.me)
for r in response:
    print(r + ': '+str(response[r]))
