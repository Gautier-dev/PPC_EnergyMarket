import multiprocessing
import random
import sysv_ipc


class House(multiprocessing.Process):
    def __init__(self, i, Clock, Weather, LockMaison):
        super().__init__()
        self.i = i
        self.consommationFactor = random.random()
        self.productionFactor = random.random()
        self.lock = LockMaison

        p = random.random()

        if p < 0.1:
            Comportement = 1
        elif 0.1 <= p < 0.7:
            Comportement = 2
        else:
            Comportement = 3

        self.Comportement = Comportement
        self.argent = random.gauss(3000, 1000)
        self.Salaire = random.gauss(2200, 700)
        self.clock = Clock.value
        self.weather = Weather.value
        self.rest = 0
        self.MqHouse = sysv_ipc.MessageQueue(self.i, sysv_ipc.IPC_CREAT)

    def Production(self):
        return self.productionFactor * (self.weather[1] * 0.65) # 0.65 = production d ernergie par heure d ensoleillement

    def consommation(self):
        return self.consommationFactor / self.weather[0]



    def run(self):
        while True:

            if self.clock == 1:  # The value of the shared memory has been updated by the Clock : it is the turn of the Houses to calculate their part
                self.argent += self.Salaire / 30  # The house win money with the work of the family
                 # The value of the shared memory has been updated by the Weather Process
                CreatedEnergy = self.Production()
                self.rest = CreatedEnergy - self.consommation()
                client = sysv_ipc.MessageQueue(-2)
                if self.rest > 0 and self.Comportement != 3:
                    message = str((self.i, self.rest)).encode()
                    client.send(message)
                    while self.clock == 1:
                        pass
                else:
                    while self.clock.Value == 1:
                        if self.rest != 0:

                            i, value = client.receive()
                            if value > self.rest:
                                message = str((i, value - self.rest)).encode()
                                self.lock.acquire()
                                client.send(message)
                                self.lock.release()
                            else:
                                if self.Comportement != 3:
                                    message = str((self.i, self.rest - value)).encode()
                                    client.send(message)


            if self.clock.value == 0:

                clientMarket = sysv_ipc.MessageQueue(-1)
                if self.Comportement == 2 or self.Comportement == 3:
                    if self.rest != 0:
                        clientMarket.send(self.rest)
                message, t = clientMarket.receive()
                value = message.decode()
                self.argent = self.argent + value





