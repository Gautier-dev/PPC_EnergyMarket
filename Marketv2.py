# -*- coding: utf-8 -*-

"""
EACH TRANSACTION IS PERFORMED ON THE NIGHT
NIGHT : ONLY THE CALCULATION OF THE PRICE
"""


import multiprocessing
import time
import random
import threading
import sysv_ipc
import concurrent.futures
import signal
import os



 #IRA DANS LE MAIN :         
externalFactors = threading.Value('i',0) #This is a counter of the disasters that occurs sometimes.    
lockExternal = threading.lock()
        
        
GlobalNeed = threading.Value('i',0) #Energy wanted by the house (initialisation)
lockGlobalNeed = threading.lock() #Protection
        
        
PayableEnergyBank = threading.Value('i',0) #(initialisation)
lockPayable = threading.lock()       

#The clock is a shared variable
Clock = multiprocessing.Value('i',1) #Définition de la shared memory

#The weather is a shared array
Weather = multiprocessing.Array('i', [0,0])

class Market(multiprocessing.Process):
    """
    Class defining the Market process.
    n = number of houses
    Father of the External Process.
    While the Clock.Value is equal to 1, it receives all the data of the houses.
    It increments energy banks and updates an array representing the need of all the houses.
    When the Clock.Value is equal to 0, it calculates the price of the energy and tell the houses what they have to pay to receive it.
    """
    
    def __init__(self,n):
        super().__init__()
        self.numberOfHouses = n
        self.mq = sysv_ipc.MessageQueue(-1, sysv_ipc.IPC_CREAT)
        self.clock = Clock.value

    def priceCalculation(self, PayableEnergyWanted, PayableEnergyBank, externalFactors, price):
        """
        This function calculates the price of the energy.
        The more energy the people need and he less energy the bank has, the more expensive it would be.
        We also have to check the externalfactors and the weather
        """

        # External factors : a counter of disasters which increases the price
        disasters = externalFactors.value * 10
        externalFactors.value = 0
        # Attenuation factor :
        lamb = 0.99
        factor = PayableEnergyWanted / PayableEnergyBank

        return (price * lamb + disasters) * factor  # "NotReallyAccurateModel" (tm)

    class ExternalProcess(multiprocessing.Process):
        """
        This process sends signals to its parent randomly, simulating disasters.
        """

        def __init__(self):
            super().init()

        def run(self):
            time.sleep(400)
            x = random.random()
            if x > 0.99:
                os.kill(os.getppid(), signal.SIGINT)

    def handler(self, sig, frame):
        if sig == signal.SIGINT:
            with lockExternal:
                externalFactors.value += 1

    def interprete(self, restOrNeed, price, houseIdentifier ):
        """
        After the reception of a message through the message queue, we have to interprete it :
        Do the house need energy ? -> Do the globalneed needs to be increased ?
        Do the house give / sell energy ? Etc.
        Necessity to implement semaphores to protect energybank and globalneed values.
        value : (HouseIdentifier,RestOrNeed)
        """
        mqHouse = sysv_ipc.MessageQueue(houseIdentifier)        
        if restOrNeed < 0:  # The House NEEDS energy
            with lockGlobalNeed:
                GlobalNeed.value -= restOrNeed
            mqHouse.send(-1 * restOrNeed * price)  # We send to the house the price it has to pay for the energy.


        else:  # The house SELLS energy
            with lockPayable:
                PayableEnergyBank.value += restOrNeed[1]
            mqHouse.send(restOrNeed * price)  # We send to the house the money it earns selling the energy

    def run(self):

        external = self.ExternalProcess
        external.start()
        NumberOfThreads = 10
        
        price = 100 #Price at the beginning of the simulation
        
       
        #Message Passing definition : 


        
    
        while True:
            while self.mq.current_messages > 0 and Clock.Value == 0 : #While there is data sent by the houses.
                
                message, t = self.mq.receive()
                value = message.decode()     
                #Value : (HouseIdentifier,RestOrNeed)
                houseIdentifier = value[0]
                restOrNeed = value[1]
                thread = threading.Thread(target=self.interprete, args=(self, restOrNeed, price, houseIdentifier))
                thread.start()
                                
                with concurrent.futures.ThreadPoolExecutor(max_workers = NumberOfThreads) as executor: #Thread pool          
                    message, t = self.mq.receive()
                    value = message.decode() 
                    #Value : (HouseIdentifier,RestOrNeed)
                    
                    #We use a thread pool to interprete the messages of the message queue
                    for result in executor.map(self.interprete, (value[1],price,value[0])):
                        pass
                
                    
            
            if Clock.Value == 1 : #The value of the shared memory has been updated by the Clock : it is the turn of the Market to calculate its part 
                #We have to acquire all the locks :
                lockGlobalNeed.acquire()
                lockPayable.acquire()
                lockExternal.acquire()
            
                PayableEnergyWanted = GlobalNeed.value #We consider that the free energy is distributed equally to all the houses in need. They will have to pay for the rest
                price = self.priceCalculation(PayableEnergyWanted, PayableEnergyBank, externalFactors, price) #Using a linear model
    
                PayableEnergyBank.value, GlobalNeed.value = 0
                
                lockGlobalNeed.release()
                lockPayable.release()
                lockExternal.release()
                
                while Clock.Value == 0:
                    pass #Block 
