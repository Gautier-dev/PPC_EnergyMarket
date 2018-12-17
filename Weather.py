# -*- coding: utf-8 -*-

from random import random, gauss

def weather():
    '''Update weather state in the shared memory
    return temperature, weather state 1 sunny 2 cloudy 3 rain 4 snow, sunlight '''
    t = getDayInSharedMemory()
    sunlight = fct_sunlight(t)  # return sunlight according to the day the clock is at
    Array.Value = [Temp_function(t), 4*random(), sunlight]


def Temp_function(t, data):
    '''return new temperature according to the day temperature of a weather station stored in data'''
    return data[t]

