

# -*- coding: utf-8 -*-

import time

def Clock():
    Clock.value = 1  #Initialisation of the shared memory value.
    while True:
        time.wait(1000)
        Clock.value = (Clock.value + 1) % 2

