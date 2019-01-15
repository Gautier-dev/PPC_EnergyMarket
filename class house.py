import multiprocessing

Clock = multiprocessing.Value('i',1) #Définition de la shared memory

tick = ClockTick(Clock)
tick.start()

class House(multiprocessing.Process):
    def __init__(self, i, FacteurConsommation, FacteurProduction, Comportement, argent, Salaire):
        super().__init__()
        self.i = i
        self.FacteurConsommation = FacteurConsommation
        self.FacteurProduction = FacteurProduction
        self.Comportement = Comportement
        self.argent = argent
        self.Salaire = Salaire
        self.clock = Clock.value
        self.weather = Weather.value

    def Production(self):
        return self.FacteurProduction * self.weather
    def consommation(self):
        return 0  #TODO

    def SendHouses(self, rest):

        message = str(rest).encode()
        MessageQueueHouse.send(message)


    def run(self):
        while True:
            if self.clock == 1:  # The value of the shared memory has been updated by the Clock : it is the turn of the Houses to calculate their part
                self.argent += self.Salaire / 30  # The house win money with the work of the family
                 # The value of the shared memory has been updated by the Weather Process
                CreatedEnergy = self.Production()
                Rest = CreatedEnergy - self.consommation()
                self.SendHouses(Rest)  # We send to the market, via Message queues, the data of the house
                while Clock.Value == 1:
                    pass  # Block until this is the turn of the other process to compute

            if demande_fini:
                echange()




            if Reception_Message_Market:
                Money += GainOrLoss  # We update the income / outcome due to the energy market.

            if Clock.value == 0:
                MqHouse = sysv_ipc.MessageQueue(self.i, sysv_ipc.IPC_CREAT)
                message, t = MqHouse.receive()
                value = message.decode()
                self.argent = self.argent - value




