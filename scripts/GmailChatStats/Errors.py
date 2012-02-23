class GmailChatStatsError(Exception):
    pass
    
class AuthError(GmailChatStatsError):
    pass
    
class LoginError(AuthError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PasswordError(AuthError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class LabelError(GmailChatStatsError):
    def __init__(self, value, labels):
        self.labels = labels
        self.value = value
    def __str__(self):
        return repr(self.value + " : " + " ".join(self.labels))
        
class ModeError(GmailChatStatsError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
