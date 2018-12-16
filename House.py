# -*- coding: utf-8 -*-

def Maison(i):
    NumeroMaison = i
    Consommation, Comportement, Argent = Randomisaton()
    while True:
        if Clock1_Tick :
            Weather = ObtenirValeurWeather()
            EnergieProduite = Production(Weather)
            Resultante = EnergieProduite - Consommation
            EnvoiMarket(NumeroMaison,Resultante,Comportement)
        
        if Reception_Message_Market :
            Argent += GainOuPerteParVenteOuAchat
            
        
