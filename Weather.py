from random import random, gauss

def weather():
    '''Update weather state in the shared memory'''
    temperature, type_of_weather = current_weather_in_shared_memory
    ensoleillement = 0
    return (fonction_meteo_selon_data(t), 4* random(), ensoleillement)


def fonction_meteo_selon_data(t):
    pass

