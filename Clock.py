# -*- coding: utf-8 -*-

import time
import multiprocessing

def ClockTick():
    while True:
        time.wait(2000)
        Clock.value = (Clock.value + 1) % 2
        
Clock = multiprocessing.Value('i',1) #Définition de la shared memory

