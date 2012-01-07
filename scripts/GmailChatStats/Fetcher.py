import imaplib
import os
import email
import getpass
from sets import Set


class AbstractFetcher(object):
    def __init__(self, username, password, chats):
        self.username = username
        self.password = password
        self.cachePath = './output/%s/cache/' % self.username
        if not os.path.isdir(self.cachePath):
            os.makedirs(self.cachePath)
        if (chats != None):
            self.chats = chats
        else:
            self.chats = "[Gmail]/Chats"
            
    def CheckChats(self):
        raise NotImplementedError
                
    def Connect(self):
        raise NotImplementedError
    def CheckLabel(self):
        raise NotImplementedError
    def GetIDs(self):
        raise NotImplementedError
    def GetXMLString(self, mid):
        raise NotImplementedError
    def GetPassword(self):
        while (self.password == None or self.password == ""):
            self.password = getpass.getpass("Password for %s@gmail.com: " % self.username)


    def GetXMLStringFromCache(self, mid):
        fileName = self.cachePath + str(mid)
        f = open(fileName, 'r')
        xmlString = f.read()
        f.close()
        return xmlString

    def GetXMLStringFromServer(self, mid):
        typ, data = self.mail.fetch(mid, '(RFC822)')
        msg = email.message_from_string(data[0][1])
        firstAtt = msg.get_payload()[0]
        xmlString = firstAtt.get_payload()
        xmlString = str.replace(xmlString, "=\r\n", '')
        xmlString = str.replace(xmlString, "3D", '')
        return xmlString

    def SaveXMLStringToCache(self, xmlString, mid):
        fileName = self.cachePath + str(mid)
        f = open(fileName, 'w')
        f.write(xmlString)
        f.close()
        return

    def GetCachedIDs (self):
        dirList=os.listdir(self.cachePath)
        cacheIds = [i for i in dirList]
        return Set(cacheIds)

    def GetOnlineIDs(self):
        result, data = self.mail.search(None, 'ALL')
        # error? who cares ;)
        onlineIds = (data[0]).split(' ')
        onlineIds = [i for i in onlineIds]
        return Set(onlineIds)

    def set_to_sortedlist(self, someset):
        someset = [int(i) for i in someset]
        someset.sort()
        return someset


def FetcherFactory(username, password, chats, mode):
        for fetchers in AbstractFetcher.__subclasses__():
                if fetchers.is_registrar_for(mode):
                    return fetchers(username, password, chats)
        raise ValueError


class NormalFetcher(AbstractFetcher):
    @classmethod
    def is_registrar_for(cls, mode):
        return mode == "usecache"

    def Connect(self):
        if (self.password == None):
            super(NormalFetcher, self).GetPassword()
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            result = self.mail.login(self.username, self.password)
            return [True, "Connected succesfully"]
        except imaplib.IMAP4.error as err:
            return [False, err]

    def CheckLabel(self):
        result = self.mail.select(self.chats, 1)
        if result[0] == 'NO':
            folders = self.mail.list()[1]
            return [False, folders]
        return [True, None]
    def Finalise(self):
        self.mail.close()
        self.mail.logout()

    def GetIDs(self):
        cached = super(NormalFetcher, self).GetCachedIDs()
        online = super(NormalFetcher, self).GetOnlineIDs()
        ids = cached | online
        self.cached = super(NormalFetcher, self).set_to_sortedlist(cached)
        self.online = super(NormalFetcher, self).set_to_sortedlist(online)
        self.ids = super(NormalFetcher, self).set_to_sortedlist(ids)
        return self.ids

    def GetXMLString(self, mid):
        if (mid in self.cached):
            return super(NormalFetcher, self).GetXMLStringFromCache(mid)
        else:
            xmlString = super(NormalFetcher, self).GetXMLStringFromServer(mid)
            super(NormalFetcher, self).SaveXMLStringToCache(xmlString, mid)
            return xmlString



class CacheonlyFetcher(AbstractFetcher):
    @classmethod
    def is_registrar_for(cls, mode):
        return mode == "cacheonly"

    def Connect(self):
        return [True, "Connected succesfully"]


    def CheckLabel(self):
        return [True, None]
    def Finalise(self):
        return

    def GetIDs(self):
        cached = super(CacheonlyFetcher, self).GetCachedIDs()
        online = Set([])
        ids = cached | online
        self.cached = super(CacheonlyFetcher, self).set_to_sortedlist(cached)
        self.online = super(CacheonlyFetcher, self).set_to_sortedlist(online)
        self.ids = super(CacheonlyFetcher, self).set_to_sortedlist(ids)
        return self.ids

    def GetXMLString(self, mid):
        if (mid in self.cached):
            return super(CacheonlyFetcher, self).GetXMLStringFromCache(mid)



class NocacheFetcher(AbstractFetcher):
    @classmethod
    def is_registrar_for(cls, mode):
        return mode == "nocache"

    def Connect(self):
        if (self.password == None):
            super(NormalFetcher, self).GetPassword()
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            result = self.mail.login(self.username, self.password)
            return [True, "Connected succesfully"]
        except imaplib.IMAP4.error as err:
            return [False, err]

    def CheckLabel(self):
        result = self.mail.select(self.chats, 1)
        if result[0] == 'NO':
            folders = self.mail.list()[1]
            return [False, folders]
        return [True, None]
    def Finalise(self):
        self.mail.close()
        self.mail.logout()

    def GetIDs(self):
        cached = Set([])
        online = super(NormalFetcher, self).GetOnlineIDs()
        ids = cached | online
        self.cached = super(NormalFetcher, self).set_to_sortedlist(cached)
        self.online = super(NormalFetcher, self).set_to_sortedlist(online)
        self.ids = super(NormalFetcher, self).set_to_sortedlist(ids)
        return self.ids

    def GetXMLString(self, mid):
        xmlString = super(NormalFetcher, self).GetXMLStringFromServer(mid)
        return xmlString