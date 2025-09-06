import re

PHONE_RE = re.compile(r'(?:\+91[-\s]?)?[6-9]\d{9}')
ABUSE_KEYWORDS = {'idiot','stupid','f**k','f***','bastard','kill','moron','dumb','scam'}
SPAM_KEYWORDS = {'buy now','click here','visit','free','subscribe','discount','offer'}

class ModerationAgent:
    def __init__(self):
        pass

    def contains_phone(self, text):
        return bool(PHONE_RE.search(text or ''))

    def check_abuse(self, text):
        t = (text or '').lower()
        for k in ABUSE_KEYWORDS:
            if k in t:
                return True, k
        return False, None

    def check_spam(self, text):
        t = (text or '').lower()
        for k in SPAM_KEYWORDS:
            if k in t:
                return True, k
        # heuristic: too many links or repeated emoji/characters
        if t.count('http')>1 or t.count('www')>1 or len(set(t)) < 5:
            return True, 'weird'
        return False, None

    def moderate(self, message):
        text = message.get('message','') if isinstance(message, dict) else str(message)
        result = {"status": "Safe", "contains_mobile": False, "flags": []}
        if self.contains_phone(text):
            result['contains_mobile'] = True
            result['flags'].append('contains_mobile')
            result['status'] = 'Unsafe'
        abuse, k = self.check_abuse(text)
        if abuse:
            result['flags'].append('abusive_language')
            result['status'] = 'Abusive'
        spam, sk = self.check_spam(text)
        if spam and result['status']!='Abusive':
            result['flags'].append('spam')
            result['status'] = 'Spam'
        if not result['flags']:
            result['status'] = 'Safe'
        result['reason'] = ' | '.join(result['flags']) if result['flags'] else 'clean'
        return result

if __name__=='__main__':
    m = ModerationAgent()
    print(m.moderate({'message':'Contact +91 9876543210 to buy now!'}))
