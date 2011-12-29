import getpass
import imaplib
import string
import sys
import email
from xml.dom import minidom
import datetime
import sqlite3

# If you use language other than English
# you have to change 'chats_name'
# (Script will print possible values)
#
#chats_name = '[Gmail]/Pikaviestit' # Finnish :)
chats_name = '[Gmail]/Chats'

# This is your gmail login (without '@gmail.com')
#
# login = 'example'
login = ''

# Ungly global vars :D
full_login = login + '@gmail.com'
table_name = 'stats'

conn = sqlite3.connect('./gmail_stat.db')
# Crate a table stats if it does not exist
conn.execute('CREATE TABLE if not exists '+table_name+'(person TEXT,  mid INTEGER,  year  INTEGER,  month  INTEGER,  day INTEGER,  hour INTEGER,  minute INTEGER, datetime TEXT);')

# We need to clear the table because the retreiving is not incremetal
conn.execute('delete from '+table_name+';')

def parse_folders(folders):
	print folders

def data_to_xml(data):
	msg = email.message_from_string(data[0][1])
	first_att = msg.get_payload()[0]
	xml_string = first_att.get_payload()
	xml_string = str.replace(xml_string, "=\r\n", '')
	xml_string = str.replace(xml_string, "3D", '')
	#print xml_string
	return minidom.parseString(xml_string)

def parse_attr(msg):
	time_element = msg.getElementsByTagName('time')[0]
	time_ms = time_element.getAttribute("ms")
	timestamp = datetime.datetime.fromtimestamp(int(time_ms) / 1000)

	to_attr = msg.getAttribute('to')
	to_attr = to_attr.split('/')[0]
	from_attr = msg.getAttribute('from')
	from_attr = from_attr.split('/')[0]
	#rawtimestamp = msg.getAttribute('int:time-stamp')
	#print 'aaa', rawtimestamp
	chat_type = msg.getAttribute('type')
	#if (chat_type != ''):
	#	timestamp = 0
	#else:
	#	timestamp = datetime.datetime.fromtimestamp(int(rawtimestamp) / 1000)
	return (to_attr, from_attr, timestamp, chat_type)

def add_msg_to_stats(mid, msg):
	sender,receiver,timestamp,chat_type = parse_attr(msg)
	#if (chat_type != ''):
	#	print "Msg no. %d type: %s - omitting" % (mid, chat_type)
	#	return
	#print sender, receiver, timestamp
	conv_with = sender
	if (sender == full_login):
		conv_with = receiver
	sqlcmd = "insert into %s values ('%s', %d,  %d,  %d,  %d,  %d,  %d, '%s')" % (table_name,conv_with,  mid,  timestamp.year,  timestamp.month,  timestamp.day,  timestamp.hour,  timestamp.minute, timestamp.isoformat(' '))
	# print sqlcmd
	conn.execute(sqlcmd)

def parse_msg(login, mid, data):
	#print "login: %s" % login
	#print "mid: %d" % mid
	conTree = data_to_xml(data)
	conNodes = conTree.childNodes
	converstationNode = conNodes[0]
	msgs = converstationNode.childNodes
	for msg in msgs:
		add_msg_to_stats(mid, msg)

if login == '':
	print 'You have to define the login!'
	sys.exit(1)

print 'Logining as %s@gmail.com' % login
password = getpass.getpass()

mail = imaplib.IMAP4_SSL('imap.gmail.com')
print 'Loging to gmail.com...'
try:
	result = mail.login(login, password)
	print '%s - %s' % (result[0], result[1][0])
except imaplib.IMAP4.error as err:
	print err
	mail.close()
	mail.logout()
	sys.exit(1)

print 'Trying to select chats folder... ',
result = mail.select(chats_name, 1)
if result[0] == 'NO':
	print '%s \n%s' % (result[0], result[1][0])
	folders = mail.list()[1]
	print 'Available folders:'
	parse_folders(folders)
else:
	print 'OK'
	print 'Fetching headers...',
	result, data = mail.search(None, 'ALL')
	print result
	chat_ids = (data[0]).split(' ')
	ids_count = len(chat_ids)
	#chat_ids = [23]
	for chat_id in chat_ids:
		print "%s / %d" % (chat_id, ids_count)
		typ, data = mail.fetch(chat_id, '(RFC822)')
		parse_msg(login, int(chat_id), data)

mail.close()
mail.logout()
print 'Commiting to db...'
conn.commit()
conn.close()
