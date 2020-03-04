import socket, re, datetime, os
from threading import Thread

#Class that deals with Twitch chat input
class Game(Thread):

    def __init__(self, settings):
        super(Game, self).__init__()

        # Load settings
        self.settings = settings

    def connect(self):
        # connect to robot
        port = 7767
        robot_conn = socket.socket()
        self.cprint("Waiting for Local connection")
        while True:
            try:
                robot_conn.connect((self.settings['LOCAL_IP'], port))
                break
            except: pass
        self.cprint("Connected")

    def cprint(self, message):
        if self.settings['COLOUR'] == True:
            print("\033[95m" + "[game.py] " + "\033[0m" + message)
        else:
            print("[chat.py] " + message)

    # Thread
    def run(self):
        conn = self.connect()
        #while True:
        return
