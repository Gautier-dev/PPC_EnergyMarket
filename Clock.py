# -*- coding: utf-8 -*-

import time
import multiprocessing

class Clock(multiprocessing.Process):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock #Pointer of the shared memory
    def run(self):
        while True:
            print("valeur clock : ", self.clock.value)
            time.sleep(5)
            self.clock.value = (self.clock.value + 1) % 2
