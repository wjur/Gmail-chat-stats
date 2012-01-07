import argparse
from GmailChatStats.DbLoader import DbLoader

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Builds stats DB.')
    parser.add_argument('--username', dest='username', action='store', required='true', type=str, help='Your gmail login (without @gmail.com)')
    parser.add_argument('--password', dest='password', action='store', type=str, help='Your password (you will be asked for it if you skip it)')
    parser.add_argument('--chats', dest='chats', action='store', type=str, help='IMAP name for Chats. It depends on the language you are using in the Gmail. \
    If you are not sure about this please do not pass this argument and the possibilities will be printed out.')

    parser.add_argument('--mode', dest='mode', action='store', choices=["usecache", "nocache", "cacheonly"], default="usecache", type=str, help="Describes how the script will behave. \
    In 'withcache' mode (default) cache will be used and incrementally exapanded by fetching messages from Gmail. In 'nocache' mode cache will not be used (only online data). In 'cacheonly' mode there the data will be fetched only from cache (only offline data)")

    args = parser.parse_args()
    dbloader = DbLoader(args.username, args.password, args.chats, args.mode)
    dbloader.Process()
