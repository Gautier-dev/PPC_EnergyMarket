import multiprocessing
import random
import sysv_ipc
from ast import literal_eval


class House(multiprocessing.Process):
    def __init__(self, i, Clock, Weather, LockMaison):
        super().__init__()
        self.i = i
        self.consommationFactor = random.random()
        self.productionFactor = random.random()
        self.lock = LockMaison

        p = random.random()

        if p < 0.1:
            Behavior = 1  # The house always give its energy surplus
        elif 0.1 <= p < 0.7:
            Behavior = 2  # The house give and sell if no takers
        else:
            Behavior = 3  # The house always sell its energy surplus

        self.Behavior = Behavior
        self.Money = random.gauss(3000, 1000)
        self.salary = random.gauss(2200, 700)
        self.clock = Clock
        self.weather = Weather
        self.SurplusOrNeed = 0
        self.MqHouse = sysv_ipc.MessageQueue(self.i, sysv_ipc.IPC_CREAT)

    def Production(self):
        return self.productionFactor * (self.weather[1] * 0.65)  # 0.65 = Energy production per hour of sunlight

    def consommation(self):
        return self.consommationFactor / self.weather[0]

    def run(self):
        client = sysv_ipc.MessageQueue(-2)  # to send messages to the House Queue
        while True:
            if self.clock == 1:  # The value of the shared memory has been updated by the Clock : it is the turn of the
                # Houses to calculate their part
                self.Money += self.salary / 30  # The house win money with the work of the family 
                created_energy = self.Production()
                self.SurplusOrNeed = created_energy - self.consommation()
                
                if self.SurplusOrNeed > 0 and self.Behavior != 3:
                    message = str((self.i, self.SurplusOrNeed)).encode()
                    client.send(message)  # Send its rest to the House Queue if giver
                    
                    #TODO : Update Surplus (sinon il va gagner de l'argent sur de l'énergie qu'il donne)                    
                    
                    while self.clock.value == 1:  # wait until the end of the day
                        pass
                else:
                    # receive energy from other houses
                    while self.clock.value == 1:
                        if self.SurplusOrNeed != 0:
                            msg = client.receive()
                            i, value = literal_eval(msg.decode())
                            if value > self.SurplusOrNeed:
                                message = str((i, value - self.SurplusOrNeed)).encode()
                                self.SurplusOrNeed = 0
                                self.lock.acquire()
                                client.send(message)
                                self.lock.release()
                            else:
                                
                                #TODO : gautier
                                
                                message = str((self.i, self.SurplusOrNeed - value)).encode()
                                self.lock.acquire()
                                client.send(message)
                                self.lock.release()

            if self.clock.value == 0:  # it's where the houses send surplus or need to the market
                
                client_market = sysv_ipc.MessageQueue(-1)
                if self.Behavior == 2 or self.Behavior == 3:
                    if self.SurplusOrNeed != 0:
                        client_market.send(self.SurplusOrNeed)
                
                while self.clock.value == 0:              
                    if client_market.current_messages > 0 :                    
                        message, t = client_market.receive()
                        value = message.decode()
                        self.Money = self.Money + value
                        while self.clock.value == 0: 
                            pass
