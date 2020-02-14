import time
import socket
import chat
import timer
from argparse import ArgumentParser, RawDescriptionHelpFormatter

def cprint(message):
    cyan = "\033[36m"
    end = "\033[0m"
    if settings['COLOUR'] is True:
        print(cyan + "[Twitch.py] " + end + message)
    else:
        print("[Twitch.py] " + message)

def getWinningVote():
    max = -1
    vote = ""
    votes = [vote_forward, vote_left, vote_right, vote_backwards]
    for i in range(4):
        if votes[i] >= max:
            max = votes[i]
            if i == 0:
                vote = "Forward"
            if i == 1:
                vote = "Left"
            if i == 2:
                vote = "Right"
            if i == 3:
                vote = "Backwards"
    return vote, max

def parse_commands(username, message):
    if message == "!help":
        send_mess = "This is a chat controlled robot, you can type the commands !forward, !left, !right or !backwards to vote. The robot chooses a move every 30 seconds. The move with the most votes is what the robot chooses to do."
        send_chat.send(send_mess)
    if message == "!about":
        send_mess = "I'm a computer science student at the University of Liverpool and this is my final year project, a Twitch chat controlled EV3 Robot."
        send_chat.send(send_mess)
    if message == "!commands":
        send_mess = "!forward, !left, !right, !backwards, !help, !about, !commands"
        send_chat.send(send_mess)

# PROGRAM START
# Load settings
import settings
settings = settings.load()

parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description="Simple Twitch IRC Bot")

parser.add_argument("-c", "--channel", required=True, help="Twitch channel to connect to")
# parser.add_argument("-p", "--port", type=int, help="Change server port. Default is 7766")
parser.add_argument("--disable-logging", action="store_true", dest="disable_logging", default=False, help="Disables chat logging")
parser.add_argument("--local", action="store_true", dest="local", default=False, help="Enables robot connection")
parser.add_argument("--ip", dest="local_ip", help="Robot IP, required if -l is given")
parser.add_argument("--no-colour", action="store_true", dest="no_colour", default=False, help="Don't colour terminal output")
parser.add_argument("-t", "--time", type=int, dest="voting_time", default=30, help="Custom voting time")

args = parser.parse_args()

settings['CHANNEL'] = args.channel.lower()
settings['LOGGING'] = not args.disable_logging
settings['LOCAL'] = args.local
settings['LOCAL_IP'] = args.local_ip
if args.local:
    if args.local_ip is not None:
        settings['LOCAL'] = True
        settings['LOCAL_IP'] = args.local_ip
    else:
        parser.error("-l/--local requires --ip")
settings['COLOUR'] = not args.no_colour
settings['VOTING_TIME'] = args.voting_time

if settings['LOCAL'] == True:
    cprint("Local connection enabled")
    cprint("Local IP: " + settings['LOCAL_IP'])

    # connect to robot
    port = 7766
    robot_conn = socket.socket()
    cprint("Waiting for Local connection")
    while True:
        try:
            robot_conn.connect((settings['LOCAL_IP'], port))
            break
        except: pass
    cprint("Connected")
else: cprint("Local connection disabled")

# Create objects
timer = timer.Timer()
receive_chat = chat.Receive(settings)
send_chat = chat.Send(settings)

# Start threads
timer.start()
receive_chat.start()

time.sleep(0.5)
if settings['CHANNEL'] == "zxqw":
    send_chat.send("Started")

last_message = ""
voting = False
vote_forward = 0
vote_left = 0
vote_right = 0
vote_backwards = 0
while True:
    if voting:
        if timer.seconds >= settings['VOTING_TIME']:
            voting = False
            timer.voting = False
            timer.seconds = 0
            winning_vote, winning_amount = getWinningVote()
            total = vote_forward + vote_left + vote_right + vote_backwards
            send_chat.send("Winning vote: " + winning_vote + " - " + str(winning_amount) + "/" + str(total))
            if settings['LOCAL'] == True:
                robot_conn.send(bytes(winning_vote + '\n', 'UTF-8'))
            vote_forward = 0
            vote_left = 0
            vote_right = 0
            vote_backwards = 0
            voting = True
            timer.voting = True

    if last_message != receive_chat.last_message:
        last_message = receive_chat.last_message
        message_split = last_message.split("*.*")
        username = message_split[1]
        # Just in case someone uses "*.*" in chat
        message_split.pop(0)
        message_split.pop(0)
        message = ""
        for split in message_split:
            message += split

        if username == "zxqw":
            if message == "!start":
                send_chat.send("Accepting Votes")
                voting = True
                timer.voting = True
            elif message == "!stop":
                send_chat.send("Halting voting")
                voting = False
                timer.voting = False
                timer.seconds = 0

        # Parse for commands
        parse_commands(username, message)

        if voting:
            if message == "!forward": vote_forward += 1
            if message == "!left": vote_left += 1
            if message == "!right": vote_right += 1
            if message == "!backwards": vote_backwards += 1

    time.sleep(0.01)
