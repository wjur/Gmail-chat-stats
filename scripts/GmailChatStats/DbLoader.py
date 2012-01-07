import os
import datetime
import sqlite3
from xml.dom import minidom
from GmailChatStats.Fetcher import FetcherFactory

class DbLoader:

    def __init__(self,username, password, chats, mode):
        self.username = username
        self.fullLogin = "%s@gmail.com" % self.username
        self.password = password
        self.chats = chats
        self.mode = mode
        directory = './output/%s/' % self.username
        if not os.path.isdir(directory):
            os.makedirs(directory)
        self.dbFile = directory + '/stats.db'
        self.tableName = 'stats'
    def __PrintLabels(self,labels):
        for label in labels:
            parts = label.split(' ')
            if (parts[2] != '"INBOX"' and parts[2] != '"/"'):
                print "\t", parts[2]
    def __ConnectToDb(self):
        self.conn = sqlite3.connect(self.dbFile)
        self.conn.execute('DROP TABLE '+self.tableName+';')
        self.conn.execute('CREATE TABLE '+self.tableName+'(person TEXT, dir INTEGER,  mid INTEGER,  year  INTEGER,  month  INTEGER,  day INTEGER,  hour INTEGER,  minute INTEGER, datetime TEXT);')
        
    def __GetMsgAttr(self, msg):
        timeElement = msg.getElementsByTagName('time')[0]
        timeMs = timeElement.getAttribute("ms")
        timestamp = datetime.datetime.fromtimestamp(int(timeMs) / 1000)

        recipient = msg.getAttribute('to').lower()
        recipient = recipient.split('/')[0]
        sender = msg.getAttribute('from').lower()
        sender = sender.split('/')[0]
        chatType = msg.getAttribute('type')
        return {'recipient': recipient, 'sender': sender, 'timestamp': timestamp, 'chatType': chatType}

    def __ProcessMsg(self, mid, msg):
        msgAttributes = self.__GetMsgAttr(msg)
        conv_with = msgAttributes['sender']
        timestamp = msgAttributes['timestamp']
        sent = 0
        if (msgAttributes['sender'] == self.fullLogin):
            conv_with = msgAttributes['recipient']
            sent = 1
        sqlcmd = "insert into %s values ('%s',%d,  %d,  %d,  %d,  %d,  %d, %d, '%s')" % (self.tableName, conv_with, sent,  mid,  timestamp.year,  timestamp.month,  timestamp.day,  timestamp.hour,  timestamp.minute, timestamp.isoformat(' '))
        self.conn.execute(sqlcmd)
        
    def __ProcessChat(self,mid,chat):
        chatTree = minidom.parseString(chat)
        chatNodes = chatTree.childNodes
        converstationNode = chatNodes[0]
        msgs = converstationNode.childNodes
        for msg in msgs:
            self.__ProcessMsg(mid, msg)
        
    def Process(self):
        self.fetcher = FetcherFactory(self.username, self.password, self.chats, self.mode)
        #check if it's possible to connect to gmail (in offline mode it will return no errors)
        loginOk, msg = self.fetcher.Connect()
        if (not loginOk): print msg
        else:
            print "Authorisation OK"
            #check if correct label was specified
            labelOk, labels = self.fetcher.CheckLabel()
            if (not labelOk):
                # lets print the labels so the user can choose the correct one next time ;)
                print "Incorrect chats label. Choose one of those:"
                self.__PrintLabels(labels)
            else:
                self.__ConnectToDb()
                #now we can process all chats
                ids = self.fetcher.GetIDs()
                for mid in ids:
                    print "Processing: ", mid
                    #chat by chat get the XML and process it
                    self.__ProcessChat(mid, self.fetcher.GetXMLString(mid))
            self.__Finalise()
    
    def __Finalise(self):
        self.fetcher.Finalise()
        self.conn.commit()
        self.conn.close()
        
