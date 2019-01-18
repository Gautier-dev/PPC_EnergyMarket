# -*- coding: utf-8 -*-

"""
EACH TRANSACTION IS PERFORMED ON THE NIGHT
NIGHT : ONLY THE CALCULATION OF THE PRICE
"""


import multiprocessing
import threading
import sysv_ipc
import signal
import ast
import External



class Market(multiprocessing.Process):
    """
    Class defining the Market process.
    n = number of houses
    Father of the External Process.
    While the Clock.Value is equal to 1, it receives all the data of the houses.
    It increments energy banks and updates an array representing the need of all the houses.
    When the Clock.Value is equal to 0, it calculates the price of the energy and tell the houses what they have to pay to receive it.
    """
    
    def __init__(self, externalFactors, lockExternal, globalNeed, lockGlobalNeed, payableEnergyBank, lockPayable,
                 clocker, weather, child_conn):
        super().__init__()
        self.mq = sysv_ipc.MessageQueue(-1, sysv_ipc.IPC_CREAT)  #init message queue of the market
        self.firstTime = 1 #Boolean : 1 = first time used, we don't have to calculate the price of the energy
        
        #Shared memory pointers
        self.externalFactors = externalFactors #Shared memory counting the disasters that can affect the energy price
        self.globalNeed = globalNeed #Shared memory counting how much energy the houses need
        self.energyBank = payableEnergyBank #Shared memory counting how much energy the houses give 
        self.clock = clocker #Shared memory : 0 = night, 1 = day
        self.weather = weather #Shared memory giving the weather
        
        #Lock pointers
        self.lockExternal = lockExternal
        self.lockGlobalNeed = lockGlobalNeed
        self.lockPayable = lockPayable
        
        #Pipe
        self.pipe = child_conn

    def priceCalculation(self, PayableEnergyWanted, PayableEnergyBank, externalFactors, price):
        """
        This function calculates the price of the energy.
        The more energy the people need and he less energy the bank has, the more expensive it would be.
        We also have to check the externalFactors and the weather
        """
        
        # External factors : a counter of disasters which increases the price
        disasters = externalFactors * 10
        # Attenuation factor :
        lamb = 0.99
        if PayableEnergyBank == 0:
            PayableEnergyBank = 1
        
        if PayableEnergyWanted == 0:
            factor = 1/2
        else:
            factor = (PayableEnergyWanted / PayableEnergyBank)
        
        return (price * lamb + disasters + factor)  # "NotReallyAccurateModel" (tm)


    def handler(self, sig, frame):
        if sig == signal.SIGINT:
            with self.lockExternal:
                self.externalFactors.value += 1

    def interprete(self, restOrNeed, price, houseIdentifier ):
        """
        After the reception of a message through the message queue, we have to interprete it :
        Do the house need energy ? -> Do the globalneed needs to be increased ?
        Do the house give / sell energy ? Etc.
        Necessity to implement semaphores to protect energybank and globalneed values.
        value : (HouseIdentifier,RestOrNeed)
        """
        mqHouse = sysv_ipc.MessageQueue(houseIdentifier)        
        message = str(restOrNeed * price).encode()
        mqHouse.send(message)  # We send to the house the price it has to pay for the energy.
        if restOrNeed < 0:  # The House NEEDS energy
            with self.lockGlobalNeed:
                self.globalNeed.value -= restOrNeed
        else:  # The house SELLS energy
            with self.lockPayable:
                self.energyBank.value += restOrNeed

    def run(self):
        external = External.externalProcess()
        signal.signal(signal.SIGINT, self.handler) #associate the SIGINT signal to the handler
        print("start external")
        external.start()

        
        price = 100 #Price at the beginning of the simulation
            
    
        while True:
            #  print("message restant MQ Market : ", self.mq.current_messages)
            while self.mq.current_messages > 0 and self.clock.value == 0: #While there is data sent by the houses.
                message, t = self.mq.receive()
                value = ast.literal_eval(message.decode())
                #Value : (HouseIdentifier,RestOrNeed)
                houseIdentifier = value[0]
                restOrNeed = value[1]
                thread = threading.Thread(target=self.interprete, args=(restOrNeed, price, houseIdentifier))
                thread.start()
                    
            #  print("Clock recupere dans market : ", self.clock.value)
            
            if self.clock.value == 1:  #  The value of the shared memory has been updated by the Clock : it is the turn
                # of the Market to calculate its part
                if self.firstTime == 1:
                    self.firstTime = 0
                else:
                    #  We have to acquire all the locks :
                    self.lockGlobalNeed.acquire()
                    self.lockPayable.acquire()
                    self.lockExternal.acquire()

                    #  These values are just information about a given day
                    payableEnergyWanted = self.globalNeed.value
                    totalPrice = price * payableEnergyWanted

                    price = self.priceCalculation(payableEnergyWanted, self.energyBank.value, self.externalFactors.value, price) #Using a linear model
                    
                    #  Print information
                    result = [str(price), str(self.externalFactors.value), str(totalPrice)]
                    print("The price of the energy is : {}.\nThe number of disasters which occured today is : {}.\nThe "
                          "price of the energy for the whole community is : {}.\n".format(result[0], result[1], result[2]))
                    #  self.pipe.send(display)

                    #  Reset of these values everyday
                    self.energyBank.value, self.globalNeed.value, self.externalFactors.value = 0, 0, 0
                    
                    self.lockGlobalNeed.release()
                    self.lockPayable.release()
                    self.lockExternal.release()
                
                while self.clock.value == 1:
                    pass #Block 
