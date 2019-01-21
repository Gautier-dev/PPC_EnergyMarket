# PPC_EnergyMarket
 Based on a "Day/night" cycle. It is defined by the Clock process.
    There is a lot of houses, defined by the House processes, and a Market process.
    The Market Process creates an External process.
    The Weather Process is used to know how much energy the houses create thanks to  hours of sunlight per day and use thanks to the temperature.
    The temperature and sunlight used by the Weather Process is based on real data from Paris.
    
    During the Day (Clock.value = 1) :
    The HOUSES calculate their energy consommation and production.
    The HOUSES THAT WANT TO GIVE ENERGY communicate, through the message queue "messageQueueHouses", the energy they want to give.
    The HOUSES THAT WANT TO RECEIVE ENERGY are picking messages from the message queue (first arrived, first served), and send a message through the giver private message queue.
    The HOUSES THAT GIVES ENERGY adapt the amount of energy they have.
    The MARKET calculates the price of the energy if this is not the first day.
    
    During the Night (Clock.value = 0) :
    The HOUSES send to the market their energy need OR their extra energy amount.
    The MARKET sends to the houses the money they have to pay OR the money they earn.
    
    At anytime :
    The EXTERNAL process can, at any moment, signal a disaster to the market.
    The MAIN process deliver the user some data to follow the evolution of the events.

# Instructions 
 - Extract the archive.
 - Download the modules matplotlib.pyplot, ast and sysv_ipc (you need to run on a Linux machine !) .
 - Run the main.py program.
 You will be able to see how the simulation goes.
 - To end the simulation, interrupt the program by pressing ctrl + C.
