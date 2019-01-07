# -*- coding: utf-8 -*-

def House(i):
    """
    The function defining the "house" type process.
    It is defined randomly, using statistics (ex : 10% ~ of the houses will have a "always give" behavior, an income upper than 3000€ ...) 
    When the clock Value is at 1, it calculates its production and consommation, then sends it to the Market.
    When it receives a message from the market, its updates its "money".
    """
    HouseIdentifier = i
    Consommation, Behavior, Money, IncomePerMonth = Randomisation() #We will randomise, using statistics ressources, the data of the house.
    while True: 
        if Clock.Value == 1: #The value of the shared memory has been updated by the Clock : it is the turn of the Houses to calculate their part
            Money += IncomePerMonth/30 #The house win money with the work of the family
            Weather = Weather.Value #The value of the shared memory has been updated by the Weather Process
            CreatedEnergy = Production(Weather)
            Rest = CreatedEnergy - Consommation
            SendMarket(HouseIdentifier, Rest, Behavior) #We send to the market, via Message queues, the data of the house
            while Clock.Value == 1:
                pass #Block until this is the turn of the other process to compute
        
        if Reception_Message_Market :
            Money += GainOrLoss #We update the income / outcome due to the energy market.
