import socket
from threading import Thread

#Class that deals with Twitch chat input
class Game(Thread):

    settings = {}
    conn = None

    robot_pos_x = 0
    robot_pos_y = 0

    # The Map
    Map = [[0 for i in range(6)] for j in range(6)]
    # Blocks
    Map[1][1] = 1
    Map[0][2] = 1
    Map[1][3] = 1
    Map[3][2] = 1
    Map[4][1] = 1
    # Coloured tiles
    Map[1][2] = 5 # Burgandy
    Map[0][3] = 4 # Cyan
    Map[4][2] = 4 # Cyan
    Map[0][5] = 3 # Yellow
    Map[5][5] = 2 # Green

    def __init__(self, settings):
        super(Game, self).__init__()

        # Load settings
        self.settings = settings

    def connect(self):
        # connect to robot
        port = 7766
        robot_conn = socket.socket()
        self.cprint("Waiting for Local connection")
        while True:
            try:
                robot_conn.connect((self.settings['LOCAL_IP'], port))
                break
            except: pass
        self.cprint("Connected")
        return robot_conn

    def send(self, message):
        self.conn.send(bytes(message + '\n', 'UTF-8'))

    def cprint(self, message):
        if self.settings['COLOUR'] == True:
            print("\033[95m" + "[game.py] " + "\033[0m" + message)
        else:
            print("[game.py] " + message)

    def save(self):
        data = "var robot_pos_x = " + str(self.robot_pos_x) + ";\nvar robot_pos_y = " + str(self.robot_pos_y) + ";"
        with open("OBS/robot_data.js", 'w') as filetowrite:
            filetowrite.write(data)

    # Thread
    def run(self):

        if self.settings['LOCAL'] == True:
            self.cprint("Local connection enabled")
            self.cprint("Local IP: " + self.settings['LOCAL_IP'])
            self.conn = self.connect()
            data = ""
            while True:
                try:
                    str = ""
                    while True:
                        data = self.conn.recv(1024).decode("utf-8")
                        str += data
                        if len(str) == 3: break
                    self.robot_pos_y = str.split(",")[0]
                    self.robot_pos_x = str.split(",")[1]
                    if self.Map[int(self.robot_pos_y)][int(self.robot_pos_x)] == 2:
                        self.send("Spin")
                    if self.Map[int(self.robot_pos_y)][int(self.robot_pos_x)] == 3:
                        self.send("Spin")
                    if self.Map[int(self.robot_pos_y)][int(self.robot_pos_x)] == 4:
                        self.send("Spin")
                    if self.Map[int(self.robot_pos_y)][int(self.robot_pos_x)] == 5:
                        self.send("Spin")
                except socket.error:
                    self.cprint(self.colours["RED"] + "Socket timeout" + self.colours["END"])
                    break
                self.cprint("Robot Y: " + self.robot_pos_y + " Robot X: " + self.robot_pos_x)
        else: self.cprint("Local connection disabled")
        return
