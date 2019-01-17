# -*- coding: utf-8 -*-

import time
import multiprocessing

class Clock(multiprocessing.Process):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock #Pointer of the shared memory
    def run(self):
        while True:
            print(Clock.value)
            time.sleep(5)
            self.clock.value = (Clock.value + 1) % 2
