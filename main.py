# -*- coding: utf-8 -*-

import multiprocessing
import threading
import Market
import Clock
import House
import Weather
import sysv_ipc

if __name__ == "__main__":
    
    ###THE CONCEPT
    """
    Based on a "Day/night" cycle. It is defined by the Clock process.
    There is a lot of houses, defined by the House processes, and a Market process.
    The Market Process creates an External process.
    The Weather Process is used to know how much energy the houses create (with the enlightment factor)...
    ... and use (with the temperature factor).
    
    On the Day (Clock.value = 1) :
    The HOUSES calculate their energy consommation and production.
    The HOUSES THAT WANT TO GIVE ENERGY communicate, through the message queue "messageQueueHouses", the energy they want to give.
    The HOUSES THAT WANT TO RECEIVE ENERGY are picking messages from the message queue (first arrived, first served), and send a message through the giver private message queue.
    The HOUSES THAT GIVES ENERGY adapt the amount of energy they have.
    The MARKET calculates the price of the energy if this is not the first day.
    
    On the Night (Clock.value = 0) :
    The HOUSES send to the market their energy need OR their extra energy amount.
    The MARKET sends to the houses the money they have to pay OR the money they earn.
    
    Everytime :
    The EXTERNAL process can, at any moment, signal a disaster to the market.
    The MAIN process deliver the user some data to follow the evolution of the events.
    
    """
                
    ###SHARED VALUES AND LOCKS

    externalFactors = multiprocessing.Value('i',0) #This is a counter of the disasters that occurs sometimes (used by the market and the external processes) (initialisation)    
    lockExternal = multiprocessing.Lock() #Protection
            
    globalNeed = multiprocessing.Value('i',0) #Energy wanted by the houses (used by the Market process) (initialisation)
    lockGlobalNeed = threading.Lock() #Protection
        
    payableEnergyBank = multiprocessing.Value('i',0) #Energy given by the houses (used by the Market process) (initialisation)
    lockPayable = threading.Lock() #Protection
    
    clocker = multiprocessing.Value('i',1) #The clock is a shared variable : 0 = night, 1 = day
    
    weather = multiprocessing.Array('i', [0,0]) #The weather is a shared array
    
    day = multiprocessing.Value('i', 0) #The date of today
    
    
    ###COMMUNICATION
    
    messageQueueHouse = sysv_ipc.MessageQueue(-2, sysv_ipc.IPC_CREAT) #Message queue used by all the houses.
    #This message queue contains the "gifts" of energy. The one which is given and not payable.
    lockHouse = multiprocessing.Lock()#Protection
    
    parent_conn, child_conn = multiprocessing.Pipe() #Création of the pipe between main process and Market Process.
    #The pipe will allow to display data about the simulation.



    ###MAIN

    
    numberOfHouses = 100    
    
    marketProcess = Market(externalFactors,lockExternal,globalNeed,lockGlobalNeed,payableEnergyBank,lockPayable,clocker,weather)
    marketProcess.start()
    
    weatherProcess = Weather(weather,clocker,day)
    weatherProcess.start()
    
    houses = [House(i,clocker,weather,lockHouse) for i in range (1,numberOfHouses+1)]
    [a.start() for a in houses]
    
    tickProcess = Clock(clocker)
    tickProcess.start()
    
    while True :
        if clocker.value == 0 :
            while messageQueueHouse.current_message > 0:
                _,_ = messageQueueHouse.receive() #The "gifts" list have to be empty for the next day. The houses which want to sell their energy will answer the Market process by themselves.
            
            print("--NIGHT--")

            while clocker.value == 0 :
                pass
        
        if clocker.value == 1 :
            
            print("--DAY--")            
            
            print(parent_conn.recv())   #The parent process receive a message from the Market Process and prints it, using the "parent connection"
            
            while clocker.value == 1 :
                pass
