import socket, re, datetime, os
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
        "BOLD": "\033[1m\033[4m",
        "END": "\033[0m",
        "BOLDEND": "\033[0m\033[0m"
    }

    # User colours
    users = {
        "zxqw": "\033[31m",
        "zxqwbot": "\033[31m"
    }

    last_message = ""
    messages = []

    def __init__(self, settings):
        super(Receive, self).__init__()

        # Load settings
        self.settings = settings

        self.cprint("Channel: " + self.settings['CHANNEL'])
        # Create file for channel
        if self.settings['LOGGING'] == True:
            try:
                os.mkdir('Logs')
            except:
                pass
            try:
                os.mkdir('Logs/' + self.settings['CHANNEL'])
                self.cprint("Creating channel file")
                try:
                    os.mkdir('Logs/' + self.settings['CHANNEL'] + '/' + self.get_date())
                except:
                    self.cprint("Channel day already created")
            except:
                self.cprint("Channel already created")
                try:
                    os.mkdir('Logs/' + self.settings['CHANNEL'] + '/' + self.get_date())
                except:
                    self.cprint("Channel day already created")
            self.settings['LOCATION'] = "Logs/" + self.settings['CHANNEL'] + "/" + self.get_date() + "/chat.txt"
            self.cprint(self.settings['LOCATION'])
        else:
            self.cprint("Logging disabled")

    # 1. Coloured Print
    def cprint(self, message):
        if self.settings['COLOUR'] == True:
            print(self.colours["LIGHT_GREEN"] + "[chat.py] " + self.colours["END"] + message)
        else:
            print("[chat.py] " + message)

    # 2. Print username with colour and message
    def chat_print(self, username, message, chat_time):
        #check for tags

        if self.settings['COLOUR'] == True:
            colour = self.users[username]
            if username == self.settings['USERNAME']:
                print("[" + chat_time + "] " + self.colours['BOLD'] + colour + username + self.colours["END"] +
                      self.colours["BOLDEND"] + ": " + message)
            else:
                print("[" + chat_time + "] " + colour + username + self.colours["END"] + ": " + message)
        else:
            print("[" + chat_time + "] " + username + ": " + message)

    # 3. Connect to IRC
    def connect(self):
        conn = socket.socket()
        conn.connect((self.settings['TWITCH_HOST'], self.settings['TWITCH_PORT']))
        conn.send(bytes('PASS ' + self.settings['OAUTH'] + '\r\n', 'UTF-8'))
        conn.send(bytes('NICK ' + self.settings['USERNAME'] + '\r\n', 'UTF-8'))
        conn.send(bytes('JOIN #' + self.settings['CHANNEL'] + '\r\n', 'UTF-8'))
        conn.send(bytes('CAP REQ :twitch.tv/membership' + '\r\n', 'UTF-8'))
        conn.send(bytes('CAP REQ :twitch.tv/tags' + '\r\n', 'UTF-8'))
        conn.send(bytes('CAP REQ :twitch.tv/commands' + '\r\n', 'UTF-8'))
        return conn

    # 4. get username of sender
    def get_username(self, line):
        username = ""
        for char in line:
            if char == "!": break
            if char != ":": username += char
        if username in self.users.keys(): pass
        else:
            from random import randint
            r = randint(0, 13)
            key = self.get_nth_key(self.colours, r)
            self.users[username] = self.colours[key]
        return username

    # 5. get message
    def get_message(self, line):
        message = ""
        i = 4
        while i < len(line):
            if i == 4:
                message += line[i][1:]
                message += " "
            else:
                message += line[i] + " "
            i += 1
        return message

    # 6. saving input message to file
    def save(self, message):
        if self.settings['LOGGING'] == True:
            import io
            with io.open(self.settings['LOCATION'], "a", encoding="utf-8") as myfile:
                myfile.write(message + "\n")

    # 7. Get time
    def get_time(self):
        return datetime.datetime.now().strftime('%H:%M:%S')

    # 8. Get Date
    def get_date(self):
        return datetime.datetime.now().strftime('%d-%m-%y')

    # 9. Get index from Users given key
    def get_nth_key(self, dictionary, n=0):
        if n < 0: n += len(dictionary)
        for i, key in enumerate(dictionary.keys()):
            if i == n: return key
        raise IndexError("dictionary index out of range")

    def obs_data(self, message):
        if (len(self.messages) < 10):
            self.messages.append(message)
        else:
            # Move all elements up one
            temp = []
            for i in range(1, len(self.messages)):
                temp.append(self.messages[i])
            temp.append(message)
            self.messages = temp
        self.obs_data_update()

    def obs_data_update(self):
        data = ""
        for i in range(0, len(self.messages)):
            data += "'"
            for char in self.messages[i]:
                # User can type escape character "\" which will break code.
                # Warninge fix this by making sure we replace every backslash with
                # two backslashes
                if char != "\\":
                    data += char
                else:
                    data += "\\\\"
            data += "',\n"
        final = "var messages = [\n" + data + "];"
        obs_location = "OBS/chat_data.js"
        with open(obs_location, 'w') as filetowrite:
            filetowrite.write(final)

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
                        elif line[2] == "PRIVMSG":
                            username = self.get_username(line[1])
                            message = self.get_message(line)
                            message = message[:-1]
                            messages_amount += 1
                            chat_time = self.get_time()
                            self.last_message = str(messages_amount) + "*.*" + username + "*.*" + message
                            self.chat_print(username, message, chat_time)
                            self.save(chat_time + " " + username + ": " + message)
                            if self.settings['OBS']:
                                self.obs_data(chat_time[:-3] + "*.*" + username + ":*.*" + message)
            except socket.error:
                print(self.colours["LIGHT_GREEN"] + "[chat.py] " + self.colours["END"] + self.colours["RED"] + "Socket timeout" + self.colours["END"])
        return

#Sending message to Twitch chat
class Send():

    settings = {}
    conn = ""

    def __init__(self, settings):
        super(Send, self).__init__()
        self.settings = settings
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
