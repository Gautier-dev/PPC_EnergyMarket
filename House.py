import multiprocessing
import random
import sysv_ipc
from ast import literal_eval


class House(multiprocessing.Process):
    def __init__(self, i, Clock, Weather, LockMaison, pipe):
        super().__init__()
        self.i = i
        self.EnergyBalance = 0

        #Randomisation of the house (income, consommation, production...)
        person = random.gauss(2, 1)
        while person < 0:
            person = random.gauss(2, 1)
        self.Number_of_People = person

        #houses have 5 m2 of solar panels on average
        area = random.gauss(6, 5)
        while area < 0:
            area = random.gauss(6, 5)
        self.area_of_solar_panels = area
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
        self.income = random.gauss(2200, 700)
        
        #Pointers of the shared memories
        self.clock = Clock
        self.weather = Weather

        #  pipe to send information to the main
        self.pipe = pipe

        
        #Message queue of the house
        self.MqHouse = sysv_ipc.MessageQueue(self.i, sysv_ipc.IPC_CREAT)

    def Production(self):
        #  In theory, 1 m2 receive 1kw
        prod = self.area_of_solar_panels * self.weather[1]  # number of kwh produced
        return prod
        
    def consommation(self):
        """
        We assume people don't have Air conditioning when it's too hot. Each person consume 3kwh on average and
        average temp at paris is 11. We assume that when temperature is above 25, each person consumes 0.5 kwh
        :return: a value that is inversely proportional to temperature
        """
        if self.weather[0] > 25:
            return 0.5 * self.Number_of_People
        else:
            return (5 - 0.18 * self.weather[0]) * self.Number_of_People



    def run(self):
        client = sysv_ipc.MessageQueue(-2)  # to send messages to the House Queue : the gifts of free energy
        client_market = sysv_ipc.MessageQueue(-1) #to send messages to the market : the payable energy
        while True:
            
            # print("Clock recupere dans house : ", self.clock.value)
            if self.clock.value == 1:  # The value of the shared memory has been updated by the Clock : it is the turn of the houses to calculate their part

                self.Money += self.income / 30  # The house win money with the work of the family
                self.EnergyBalance = self.Production() - self.consommation()
                #   alert the main process that it needs to print data now
                self.pipe.send([self.i, self.Money, self.income, self.EnergyBalance])
                
                if self.EnergyBalance > 0 and self.Behavior != 3:
                    #Give Energy to other houses if we want to give it.
                    message = str((self.i, self.EnergyBalance)).encode()
                    message.decode()
                    client.send(message)  # Send its rest to the House Queue if giver
                    
                    while self.clock.value == 1 :
                        #If someone take some energy : we have to change the value of SurplusOrNeed
                        if self.MqHouse.current_messages != 0:
                            message, t = self.MqHouse.receive()
                            value = message.decode()
                            self.EnergyBalance -= float(value)
                

                else:
                    # receive energy from other houses
                    while self.clock.value == 1:
                        if self.EnergyBalance < 0 and client.current_messages > 0 :
                            self.lock.acquire()
                            msg, t = client.receive()
                            self.lock.release()
                            i, value = literal_eval(msg.decode())  # The house i can give the amount of energy value
                            
                            #There is more energy than needed / just enough
                            if value >= self.EnergyBalance:
                                self.EnergyBalance = 0
                                #Update of the "offer" in the global queue :                                
                                message = str((i, value - self.EnergyBalance)).encode()
                                
                                #The locking is disabled due of deadlocks : we consider that the "giver" does not have to wait to acquire the lock.
                                #self.lock.acquire()
                                client.send(message)
                                #self.lock.release()
                                
                                #We say to the house identified by "i" that we have taken some energy.
                                message = str(value).encode()
                                thankYou = sysv_ipc.MessageQueue(i)
                                thankYou.send(message)
                                #The while loop will happen and just pass until the clock value changes.
                                
                            #There is not enough energy
                            else:
                                self.EnergyBalance = 0
                                #No need to send another message to the global queue : all the energy given is used
                                #We say to the house identified by "i" that we have taken some energy.
                                message = str(value).encode()
                                thankYou = sysv_ipc.MessageQueue(i)
                                thankYou.send(message)
                                #The "while" loop will happen another time, to try to receive enough energy.


            if self.clock.value == 0:  # it's where the houses send surplus or need to the market
                
                #Sending the message
                if self.Behavior == 2 or self.Behavior == 3:
                    if self.EnergyBalance != 0:
                        message = str((self.i, self.EnergyBalance)).encode()
                        client_market.send(message)
                
                #Waiting for the money / the bill.
                while self.clock.value == 0:              
                    if self.MqHouse.current_messages > 0:
                        message, t = self.MqHouse.receive() #The market sends the data to the Mq of the house
                        value = float(message.decode())
                        self.Money = self.Money + value
                        if self.Money < 0:
                            print("House {} does not have money anymore ! Giving it 500 $.".format(self.i))
                        while self.clock.value == 0: 
                            pass
