import threading, time, sys
import chat
import threads

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

#Channel Name from arguments, defaults to what is set in settings.txt
channel = ""
if len(sys.argv) > 1:
    channel = sys.argv[1].lower()

#Create objects
timer = threads.Timer()
receive_chat = chat.Receive(channel)
send_chat = chat.Send(channel)

#ADd to threads array
threads_arr = []
threads_arr.append(timer)
threads_arr.append(receive_chat)

#Start threads
timer.start()
receive_chat.start()

time.sleep(0.5)
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
            send_chat.send("Winning vote: " + str(winning_vote) + " - " + str(winning_amount) + "/" + str(total))
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
                send_chat.send("Stopping")
                voting = False
                timer.voting = False
                timer.seconds = 0

        if voting:
            if message == "!forward": vote_forward += 1
            if message == "!left": vote_left += 1
            if message == "!right": vote_right += 1
            if message == "!backwards": vote_backwards += 1

    time.sleep(0.01)