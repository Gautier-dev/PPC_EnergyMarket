# -*- coding: utf-8 -*-

import time
import multiprocessing

class ClockTick(multiprocessing.Process):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock #Pointer of the shared memory
    def run(self):
        Clock=self.clock
        while True:
            time.wait(2000)
            Clock.value = (Clock.value + 1) % 2

