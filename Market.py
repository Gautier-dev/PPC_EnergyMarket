# -*- coding: utf-8 -*-

def Market():
    BesoinGlobal = 0 #Energie demandée par les maisons   
    TableauBesoin = [] #Référencera chaque maison et son besoin en énergie
    Banque_Energie_Payante = 0 #Stockage d'énergie à vendre
    Banque_Energie_Gratuite = 0 #Stockage d'énergie à donner
    while True :
        if Reception_Message_Maison :
            if Maison_Besoin_D_Energie :
                BesoinGlobal += BesoinMaison
                TableauBesoin.append((maison,BesoinMaison))
                
            elif Maison_Donne_Energie :
                Besoin_Energie_Gratuite += EnergieMaison
                
            elif Maison_Vend_Energie :
                Besoin_Energie_Payante += EnergieMaison
        
        if Clock2_Tick:
            Demande_D_Energie_Payante = BesoinGlobal - Banque_Energie_Gratuite
            Prix = CalculPrix(Demande_D_Energie_Payante, Banque_Energie_Payante, Facteurs_Extérieurs, Prix)
            #Plus le rapport demande/banque est haut, plus le prix est élevé.
            #Dans le cas où il n'y a simplement pas assez d'énergie, on considère que le prix augmente drastiquement.
            Prix_Du_Joul = Prix/Demande_D_Energie_Payante
            for maison in TableauBesoin:
                Prix_De_Son_Energie = maison[1]*Prix_Du_Joul
                Envoyer_Maison(Prix_De_Son_Energie)
            Banques = 0
            TableauBesoin = []
            BesoinGlobal = 0
        
        if Reception_Signal_External :
            impacter(Facteurs_Exterieurs)
            
