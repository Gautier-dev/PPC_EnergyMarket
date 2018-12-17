from random import random, gauss

def weather():
    '''Update weather state in the shared memory
    return temperature, weather state, '''
    temperature, type_of_weather = current_weather_in_shared_memory
    sunlight = fct_sunlight(t)  # return sunlight according to the day the clock is at
    Array.Value = [Temp_function(t), 4*random(), sunlight]


def Temp_function(t, data):
    '''return new temperature according to the day temperature of a weather station stored in data'''
    return data[t]

