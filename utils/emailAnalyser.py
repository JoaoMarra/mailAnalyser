
class EmailAnalyser:

    @staticmethod
    def calculateResponseArrayForThread(thread, user):
        lastMail = thread.messages[0]
        fromUser = lastMail.fromUser
        responses = []
        turn = 0
        for i in range(1,len(thread.messages)):
            m = thread.messages[i]
            if turn == 0:
                if m.fromUser.email == user:
                    responses.append({
                        'index' : i,
                        'seconds' : lastMail.difTime(m),
                        'from' : fromUser
                        })
                    turn = 1
            elif turn == 1:
                if m.fromUser.email != user:
                    lastMail = m
                    turn = 0
                    fromUser = m.fromUser
        return responses