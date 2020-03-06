from utils.gmailReader import GmailReader
from utils.gmailParser import GmailParser
from datetime import datetime, timedelta

reader = GmailReader()

now = datetime.today() - timedelta(days=0)
yesterday = datetime.today() - timedelta(days=6)

threads = reader.readThreads(yesterday, now)
parsed = GmailParser.parseThreads(threads)

for p in parsed:
    print(p)
