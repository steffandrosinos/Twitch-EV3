from threading import Thread
import time


class Timer(Thread):
    voting = False
    seconds = 0

    def run(self):
        while True:
            while self.voting:
                self.seconds += 1
                time.sleep(1)
            self.seconds = 0
            time.sleep(0.1)
        return
