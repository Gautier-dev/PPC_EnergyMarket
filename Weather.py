# -*- coding: utf-8 -*-
import random
import multiprocessing

jour = multiprocessing.Value('i', 0)
Weather = multiprocessing.Array('i', [0, 0])

class weather(multiprocessing.Process, Weather):
    """
    Update weather state in the shared memory.
    return temperature, weather state: (1 sunny, 2 cloudy, 3 rain, 4 snow), sunlight
    """
    def __init__(self, t):
        super().__init__()
        self.t = t



    def Temp_function(self):
        """
        return new temperature according to the day temperature of a weather station stored in data
        """
        DataTemp = [[3.3, 0.7, 6], [4.2, 1.2, 7.3], [7.8, 3.4, 12.2], [10.8, 5.8, 15.9],
                    [14.3, 8.9, 19.8], [17.5, 12.1, 22.9], [19.4, 14.1, 24.8], [19.1, 13.9, 24.3],
                    [16.4, 11.5, 21.3], [11.6, 7.6, 15.7], [7.2, 4.3, 10.1], [4.2, 1.8, 6.7]]
        jour_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for k in range(12):
            cumule = 0
            for i in range(k):
                cumule += jour_mois[k]
            if cumule < self.t <= cumule + jour_mois[k]:
                ecart_type = min(abs(DataTemp[k][0] - DataTemp[k][1]), abs(DataTemp[k][0] - DataTemp[k][2]))
                v = random.gauss(DataTemp[k][1], ecart_type)
                while (v > DataTemp[k][2]) and (v < DataTemp[k][1]):
                    v = random.gauss(DataTemp[k][1], ecart_type)
                return v


    def sunlight(self):
        Data = [62.5, 79.2, 128.9, 166, 193.8, 202.1, 212.2, 212.1, 167.9, 117.8, 67.7, 51.4]
        jour_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for k in range(12):
            cumule = 0
            for i in range(k):
                cumule += jour_mois[k]
            if cumule < self.t <= cumule + jour_mois[k]:
                ecart_type = 0.15 * Data[k]
                v = random.gauss(Data[k], ecart_type)
                while (v > 16) and (v < 2):
                    v = random.gauss(Data[k], ecart_type)
                return v


    def run(self):
        if Clock.value == 0:
            jour.value = jour + 1
            Weather[0] = self.Temp_function()  # Updates the shared memory for all the processes.
            Weather[1] = self.sunlight()
            while Clock.Value == 0:
                pass


