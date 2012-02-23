class GmailChatStatsError(Exception):
    """Base class for exceptions in GmailChatStats"""
    pass
    
class AuthError(GmailChatStatsError):
    """Base class for exceptions connected with authentication"""
    pass
    
class LoginError(AuthError):
    """Exception raised when login is incorrect"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PasswordError(AuthError):
    """Exception raised when it is unable to login with supplied login and password"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LabelError(GmailChatStatsError):
    pass
        
class LabelNotFoundError(LabelError):
    """Exception raised chats' label is not found"""
    def __init__(self, value, labels):
        self.labels = labels
        self.value = value
    def __str__(self):
        return repr(self.value + " : " + " ".join(self.labels))
        
class InvalidLabelError(LabelError):
    """Exception raised on incorrect chats' label"""
    def __init__(self, value, labels):
        self.labels = labels
        self.value = value
    def __str__(self):
        return repr(self.value + " : " + " ".join(self.labels))
        
class ModeError(GmailChatStatsError):
    """Exception raised on incorrect mode"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
