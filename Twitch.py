import threading, time, sys, socket, os
import chat
import timer

def cprint(message):
    cyan = "\033[36m"
    end = "\033[0m"
    if settings['COLOUR'] == "True":
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
            if i == 0: vote = "Forward"
            if i == 1: vote = "Left"
            if i == 2: vote = "Right"
            if i == 3: vote = "Backwards"
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

#Channel Name from arguments, defaults to what is set in settings.txt
channel = ""
if len(sys.argv) > 1:
    channel = sys.argv[1].lower()
    if settings['LOCAL'] == "True":
        try:
            if sys.argv[2] != None:
                if sys.argv[2] == "False": settings['LOCAL'] = "False"
                else: settings['LOCAL_IP'] = sys.argv[2]
        except: pass

if settings['LOCAL'] == "True":
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

#Create objects
timer = timer.Timer()
receive_chat = chat.Receive(channel, settings)
send_chat = chat.Send(channel, settings)

#Add to threads array
threads_arr = []
threads_arr.append(timer)
threads_arr.append(receive_chat)

#Start threads
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
        if timer.seconds >= 30:
            voting = False
            timer.voting = False
            timer.seconds = 0
            winning_vote, winning_amount = getWinningVote()
            total = vote_forward + vote_left + vote_right + vote_backwards
            send_chat.send("Winning vote: " + winning_vote + " - " + str(winning_amount) + "/" + str(total))
            if settings['LOCAL'] == "True":
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
        #Just in case someone uses "*.*" in chat
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

        #Parse for commands
        parse_commands(username, message)

        if voting:
            if message == "!forward": vote_forward += 1
            if message == "!left": vote_left += 1
            if message == "!right": vote_right += 1
            if message == "!backwards": vote_backwards += 1

    time.sleep(0.01)