# -*- coding: utf-8 -*-

import time
import random
import signal
import os
import multiprocessing

class externalProcess(multiprocessing.Process):
        """
        This process sends signals to its parent randomly, simulating disasters.
        """

        def __init__(self):
            super().__init__()

        def run(self):
            while(True):
                time.sleep(2)
                x = random.random()
                if x > 0.94 and x < 0.98:
                    #Diplomatic tension
                    os.kill(os.getppid(), signal.SIGINT)
                elif x > 0.98 :
                    #War
                    os.kill(os.getppid(), signal.SIGINT)
                    os.kill(os.getppid(), signal.SIGINT)