from time import sleep

class WaitInstruction:
    def __init__(self, time):
        self.time = time

    def call(self):
        sleep(self.time / 1000)