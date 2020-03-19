import socket, time
from threading import Thread

#Class that deals with Twitch chat input
class Game(Thread):

    settings = {}

    robot_pos_x = 0
    robot_pos_y = 0

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
        return robot_conn

    def cprint(self, message):
        if self.settings['COLOUR'] == True:
            print("\033[95m" + "[game.py] " + "\033[0m" + message)
        else:
            print("[game.py] " + message)

    def openfile(self):
        file = open('robot_pos.txt', 'r')
        content = file.readline()
        content = content.split(',')
        content[1] = content[1][:-1]
        return int(content[0]), int(content[1])

    def save(self):
        data = "var robot_pos_x = " + str(self.robot_pos_x) + ";\nvar robot_pos_y = " + str(self.robot_pos_y) + ";"
        with open("OBS/robot_data.js", 'w') as filetowrite:
            filetowrite.write(data)

    # Thread
    def run(self):
        conn = self.connect()
        data = ""
        while True:
            try:
                str = ""
                while True:
                    data = conn.recv(1024).decode("utf-8")
                    str += data
                    if len(str) == 3: break
                self.robot_pos_y = str.split(",")[0]
                self.robot_pos_x = str.split(",")[1]
            except socket.error:
                self.cprint(self.colours["RED"] + "Socket timeout" + self.colours["END"])
                break
            self.cprint("Robot X: " + self.robot_pos_x + " Robot Y: " + self.robot_pos_y)
        return
