import multiprocessing

class House(multiprocessing.Process):
    def __init__(self, i, FacteurConsommation, FacteurProduction, Comportement, heritage, Salaire):
        super().__init__()
        self.i = i
        self.FacteurConsommation = FacteurConsommation
        self.FacteurProduction = FacteurProduction
        self.Comportement = Comportement
        self.heritage = heritage
        self.Salaire = Salaire

    def Production(self):
        pass

    def run(self):
        while True:
            if Clock.value == 1:  # The value of the shared memory has been updated by the Clock : it is the turn of the Houses to calculate their part
                Money += self.Salaire / 30  # The house win money with the work of the family
                Weather = Weather.Value  # The value of the shared memory has been updated by the Weather Process
                CreatedEnergy = Production(Weather)
                Rest = CreatedEnergy - Consommation
                SendMarket(HouseIdentifier, Rest,
                           Behavior)  # We send to the market, via Message queues, the data of the house
                while Clock.Value == 1:
                    pass  # Block until this is the turn of the other process to compute

            if Reception_Message_Market:
                Money += GainOrLoss  # We update the income / outcome due to the energy market.

            if Clock.value == 0:
                pass