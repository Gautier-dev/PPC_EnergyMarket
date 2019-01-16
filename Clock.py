# -*- coding: utf-8 -*-

import time
import multiprocessing

class Clock(multiprocessing.Process):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock #Pointer of the shared memory
    def run(self):
        Clock=self.clock
        while True:
            time.sleep(2)
            Clock.value = (Clock.value + 1) % 2
