import time
import socket
import chat
import timer
import game
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
    votes = [vote_north, vote_west, vote_east, vote_south]
    for i in range(4):
        if votes[i] >= max:
            max = votes[i]
            if i == 0:
                vote = "North"
            if i == 1:
                vote = "West"
            if i == 2:
                vote = "East"
            if i == 3:
                vote = "South"
    if max == 0:
        vote = "none"
    return vote, max

def parse_commands(username, message):
    if message == "!help":
        send_mess = "This is a chat controlled robot, you can type the commands !north, !west, !east or !south to vote. The robot chooses a move every 30 seconds. The move with the most votes is what the robot chooses to do."
        send_chat.send(send_mess)
    if message == "!about":
        send_mess = "I'm a computer science student at the University of Liverpool and this is my final year project, a Twitch chat controlled EV3 Robot."
        send_chat.send(send_mess)
    if message == "!commands":
        send_mess = "!north, !west, !east, !south, !help, !about, !commands"
        send_chat.send(send_mess)

def obs_data(voting_, vote_north_, vote_west_, vote_east_, vote_south_):
    if voting_:
        voting_str = "true"
    else:
        voting_str = "false"
    data = "var voting = " + voting_str + ";\nvar voting_west = " + str(vote_west_) + ";\nvar voting_east = " + str(vote_east_) + ";\nvar voting_north = " + str(vote_north_) + ";\nvar voting_south = " + str(vote_south_) + ";"
    with open("OBS/stream_data.js", 'w') as filetowrite:
        filetowrite.write(data)

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
parser.add_argument("--OBS", action="store_true", dest="obs", default=False, help="Enables OBS overlay data")

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
settings['OBS'] = args.obs

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
    robot_game = game.Game(settings)
    robot_game.start()
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
    send_chat.send("Running")

last_message = ""
voting = False
vote_north = 0
vote_east = 0
vote_west = 0
vote_south = 0
if settings['OBS']:
    obs_data(voting, vote_north, vote_west, vote_east, vote_south)
while True:
    if voting:
        if timer.seconds >= settings['VOTING_TIME']:
            voting = False
            timer.voting = False
            timer.seconds = 0
            winning_vote, winning_amount = getWinningVote()
            total = vote_north + vote_west + vote_east + vote_south
            if winning_vote != "none":
                send_chat.send("Winning vote: " + winning_vote + " - " + str(winning_amount) + "/" + str(total))
                if settings['LOCAL'] == True:
                    robot_conn.send(bytes(winning_vote + '\n', 'UTF-8'))
            else:
                send_chat.send("No votes recorded - resetting")
            vote_north = 0
            vote_west = 0
            vote_east = 0
            vote_south = 0
            voting = True
            timer.voting = True
            if settings['OBS']:
                obs_data(voting, vote_north, vote_west, vote_east, vote_south)
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
            if message == "!fnorth":
                send_chat.send("Forced North")
                if settings['LOCAL'] == True:
                    robot_conn.send(bytes("North" + '\n', 'UTF-8'))
            elif message == "!fwest":
                send_chat.send("Forced West")
                if settings['LOCAL'] == True:
                    robot_conn.send(bytes("West" + '\n', 'UTF-8'))
            elif message == "!feast":
                send_chat.send("Forced East")
                if settings['LOCAL'] == True:
                    robot_conn.send(bytes("East" + '\n', 'UTF-8'))
            elif message == "!fsouth":
                send_chat.send("Forced South")
                if settings['LOCAL'] == True:
                    robot_conn.send(bytes("South" + '\n', 'UTF-8'))

            if message == "!start":
                send_chat.send("Accepting Votes, getting results every " + str(settings['VOTING_TIME']) + " seconds")
                voting = True
                timer.voting = True
            elif message == "!stop":
                send_chat.send("Not accepting votes")
                voting = False
                vote_north = 0
                vote_west = 0
                vote_east = 0
                vote_south = 0
                if settings['OBS']:
                    obs_data(voting, vote_north, vote_west, vote_east, vote_south)
                timer.voting = False
                timer.seconds = 0

        # Parse for commands
        parse_commands(username, message)

        if voting:
            if message == "!north":
                vote_north += 1
                if settings['OBS']:
                    obs_data(voting, vote_north, vote_west, vote_east, vote_south)
            if message == "!west":
                vote_west += 1
                if settings['OBS']:
                    obs_data(voting, vote_north, vote_west, vote_east, vote_south)
            if message == "!east":
                vote_east += 1
                if settings['OBS']:
                    obs_data(voting, vote_north, vote_west, vote_east, vote_south)
            if message == "!south":
                vote_south += 1
                if settings['OBS']:
                    obs_data(voting, vote_north, vote_west, vote_east, vote_south)

    time.sleep(0.01)
