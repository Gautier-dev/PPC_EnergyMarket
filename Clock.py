# -*- coding: utf-8 -*-

import time
import multiprocessing

class ClockTick(multiprocessing.process):
    def __init__(self,clock):
        super().__init__()
        self.clock=clock #Pointer of the shared memory
    def run(self):
        Clock=self.clock
        while True:
            time.wait(2000)
            Clock.value = (Clock.value + 1) % 2
        
Clock = multiprocessing.Value('i',1) #Définition de la shared memory

tick = ClockTick(Clock)
tick.start()
