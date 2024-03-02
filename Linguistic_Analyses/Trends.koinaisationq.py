# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 16:13:32 2021

@author: Elisa
"""
#==============================================================================
#    Koinaization (Trends Analyses) - the /q/ realization
#==============================================================================

# ----------------------------------------------------------------------------------------------------
# |                      DATA INFORMATION                                                            |
# -------------------------------------------------------------------------
# | This script is set to work on the tarc data totality (file tarc.tsv)  |
# -------------------------------------------------------------------------
import pandas as pd 
import matplotlib.pyplot as plt
path1 = r""
from scipy.stats import chi2_contingency


def upload(filename="", path = path1, end= 38918, rap = False):
    tsv = path+filename
    df = pd.read_csv(tsv, sep="\t", encoding='utf-8').astype(str)
    if rap: #only rap data
        date = list(df['data'][end:])
        words = list(df['CODA'][end:])  
        ara = list(df['arabish'][end:]) 
        toks = list(df['token'][end:])
        pos = list(df['pos'][end:])
        tipo = list(df['TYPE'][end:])
        loc = list(df['governorate'][end:])
        age = list(df['age'][end:])
        gend = list(df['gender'][end:])
    else : #evrything except rap data
        date = list(df['data'][:end])
        words = list(df['CODA'][:end])  
        ara = list(df['arabish'][:end]) 
        toks = list(df['token'][:end])
        pos = list(df['pos'][:end])
        tipo = list(df['TYPE'][:end])
        loc = list(df['governorate'][:end])
        age = list(df['age'][:end])
        gend = list(df['gender'][:end])
          
    return df, date, words, ara, pos, toks, tipo, loc, age, gend 
        
df, date, words, ara, pos, toks, tipo, loc, age, gend  = upload(filename = "tarc.tsv", path = path1, end= 38918, rap = False)
dfR, dateR, wordsR, araR, posR, toksR, tipoR, locR, ageR, gendR  = upload(filename = "tarc.tsv", path = path1, end= 38919, rap = True) #only rap data

# =============================================================================         
# --------------------------------------------------------------------------
# |  Q¯af realization                                                      |
# |  Diatopic and diastratic analyses                                      |
# --------------------------------------------------------------------------
govlis = ['TunisQ', 'TunisG', 'Ariana', 'Béja', 'Sousse', 'Bizerte', 'Gabès', 'Nabeul', 'Jendouba', 'Kairouan', 'Zaghouan', 'Kebili', 'El_Kef', 'Mahdia', 'Manouba', 'Medenine', 'Monastir', 'Gafsa', 'Sfax', 'Sidi_Bouzid', 'Siliana', 'Ben_Arous', 'Tataouine', 'Tozeur', 'Kasserine']
#govlis includes all the governorates except for Tunis


#list of indexes where there is a <ق> (<q>) in the word encoded in CODA
def Qlist(rap = False): 

    if rap == True: 
        qidx = []
        for x, y in enumerate(wordsR): 
            if 'ق' in y: 
                qidx.append(x)
    else:
        qidx = []
        for x, y in enumerate(words): 
            if 'ق' in y: 
                qidx.append(x)

    return qidx

#this function separates the different graphical realization (q and 9 vs. g)
def Separate(gender=False, rap=False): 
    
    if rap: 
        qala, gala, tunis = [], [], [] 
        qidx = Qlist(rap = True)
        govlis.append('Tunis')
        for x, y in enumerate(qidx):
            if 'g' in araR[y]: 
                if locR[y] in govlis:
                    gala.append((x, araR[y], locR[y], ageR[y], gendR[y]))
            elif 'q' in araR[y] or '9' in araR[y]: 
                if locR[y] in govlis:
                    qala.append((x, araR[y], locR[y], ageR[y], gendR[y]))
        govlis.pop(-1)
    else: 
        qala, gala, tunis = [], [], []
        qidx = Qlist(rap = False)
        for x, y in enumerate(qidx):
            if gender == True: #does not exclude tokens for which there is no diatopic info
                if 'g' in ara[y]:
                    if loc[y] != 'Tunis' and gend[y] != '/':
                        gala.append((x, ara[y], loc[y], age[y], gend[y]))
                    elif loc[y] == 'Tunis' and gend[y] != '/':
                        tunis.append((x, ara[y], 'TunisG', age[y], gend[y]))
                elif 'q' in ara[y] or '9' in ara[y]: 
                    if loc[y] != 'Tunis' and gend[y] != '/':
                        qala.append((x, ara[y], loc[y], age[y], gend[y]))
                    elif loc[y] == 'Tunis' and gend[y] != '/':
                        tunis.append((x, ara[y], 'TunisQ', age[y], gend[y]))
            
            else: #takes only tokens for which there is diatopic information
                if 'g' in ara[y]: 
                    if loc[y] in govlis:
                        gala.append((x, ara[y], loc[y], age[y], gend[y]))
                    elif loc[y] == 'Tunis':
                        tunis.append((x, ara[y], 'TunisG', age[y], gend[y]))
                elif 'q' in ara[y] or '9' in ara[y]: 
                    if loc[y] in govlis:
                        qala.append((x, ara[y], loc[y], age[y], gend[y]))
                    elif loc[y] == 'Tunis':
                        tunis.append((x, ara[y], 'TunisQ', age[y], gend[y]))
            
    return qala, gala, tunis

#Govs function counts the occurrences for each governorate
def Govs(lis): 
    
    govDiz = {'Ariana':0, 'Béja':0, 'Sousse':0, 'Bizerte':0, 
              'Gabès':0, 'Nabeul':0, 'Jendouba':0, 'Kairouan':0, 
              'Zaghouan':0, 'Kebili':0, 'El_Kef':0, 'Mahdia':0, 
              'Manouba':0, 'Medenine':0, 'Monastir':0, 'Gafsa':0, 
              'Sfax':0, 'Sidi_Bouzid':0, 'Siliana':0, 'Ben_Arous':0, 
              'Tataouine':0, 'Tozeur':0, 'TunisG':0, 'TunisQ':0, 'Kasserine':0}
   
    
    for x, y in enumerate(lis):
        idx, ar, l= y[0], y[1], y[2]
        if y[2] in govDiz: 
            govDiz[y[2]] += 1
            
    return govDiz

#data: loc_code (urban=0/not_urban=1) | Q_code (0=qala/1=gala) 
def PearsonDiatopic(verbose=True, Tunis=False): 
    l, Q = [], []
    qala, gala, tunis = Separate(gender=False, rap=False)
    Ulis = ['Bizerte', 'Ariana', 'Zaghouan', 'Nabeul', 'Kairouan', 'Sousse', 'Monastir', 'Mahdia', 'Sfax'] 
    Blis = ['Béja',  'Gabès',  'Jendouba',  'Kebili',  'El_Kef',  'Manouba', 'Medenine',  'Gafsa', 'Sidi_Bouzid', 'Siliana', 'Ben_Arous', 'Tataouine', 'Tozeur', 'Kasserine']
    for x, y in enumerate(qala): 
        if y[2] in Ulis:
            l.append(0)
            Q.append(0)
        elif y[2] in Blis: 
            l.append(1)
            Q.append(0)
    
    for x, y in enumerate(gala): 
        if y[2] in Ulis:
            l.append(0)
            Q.append(1)
        elif y[2] in Blis: 
            l.append(1)
            Q.append(1)      
            
    if Tunis == True: 
        for x, y in enumerate(tunis): 
            l.append(2)
            if y[2] == 'TunisQ':
                Q.append(1)
            else:
                Q.append(0)
    
    Pdf= pd.DataFrame({'l':l,'Q':Q})  

    x_ = Pdf['l']
    y_ = Pdf['Q'] 
       
    contigency= pd.crosstab(x_, y_)
    #contigency_pct= pd.crosstab(x_, y_, normalize='index')
    chi2, p_value, dof, expected = chi2_contingency(contigency)
    if p_value < 0.05: 
        p = 'significative'
    else: 
        p = 'not significative' 

    
    if verbose:
        if Tunis == True:          
            print('The Pearson’s chi-square between governorates (+Tunis) and the /q/ realization is '+p +' being the p-value '+str(round(p_value,2)))
        else: 
            print('The Pearson’s chi-square between governorates (-Tunis) and the /q/ realization is '+p +' being the p-value '+str(round(p_value,2)))
        
        
    return loc, Q  
 
  

def DiatopicWrite(verbose=True):            
    qala, gala, tunis = Separate(gender=False, rap=False)
    dizQ = Govs(qala)  
    dizG = Govs(gala) 
    dizT = Govs(tunis)
    

    totG, totQ, totT = len(gala), len(qala), len(tunis)
    
    if verbose == True:
    
        print('________________DIATOPIC ANALYSIS_______________________\n\nThe percentage of Governorates bil-qala (81.03% of the total) are:\n')
        for x in dizQ: 
            if dizQ[x] != 0:
                print(x+': '+str(round(dizQ[x]*100/totQ,2))+'%')
                      
        print('..............................................\nThe percentage of Governorates bil-gala (18.96% of the total) are:\n')
        for x in dizG: 
            if dizG[x] != 0:
                print(x+': '+str(round(dizG[x]*100/totG,2))+'%')  
        
        print('..............................................')
        PearsonDiatopic(verbose=True, Tunis=False) 
                
        print('_____________________________________________\nRegarding Tunis:\n')
        for x in dizT: 
            if dizT[x] != 0:
                print(x+': '+str(round(dizT[x]*100/totT,2))+'%')  
        print('..............................................')        
        PearsonDiatopic(verbose=True, Tunis=True) 

    return dizT

def File(qala, gala, tunis): 
    
    file = path1+'\\q_realization.txt'
    
    f = open(file, 'w', encoding='utf-8')
    f.write('The following are the words containing [q] realization (Tunis excluded):\n\n')
    for x, y in enumerate(qala): 
        f.write(f'<idx: {y[0]+1}> <word: {y[1]}> <gov: {y[2]}> <age: {y[3]}> <gender:{y[4]}>\n\n')
    
    f.write('\n\t***********************************************\n')
    f.write('The following are the words containing [g] realization (Tunis excluded):\n\n')
    for x, y in enumerate(gala): 
        f.write(f'<idx: {y[0]+1}> <word: {y[1]}> <gov: {y[2]}> <age: {y[3]}> <gender:{y[4]}>\n\n')

    f.write('\n\t***********************************************\n')
    f.write('The following are the words containing [q] realization from Tunis:\n\n')
    for x, y in enumerate(tunis): 
        if y[2] == 'TunisQ':
            f.write(f'<idx: {y[0]+1}> <word: {y[1]}> <gov: Tunis> <age: {y[3]}> <gender:{y[4]}>\n\n')
    
    f.write('\n\t***********************************************\n')            
    f.write('The following are the words containing [g] realization from Tunis:\n\n')
    for x, y in enumerate(tunis): 
        if y[2] == 'TunisG':
            f.write(f'<idx: {y[0]+1}> <word: {y[1]}> <gov: Tunis> <age: {y[3]}> <gender:{y[4]}>\n\n')

    f.close() 

#data: Gder (M=0/F=1) | Q_code (0=qala/1=gala) 
def PearsonGender(verbose = True, Tunis = True): 
    
    qala, gala, tunis = Separate(gender=True, rap=False)
    File(qala, gala, tunis)
    Gder, Q_code = [], []
    for x, y in enumerate(qala): 
        if y[-1] == 'M':
            Gder.append(0)
            Q_code.append(0)
        elif y[-1] == 'F': 
            Gder.append(1)
            Q_code.append(0)
    
    for x, y in enumerate(gala): 
        if y[-1] == 'M':
            Gder.append(0)
            Q_code.append(1)
        elif y[-1] == 'F': 
            Gder.append(1)
            Q_code.append(1)      
            
    if Tunis == True: 
        for x, y in enumerate(tunis): 
            if y[2] == 'TunisQ':
                Q_code.append(1)
                if y[-1] == 'M':
                    Gder.append(0)
                elif y[-1] == 'F': 
                    Gder.append(1)
            else:
                Q_code.append(0)
                if y[-1] == 'M':
                    Gder.append(0)
                elif y[-1] == 'F': 
                    Gder.append(1)
                    
    Pdf= pd.DataFrame({'qaf':Q_code,'Sex':Gder})  

    x_ = Pdf['qaf']
    y_ = Pdf['Sex']      
    contigency= pd.crosstab(x_, y_)
    #contigency_pct= pd.crosstab(x_, y_, normalize='index')
    chi2, p_value, dof, expected = chi2_contingency(contigency)
    #sns.heatmap(contigency, annot=True, cmap="YlGnBu")
    #print('/q/ realization', contigency)        
   
    if p_value < 0.05: 
        p = 'significative'
    else: 
        p = 'not significative' 
    
    
    if verbose:
        if Tunis == True: 
            print(f'The Pearson’s chi-square between users gender (+Tunis) and the /q/ realization gave a {p} p-value, being {round(p_value,2)}')

        else:
            print(f'The Pearson’s chi-square between users gender (-Tunis) and the /q/ realization gave a {p} p-value, being {round(p_value,2)}')

   
    return Gder, Q_code  
    


def GenderWrite():            
    qala, gala, tunis = Separate(gender=True, rap=False)
    #totG, totQ, totT = len(gala), len(qala), len(tunis)
    
    print('____________________GENDER ANALYSIS_________________________\n\nThe percentage of users writing bil-qala (86.63% of the total) are:\n')
    M, F = 0, 0
    for x, y in enumerate(qala): 
        if qala[x][4] == 'M':
            M += 1
        elif qala[x][4] == 'F':
            F += 1
        
    print('Female for the '+str(round(F*100/(M+F),2))+'%')
    print('Male for the '+str(round(M*100/(M+F),2))+'%')
    # Pie chart for bil-qala table (4.5) :
    labels = 'M', 'F'
    sizes = [round(M*100/(M+F),2), round(F*100/(M+F),2)]
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()               
    print('..............................................\nThe percentage of users writing bil-gala (13.36% of the total) are:\n')
    M, F = 0, 0
    for x, y in enumerate(gala): 
        if gala[x][4] == 'M':
            M += 1
        elif gala[x][4] == 'F':
            F += 1
        
    print('Female for the '+str(round(F*100/(M+F),2))+'%')
    print('Male for the '+str(round(M*100/(M+F),2))+'%') 
    # Pie chart for bil-gala table (4.6):
    labels = 'M', 'F'
    sizes = [round(M*100/(M+F),2), round(F*100/(M+F),2)]
    explode = (0.1, 0)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show() 
    print('..............................................')
    PearsonGender(verbose = True, Tunis = False)
            
    print('..............................................\nRegarding Tunis, the users are:\n')

    M, F = 0, 0
    for x, y in enumerate(tunis): 
        if tunis[x][4] == 'M':
            M += 1
        elif tunis[x][4] == 'F':
            F += 1
        
    
    GM, GF, QM, QF = 0,0,0,0
    for x, y in enumerate(tunis): 
        if tunis[x][2] == 'TunisG': 
            if tunis[x][4] == 'M':
                GM += 1  
            elif tunis[x][4] == 'F':
                GF += 1
        elif tunis[x][2] == 'TunisQ':
            if tunis[x][4] == 'M':
                QM += 1  
            elif tunis[x][4] == 'F':
                QF += 1
    
    print('-Female for the '+str(round(F*100/(M+F),2))+'% and')
    print('\t'+str(round(QF*100/(QF+GF),2))+'% write bil-qala.')
    print('\t'+str(round(GF*100/(QF+GF),2))+'% write bil-gala,\n')

    print('-Male for the '+str(round(M*100/(M+F),2))+'%. Of them:')
    print('\t'+str(round(QM*100/(QM+GM),2))+'% write bil-qala,')       
    print('\t'+str(round(GM*100/(QM+GM),2))+'% write bil-gala.') 
    # Pie chart for table 4.7 male of Tunis:
    labels = 'M (bil-qala)', 'M (bil-gala)'
    sizes = [round(QM*100/(QM+GM),2), round(GM*100/(QM+GM),2)]
    explode = (0, 0.1)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    # Pie chart for table 4.8, female of Tunis:
    labels = 'F (bil-qala)', 'F (bil-gala)'
    sizes = [round(QF*100/(QF+GF),2), round(GF*100/(QF+GF),2)]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    print('..............................................')
    PearsonGender(verbose = True, Tunis = True)      

def RapWrite(): 
    print('\n___________________RAP_______________________\n')
    qala, gala, tunis = Separate(gender=False, rap=True)
    tot = len(qala)+len(gala)
    print('The percentage of token (from rap data) encoded with g is '+ str(round(len(gala)*100/tot,2))+'%')
    print('The percentage of token (from rap data) encoded with q/9 is '+ str(round(len(qala)*100/tot,2))+'%')
    

def main():
    DiatopicWrite(verbose=True)
    GenderWrite()
    RapWrite()

if __name__ == "__main__":
    main()


