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
            time.sleep(400)
            x = random.random()
            if x > 0.99:
                os.kill(os.getppid(), signal.SIGINT)