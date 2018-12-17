# -*- coding: utf-8 -*-

def Market(n):
    """
    Function defining the Market process.
    Father of the External Process.
    While the Clock.Value is equal to 1, it receives all the data of the houses.
    It increments energy banks and updates an array representing the need of all the houses.
    When the Clock.Value is equal to 0, it calculates the price of the energy and tell the houses what they have to pay to receive it.
    """
    
    ExternalProcessLaunch()
    GlobalNeed = 0 #Energy wanted by the house (initialised)
    NeedArray = [] #Will reference all the houses and their need (initialised)
    PayableEnergyBank = 0 #(initialised)
    FreeEnergyBank = 0 #(initialised)
    NumberOfHomes = n
    while True :
        if Reception_Message_House : #Everytime an house transmit its data
            if HouseNeedsEnergy : 
                GlobalNeed += HouseNeed
                NeedArray.append((HouseIdentifier,HouseNeed))
                
            elif HouseGivesEnergy :
                FreeEnergyBank += HouseEnergy
                
            elif HouseSellsEnergy :
                PayableEnergyBank += HouseEnergy
        
        if Clock.Value == 0 : #The value of the shared memory has been updated by the Clock : it is the turn of the Market to calculate its part 
            PayableEnergyWanted = GlobalNeed - FreeEnergyBank #We consider that the free energy is distributed equally to all the houses in need. They will have to pay for the rest
            FreeEnergyPerHouse = FreeEnergyBank / NumberOfHomes
            Price = PriceCalculation(PayableEnergyWanted, PayableEnergyBank, ExternalFactors, Price) #Using a linear model
            for house in NeedArray:
                EnergyNeed = EnergyNeed - FreeEnergyPerHouse #Free Energy given to the house
                PriceForThisHouse = Calculation(EnergyNeed,Price) 
                SendToHouse(PriceForThisHouse) #Communication by Message queues
            PayableEnergyBank, FreeEnergyBank = 0
            NeedArray = []
            GlobalNeed = 0
            
            while Clock.Value == 0 :
                pass  #Block 

        
        if Reception_Signal_External : #Handler : we receive a signal from this process
            impact(ExternalFactors)
            
