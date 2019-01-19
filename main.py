# -*- coding: utf-8 -*-

import multiprocessing
import threading
import Market
import Clock
import House
import Weather
import sysv_ipc
import matplotlib.pyplot

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

    externalFactors = multiprocessing.Value('i', 0) #This is a counter of the disasters that occurs sometimes (used by the market and the external processes) (initialisation)
    lockExternal = multiprocessing.Lock() #Protection
            
    globalNeed = multiprocessing.Value('f', 0) #Energy wanted by the houses (used by the Market process) (initialisation)
    lockGlobalNeed = threading.Lock() #Protection
        
    payableEnergyBank = multiprocessing.Value('f', 0) #Energy given by the houses (used by the Market process) (initialisation)
    lockPayable = threading.Lock() #Protection
    
    clocker = multiprocessing.Value('i', 1) #The clock is a shared variable : 0 = night, 1 = day
    
    weather = multiprocessing.Array('f', [3.3, 62.5/31]) #The weather is a shared array
    
    day = multiprocessing.Value('i', 1) #The date of today

    numberOfHouses = 10
    
    
    ###COMMUNICATION
    
    messageQueueHouse = sysv_ipc.MessageQueue(-2, sysv_ipc.IPC_CREAT) #Message queue used by all the houses.
    #This message queue contains the "gifts" of energy. The one which is given and not payable.
    lockHouse = multiprocessing.Lock()#Protection

    # The pipes will allow to display data about the simulation.

    #  Market pipe
    main_conn_market, market_conn = multiprocessing.Pipe() #Création of the pipe between main process and Market Process.

    #  houses pipe
    houses_pipes = [multiprocessing.Pipe() for i in range(numberOfHouses)]


    ###MAIN

    

    
    marketProcess = Market.Market(externalFactors, lockExternal, globalNeed, lockGlobalNeed, payableEnergyBank, lockPayable, clocker, weather, market_conn)
    print("Starting market")
    marketProcess.start()
    
    weatherProcess = Weather.Weather(weather, clocker, day)
    print("Starting weather")
    weatherProcess.start()
    
    houses = [House.House(i, clocker, weather, lockHouse, houses_pipes[i][1]) for i in range(numberOfHouses)]
    print("Starting every Houses")
    for k in houses:
        k.start()
    
    tickProcess = Clock.Clock(clocker)
    print("Starting the clock")
    tickProcess.start()
    
    firstTime = True #Used for the first day (the market isn't up)

    # For the graph
    dayG = []
    priceG = []

    housesG = [[] for k in range(numberOfHouses)]
    
    while True:
        if clocker.value == 0:
            
            print("--NIGHT--")

            while messageQueueHouse.current_messages > 0:
                _, _ = messageQueueHouse.receive()  # The "gifts" list have to be empty for the next day. The houses which want to sell their energy will answer the Market process by themselves.

            print("values for the day {} : temperature will be {:.3} and it will have {:.3} hours of sunlight".format(day.value, weather[0], weather[1]))

            while clocker.value == 0:
                pass
        
        if clocker.value == 1:
            
            print("--DAY--")

            if not (firstTime):

                #  The main process receive a message from the different Processes and prints it, using the "parent connection"
                result_market = main_conn_market.recv()

                print("The price of the energy is : {}.\nThe number of disasters which occured today is : {}.\nThe "
                      "price of the energy for the whole community is : {}.\n".format(result_market[0],
                                                                                      result_market[1],result_market[2]))

                for k in range(numberOfHouses):
                    tab = houses_pipes[k][0].recv()
                    print("House {} has {:.6}$, an income of {:.6}$ and an energy balance of {}"
                          .format(tab[0], tab[1], tab[2], tab[3]))
                    housesG[k].append(tab[1])
                dayG.append(day.value)
                priceG.append(result_market[0])

                matplotlib.pyplot.clf()
                matplotlib.pyplot.subplot(121)
                matplotlib.pyplot.title("values for the day {} : temperature will be {:.3} and it will have {:.3} hours of sunlight".format(day.value, weather[0], weather[1]))
                matplotlib.pyplot.plot(dayG, priceG, 'r--')
                matplotlib.pyplot.subplot(122)
                matplotlib.pyplot.title("houses")
                matplotlib.pyplot.plot(dayG, housesG[0], 'r', dayG, housesG[1], 'b', dayG, housesG[2], 'y')  #todo toutes les maisons

                matplotlib.pyplot.show()

            else:
                firstTime = False





            while clocker.value == 1:
                pass




