
class EmailAnalyser:

    @staticmethod
    def calculateResponseArrayForThread(thread, meUser):
        lastMail = thread.messages[0]
        fromUser = lastMail.fromUser
        responses = []
        turn = 0
        if fromUser.email == meUser:
            turn = 1
        for i in range(1,len(thread.messages)):
            m = thread.messages[i]
            if turn == 0:
                if m.fromUser.email == meUser:
                    responses.append({
                        'index' : i,
                        'seconds' : lastMail.difTime(m),
                        'from' : fromUser
                        })
                    turn = 1
            elif turn == 1:
                if m.fromUser.email != meUser:
                    lastMail = m
                    turn = 0
                    fromUser = m.fromUser
        return responses

    @staticmethod
    def calculateReponseForUserForThreads(threads, meUser):
        responseDictionary = {}
        for thread in threads:
            forThread = EmailAnalyser.calculateResponseArrayForThread(thread, meUser)
            for response in forThread:
                if response['from'].email not in responseDictionary:
                    responseDictionary[response['from'].email] = {
                        'seconds' : response['seconds'],
                        'count' : 1
                    };
                else:
                    responseDictionary[response['from'].email]['seconds'] += response['seconds'];
                    responseDictionary[response['from'].email]['count'] += 1;
        return responseDictionary
