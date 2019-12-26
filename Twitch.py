#Imports
import socket, re, time, datetime, sys, os
from random import *

#Load settings
import settings
settings = settings.load()

#Coloured output
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

#User colours
users =	{
  "zxqw": "\033[31m",
  "zxqwbot": "\033[31m"
}

####################################################################
#                             Commands                             #
####################################################################
# Command list
def load_commands():
    commands = {'!commands': command_commands,
    '!help': command_help,
    '!info': command_info,
    '!left': command_left,
    '!right': command_right,
    '!forward': command_forward,
    '!backwards': command_backwards}
    return commands

# Actual Commands
def command_commands():
    commands = load_commands()
    message = "Commands: "
    for command in commands:
        message += command + " "
    send_message(message)
    print(colours["LIGHT_GREEN"] + "Commands detected" + colours["END"])

def command_help():
    message = "To use the robot, use the !forward, !backwards, !left and !right commands to control the robot. Keep in mind multiple people might use the robot at the same time."
    send_message(message)
    print(colours["LIGHT_GREEN"] + "Help detected" + colours["END"])

def command_info():
    message = "I'm a student at the University of Liverpool. This is my third year project in which I make a twitch chat controllable robot."
    send_message(message)
    print(colours["LIGHT_GREEN"] + "Info detected" + colours["END"])

def command_left():
    send_message('Moving left')
    print(colours["LIGHT_GREEN"] + "Left detected" + colours["END"])

def command_right():
    send_message('Moving right')
    print(colours["LIGHT_GREEN"] + "Right detected" + colours["END"])

def command_forward():
    send_message('Moving forward')
    print(colours["LIGHT_GREEN"] + "Forward detected" + colours["END"])

def command_backwards():
    send_message('Moving backwards')
    print(colours["LIGHT_GREEN"] + "Backwards detected" + colours["END"])

####################################################################

####################################################################
#                             Helpers                              #
####################################################################
# 1. Connecting to twitch irc
def connect():
    conn = socket.socket()
    conn.connect((settings['TWITCH_HOST'], settings['TWITCH_PORT']))
    conn.send(bytes('PASS ' + settings['OAUTH'] + '\r\n', 'UTF-8'))
    conn.send(bytes('NICK ' + settings['USERNAME'] + '\r\n', 'UTF-8'))
    conn.send(bytes('JOIN #' + settings['CHANNEL'] + '\r\n', 'UTF-8'))
    return conn

# 2. get username of sender
def get_username(line):
    username = ""
    for char in line:
        if char == "!":
            break
        if char != ":":
            username += char
    return username

# 3. get message
def get_message(line):
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

# 4. parsing message
def parse_message(username, message, command_location):
    if len(message) >= 1:
        message_split = message.split(' ')
        if message_split[0] in commands:
            commands[message_split[0]]()
            message_display = get_time() + " " + username + ": " + message
            save(message_display, command_location)

# 5. send message to chat
def send_message(message):
    conn.send(bytes("PRIVMSG #" + settings["CHANNEL"] + " :" + message + "\r\n", "UTF-8"))

# 6. saving input message to file
def save(message, file_location):
    if settings['LOGGING'] == 'True':
        import io
        with io.open(file_location, "a", encoding="utf-8") as myfile:
            myfile.write(message + "\n")

# 7. Get time
def get_time():
    return datetime.datetime.now().strftime('%H:%M:%S')

# 8. Get Date
def get_date():
    return datetime.datetime.now().strftime('%d-%m-%y')

def send(message):
    robot_conn.send(bytes(message + '\n', 'UTF-8'))

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")

def chat_print(username_, message_, chat_time):
    if username_ in users.keys():
        pass
    else:
        from random import randint
        r = randint(0, 13)
        key = get_nth_key(colours, r)
        users[username_] = colours[key]
    colour = users[username_]
    s = chat_time + " " + colour + username_ + colours["END"] + ": " + message_
    print(s)

####################################################################

####################################################################
#                           Program start                          #
####################################################################

#connect to robot
host = "192.168.1.94" #Robots ip
port = 7766
robot_conn = socket.socket()
robot_conn.connect((host, port))

#Channel Name
if len(sys.argv) > 1:
    settings['CHANNEL'] = sys.argv[1].lower()
print(colours["LIGHT_GREEN"] + "Channel: " + settings['CHANNEL'] + colours["END"])

#Create file for channel
if settings['LOGGING'] == 'True':
    try:
        os.mkdir(settings['CHANNEL'])
        print(colours["LIGHT_GREEN"] + "Creating channel file" + colours["END"])
        try:
            os.mkdir(settings['CHANNEL']+'/'+get_date())
        except:
            print(colours["LIGHT_GREEN"] + "Channel day already created" + colours["END"])
    except:
        print(colours["LIGHT_GREEN"] + "Channel already created" + colours["END"])
        try:
            os.mkdir(settings['CHANNEL']+'/'+get_date())
        except:
            print(colours["LIGHT_GREEN"] + "Channel day already created" + colours["END"])

txt_command_location = settings['CHANNEL'] + "/" + get_date() + "/commands.txt"
txt_chat_location = settings['CHANNEL'] + "/" + get_date() + "/chat.txt"

#load commands
commands = load_commands()
print(colours["LIGHT_GREEN"] + "Commands loaded" + colours["END"])
if settings['LOGGING'] == 'True':
    print(colours["LIGHT_GREEN"] + "LOGGING ENABLED" + colours["END"])
    print(colours["LIGHT_GREEN"] + txt_command_location + colours["END"])
    print(colours["LIGHT_GREEN"] + txt_chat_location + colours["END"])
else:
    print(colours["LIGHT_RED"] + "LOGGING DISABLED" + colours["END"])

conn = connect()
data = ""
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
                    username = get_username(line[0])
                    message = get_message(line)
                    chat_time = get_time()
                    #parse_message(username, message, txt_command_location)
                    chat_print(username, message, chat_time)
                    send(username + ":" + message) #check for split[0] split[1] .. split[n] on receiving end
                    save(chat_time + " " + username + ": " + message, txt_chat_location)
    except socket.error:
        print(colours["RED"] + "Socket timeout" + colours["END"])
