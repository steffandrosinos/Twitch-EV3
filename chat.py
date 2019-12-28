import socket, re, time, datetime, sys, os
from random import *
from threading import Thread

#Class that deals with Twitch chat input
class Receive(Thread):

    settings = {}

    # Coloured output
    colours = {
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
        "PURPLE": "\033[35m",
        "CYAN": "\033[36m",
        "DARK_GRAY": "\033[90m",
        "LIGHT_GREY": "\033[37m",
        "LIGHT_RED": "\033[91m",
        "LIGHT_GREEN": "\033[92m",
        "LIGHT_YELLOW": "\033[93m",
        "LIGHT_BLUE": "\033[94m",
        "LIGHT_PINK": "\033[95m",
        "LIGHT_CYAN": "\033[96m",
        "WHITE": "\033[97m",
        "END": "\033[0m"
    }

    # User colours
    users = {
        "zxqw": "\033[31m",
        "zxqwbot": "\033[31m"
    }

    last_message = ""

    def __init__(self, channel):
        super(Receive, self).__init__()

        # Load settings
        import settings
        self.settings = settings.load()

        if channel != "":
            self.settings['CHANNEL'] = channel

        print(self.colours["LIGHT_GREEN"] + "Channel: " + self.settings['CHANNEL'] + self.colours["END"])
        # Create file for channel
        if self.settings['LOGGING'] == 'True':
            try:
                os.mkdir(self.settings['CHANNEL'])
                print(self.colours["LIGHT_GREEN"] + "Creating channel file" + self.colours["END"])
                try:
                    os.mkdir(self.settings['CHANNEL'] + '/' + self.get_date())
                except:
                    print(self.colours["LIGHT_GREEN"] + "Channel day already created" + self.colours["END"])
            except:
                print(self.colours["LIGHT_GREEN"] + "Channel already created" + self.colours["END"])
                try:
                    os.mkdir(self.settings['CHANNEL'] + '/' + self.get_date())
                except:
                    print(self.colours["LIGHT_GREEN"] + "Channel day already created" + self.colours["END"])

        self.settings['LOCATION'] = self.settings['CHANNEL'] + "/" + self.get_date() + "/chat.txt"
        print(self.colours["LIGHT_GREEN"] + self.settings['LOCATION'] + self.colours["END"])

    # 1. Connect to IRC
    def connect(self):
        conn = socket.socket()
        conn.connect((self.settings['TWITCH_HOST'], self.settings['TWITCH_PORT']))
        conn.send(bytes('PASS ' + self.settings['OAUTH'] + '\r\n', 'UTF-8'))
        conn.send(bytes('NICK ' + self.settings['USERNAME'] + '\r\n', 'UTF-8'))
        conn.send(bytes('JOIN #' + self.settings['CHANNEL'] + '\r\n', 'UTF-8'))
        return conn

    # 2. get username of sender
    def get_username(self, line):
        username = ""
        for char in line:
            if char == "!":
                break
            if char != ":":
                username += char
        return username

    # 3. get message
    def get_message(self, line):
        message = ""
        i = 3
        length = len(line)
        while i < length:
            if i == 3:
                tmp = line[i]
                message += tmp[1:]
                message += " "
            else:
                message += line[i] + " "
            i += 1
        return message

    # 4. saving input message to file
    def save(self, message):
        if self.settings['LOGGING'] == 'True':
            import io
            with io.open(self.settings['LOCATION'], "a", encoding="utf-8") as myfile:
                myfile.write(message + "\n")

    # 5. Get time
    def get_time(self):
        return datetime.datetime.now().strftime('%H:%M:%S')

    # 6. Get Date
    def get_date(self):
        return datetime.datetime.now().strftime('%d-%m-%y')

    # 7. Get index from Users given key
    def get_nth_key(self, dictionary, n=0):
        if n < 0:
            n += len(dictionary)
        for i, key in enumerate(dictionary.keys()):
            if i == n:
                return key
        raise IndexError("dictionary index out of range")

    # 8. Print username with colour and message
    def chat_print(self, username, message, chat_time):
        if username in self.users.keys():
            pass
        else:
            from random import randint
            r = randint(0, 13)
            key = self.get_nth_key(self.colours, r)
            self.users[username] = self.colours[key]
        colour = self.users[username]
        print(chat_time + " " + colour + username + self.colours["END"] + ": " + message)

    # Thread
    def run(self):
        conn = self.connect()
        data = ""
        messages_amount = 0
        while True:
            try:
                data = data + conn.recv(1024).decode('UTF-8')
                data_split = re.split(r"[~\r\n]+", data)
                data = data_split.pop()
                for line in data_split:
                    line = str.rstrip(line)
                    line = str.split(line)
                    if len(line) >= 1:
                        if line[0] == "PING":
                            conn.send(bytes('PONG ' + line[1] + '\r\n', 'UTF-8'))
                        if line[1] == "PRIVMSG":
                            username = self.get_username(line[0])
                            message = self.get_message(line)
                            message = message[:-1]
                            messages_amount += 1
                            chat_time = self.get_time()
                            self.last_message = str(messages_amount) + "*.*" + username + "*.*" + message
                            self.chat_print(username, message, chat_time)
                            #self.save(chat_time + " " + username + ": " + message)
            except socket.error:
                print(self.colours["RED"] + "Socket timeout" + self.colours["END"])
        return

#Sending message to Twitch chat
class Send():

    settings = {}
    conn = ""

    def __init__(self, channel):
        super(Send, self).__init__()

        # Load settings
        import settings
        self.settings = settings.load()

        if channel != "":
            self.settings['CHANNEL'] = channel

        self.conn = self.connect()

    # Connect to IRC
    def connect(self):
        conn = socket.socket()
        conn.connect((self.settings['TWITCH_HOST'], self.settings['TWITCH_PORT']))
        conn.send(bytes('PASS ' + self.settings['OAUTH'] + '\r\n', 'UTF-8'))
        conn.send(bytes('NICK ' + self.settings['USERNAME'] + '\r\n', 'UTF-8'))
        conn.send(bytes('JOIN #' + self.settings['CHANNEL'] + '\r\n', 'UTF-8'))
        return conn

    def send(self, message):
        self.conn.send(bytes("PRIVMSG #" + self.settings["CHANNEL"] + " :" + message + "\r\n", "UTF-8"))