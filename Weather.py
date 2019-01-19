# -*- coding: utf-8 -*-
import random
import multiprocessing

class Weather(multiprocessing.Process):
    """
    Update weather state and day in the shared memory.
    Compute temperature and sunlight
    """
    def __init__(self, Weather, Clock, day):
        super().__init__()
        self.day = day
        self.weather = Weather
        self.clock = Clock



    def Temp_function(self):
        """
        return new temperature according to data from the city of Paris
        """
        DataTemp = [[3.3, 0.7, 6], [4.2, 1.2, 7.3], [7.8, 3.4, 12.2], [10.8, 5.8, 15.9],
                    [14.3, 8.9, 19.8], [17.5, 12.1, 22.9], [19.4, 14.1, 24.8], [19.1, 13.9, 24.3],
                    [16.4, 11.5, 21.3], [11.6, 7.6, 15.7], [7.2, 4.3, 10.1], [4.2, 1.8, 6.7]]
        NumberDayMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for k in range(12):
            add_day_up = 0
            for i in range(k):
                add_day_up += NumberDayMonth[k]
            if add_day_up < self.day.value <= add_day_up + NumberDayMonth[k]:
                standard_deviation = min(abs(DataTemp[k][0] - DataTemp[k][1]), abs(DataTemp[k][0] - DataTemp[k][2]))
                #  Generate a value according to a Normal distribution around the mean
                v = random.gauss(DataTemp[k][1], 0.3*standard_deviation)
                while (v > DataTemp[k][2]) and (v < DataTemp[k][1]):
                    v = random.gauss(DataTemp[k][1], 0.3*standard_deviation)
                return v


    def sunlight(self):
        """

        :return: number of hours of sunlight in a given day. Data from Paris
        """
        Data = [62.5, 79.2, 128.9, 166, 193.8, 202.1, 212.2, 212.1, 167.9, 117.8, 67.7, 51.4]
        NumberDayMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for k in range(12):
            add_day_up = 0
            for i in range(k):
                add_day_up += NumberDayMonth[k]
            if add_day_up < self.day.value <= add_day_up + NumberDayMonth[k]:
                hours_per_day = Data[k]/NumberDayMonth[k]
                #  Generate a value according to a Normal distribution around the mean
                standard_deviation = 0.15 * hours_per_day
                v = random.gauss(hours_per_day, standard_deviation)
                while (v > 16) and (v < 0):
                    v = random.gauss(Data[k], standard_deviation)
                return v


    def run(self):
        """

        :return: run the process : change the day, temperature, sunlight according to the clock

        """
        while True:
            if self.clock.value == 0:
                self.day.value += 1  # change the day
                if self.day.value > 365:
                    self.day.value = 1
                self.weather[0] = self.Temp_function()  # Updates the shared memory for all the processes.
                self.weather[1] = self.sunlight()
                #print(self.day.value, self.weather[0], self.weather[1])
                while self.clock.value == 0:
                    pass


