# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 11:37:11 2021

@author: Elisa
"""
#==============================================================================
#          Koinaization (Trends Analyses) - Diphtongs
#==============================================================================

# ----------------------------------------------------------------------------------------------------
# |                      DATA INFORMATION                                                            |
# -------------------------------------------------------------------------
# | This script is set to work on the tarc data totality (file tarc.tsv)  |
# -------------------------------------------------------------------------
import pandas as pd 
import matplotlib.pyplot as plt
path1 = r""
from utilities import avoid
from utilities import p_avoid
from scipy.stats import chi2_contingency

def upload(filename="", path = path1):
    tsv = path+filename
    df = pd.read_csv(tsv, sep="\t", encoding='utf-8').astype(str)

    date = list(df['data'])
    words = list(df['CODA'])  
    ara = list(df['arabish']) 
    toks = list(df['token'])
    pos = list(df['pos'])
    tipo = list(df['TYPE'])
    loc = list(df['governorate'])
    age = list(df['age'])
    gend = list(df['gender'])
          
    return df, date, words, ara, pos, toks, tipo, loc, age, gend 
        
df, date, words, ara, pos, toks, tipo, loc, age, gend  = upload(filename = "\\TArC.tsv", path = path1)


# =============================================================================         
# --------------------------------------------------------------------------
# |  Diatopic frequency of diphthongs                                      |
# |  in Tunisia                                                            |
# --------------------------------------------------------------------------
govlis = ['TunisQ', 'TunisG', 'Ariana', 'Béja', 'Sousse', 'Bizerte', 'Gabès', 'Nabeul', 'Jendouba', 'Kairouan', 'Zaghouan', 'Kebili', 'El_Kef', 'Mahdia', 'Manouba', 'Medenine', 'Monastir', 'Gafsa', 'Sfax', 'Sidi_Bouzid', 'Siliana', 'Ben_Arous', 'Tataouine', 'Tozeur', 'Kasserine']
#govlis is without Tunis governorate

#dictionary with 2 lists of indexes where in the word appears a y or a w in the second position
def Dlist(): 

    didx = {'y':[], 'w':[]}
    #in 'avoid' list there are 82 words with not etymological diphtongs and loans
    for x, y in enumerate(words): 
        p = pos[x].split('-') 
        if y not in avoid and p[0]  not in p_avoid:
                            
                if len(y) >= 3:
                                            
                    w = list(y)
                    if w[0] != 'ا' and w[1] == 'ي' :
                        #if w[2] != 'ّ': #shadda
                        if pos[x] != 'NOUN_PROP':
                            if w[0] != 'ف' and pos[x].split('+')[0] != 'PREP':
                                didx['y'].append(x)
                    elif w[0] != 'ا' and w[1] == 'و':
                        #if w[2] != 'ّ': #shadda
                        if pos[x] != 'NOUN_PROP':
                            if 'PRON' not in pos[x] and 'روح' not in y:
                                didx['w'].append(x)

    return didx

#The function separates diphthong from monophthongation for y and w
def Separate(gender=False): 
    
    dipht, monopht = {'ay':[], 'aw':[]}, {'i':[], 'u':[]}
    didx = Dlist()
    for x, y in enumerate(didx['y']):
        
         if gender == True:  #does not exclude tokens for which there is no diatopic info
              if loc[y] == 'Tunis' and gend[y] != '/':   
                 if 'ay' in ara[y] or 'ey' in ara[y]: 
                     dipht['ay'].append((y, ara[y], words[y], loc[y], age[y], gend[y]))
                 elif 'ai' in ara[y] or 'ei' in ara[y]: 
                     dipht['ay'].append((y, ara[y], words[y], loc[y], age[y], gend[y]))
                    
                 elif 'éy' in ara[y] or 'éi' in ara[y]: 
                     dipht['ay'].append((y, ara[y], words[y], loc[y], age[y], gend[y]))
                    
                 elif 'i' in ara[y] or 'e' in ara[y]: 
                    monopht['i'].append((y, ara[y], words[y], loc[y], age[y], gend[y]))

        
         else:#takes only tokens for which there is diatopic information
            if 'ay' in ara[y] or 'ey' in ara[y]: 
                dipht['ay'].append((y, ara[y], words[y], loc[y]))
                
            elif 'ai' in ara[y] or 'ei' in ara[y]: 
                dipht['ay'].append((y, ara[y], words[y], loc[y]))
                
            elif 'éy' in ara[y] or 'éi' in ara[y]: 
                dipht['ay'].append((y, ara[y], words[y], loc[y]))
                
            elif 'i' in ara[y] or 'e' in ara[y]: 
                monopht['i'].append((y, ara[y], words[y], loc[y]))
                    
    for x, y in enumerate(didx['w']):
        
        if gender == True:#does not exclude tokens for which there is no diatopic info       
            if loc[y] == 'Tunis' and gend[y] != '/':                  
                if 'aw' in ara[y] or 'ew' in ara[y]: 
                    dipht['aw'].append((y, ara[y], words[y], loc[y], age[y], gend[y]))
                    
                elif 'u' in ara[y] or 'o' in ara[y]: 
                    monopht['u'].append((y, ara[y], words[y], loc[y], age[y], gend[y]))
            
        else: #takes only tokens for which there is diatopic information
            if 'aw' in ara[y] or 'ew' in ara[y]: 
                dipht['aw'].append((y, ara[y], words[y], loc[y]))
                
            elif 'u' in ara[y] or 'o' in ara[y]: 
                monopht['u'].append((y, ara[y], words[y], loc[y]))
        
    return dipht, monopht


#The function calculates the occurrences for each governorate
def Govs(lis, Tunis=True): # dipht['ay'] | dipht['aw'] | monopht['i'] | monopht['u']  
    
    if Tunis:  
        
        govDiz = {'Tunis':0} 
        
        
        for x, y in enumerate(lis):
            idx, ar, l= y[0], y[1], y[2]
            if y[3] in govDiz: 
                govDiz[y[3]] += 1
                
        tot = govDiz['Tunis']
                
    else: 
        tot = 0
        govDiz = {'Ariana':0, 'Béja':0, 'Sousse':0, 'Bizerte':0, 
                  'Gabès':0, 'Nabeul':0, 'Jendouba':0, 'Kairouan':0, 
                  'Zaghouan':0, 'Kebili':0, 'El_Kef':0, 'Mahdia':0, 
                  'Manouba':0, 'Medenine':0, 'Monastir':0, 'Gafsa':0, 
                  'Sfax':0, 'Sidi_Bouzid':0, 'Siliana':0, 'Ben_Arous':0, 
                  'Tataouine':0, 'Tozeur':0, 'Kasserine':0}
       
        
        for x, y in enumerate(lis):
            idx, ar, l= y[0], y[1], y[2]
            if y[3] in govDiz: 
                govDiz[y[3]] += 1
        
        for x, y in enumerate(govDiz): 
            tot += govDiz[y]
        
            
    return govDiz, tot

def PearsonDiatopic(verbose=True, Tunis=False): #data: loc_code (urban=0/not_urban=1) | pht (0=dipht/1=monopht) 
    loc_code, pht = [], []
    dipht, monopht = Separate(gender=False)
    Ulis = ['Bizerte', 'Ariana', 'Zaghouan', 'Nabeul', 'Kairouan', 'Sousse', 'Monastir', 'Mahdia', 'Sfax'] 
    Blis = ['Béja',  'Gabès',  'Jendouba',  'Kebili',  'El_Kef',  'Manouba', 'Medenine',  'Gafsa', 'Sidi_Bouzid', 'Siliana', 'Ben_Arous', 'Tataouine', 'Tozeur', 'Kasserine']
    for x, y in enumerate(dipht['ay']): 
        if y[3] in Ulis:
            loc_code.append(0)
            pht.append(0)
        elif y[3] in Blis: 
            loc_code.append(1)
            pht.append(0)
        if Tunis == True: 
            if y[3] == 'Tunis': 
                loc_code.append(2)
                pht.append(0)            
                    
    for x, y in enumerate(dipht['aw']): 
        if y[3] in Ulis:
            loc_code.append(0)
            pht.append(0)
        elif y[3] in Blis: 
            loc_code.append(1)
            pht.append(0)   
        if Tunis == True: 
            if y[3] == 'Tunis': 
                loc_code.append(2)
                pht.append(0)
            
    for x, y in enumerate(monopht['i']): 
        if y[3] in Ulis:
            loc_code.append(0)
            pht.append(1)
        elif y[3] in Blis: 
            loc_code.append(1)
            pht.append(1)
        if Tunis == True: 
            if y[3] == 'Tunis': 
                loc_code.append(0)
                pht.append(1)
    
    for x, y in enumerate(monopht['u']): 
        if y[3] in Ulis:
            loc_code.append(0)
            pht.append(1)
        elif y[3] in Blis: 
            loc_code.append(1)
            pht.append(1)  
        if Tunis == True: 
            if y[3] == 'Tunis': 
                loc_code.append(0)
                pht.append(1)
    
    Pdf= pd.DataFrame({'loc_code':loc_code,'pht':pht})  

    x_ = Pdf['loc_code']
    y_ = Pdf['pht'] 

    contigency= pd.crosstab(x_, y_)

    chi2, p_value, dof, expected = chi2_contingency(contigency)
    if p_value < 0.05: 
        p = 'significative'
    else: 
        p = 'not significative'
        
    if verbose:
        if Tunis == True: 
            print(f'The Pearson’s chi-square between governorates (+Tunis) and the etymological diphtongs realization is {p}, being the p_value {round(p_value,2)}')
        else: 
            print(f'The Pearson’s chi-square between governorates (-Tunis) and the etymological diphtongs realization is {p}, being the p_value {round(p_value,2)}')
                
    return loc_code, pht 

def File(dipht, monopht): 
    
    file = path1+'\\diphtongs_realization.txt'
    
    f = open(file, 'w', encoding='utf-8')
    f.write('The following are the words containing the diphtong /ay/:\n\n')
    for x, y in enumerate(dipht['ay']): 
        f.write(f'<idx: {y[0]}> <word: {y[1]}> <gov: {y[3]}> <age: {y[4]}> <gender:{y[5]}>\n\n')
    
    f.write('\n\t***********************************************\n')
    f.write('The following are the words containing the diphtong /aw/:\n\n')
    for x, y in enumerate(dipht['aw']): 
        f.write(f'<idx: {y[0]}> <word: {y[1]}> <gov: {y[3]}> <age: {y[4]}> <gender:{y[5]}>\n\n')

    f.write('\n\t***********************************************\n')
    f.write('The following are the words containing the monophtongization in /i:/:\n\n')
    for x, y in enumerate(monopht['i']): 
        f.write(f'<idx: {y[0]}> <word: {y[1]}> <gov: {y[3]}> <age: {y[4]}> <gender:{y[5]}>\n\n')
    
    f.write('\n\t***********************************************\n')            
    f.write('The following are the words containing the monophtongization in /u:/:\n\n')
    for x, y in enumerate(monopht['u']): 
        f.write(f'<idx: {y[0]}> <word: {y[1]}> <gov: {y[3]}> <age: {y[4]}> <gender:{y[5]}>\n\n')

    f.close() 

   

def DiatopicWrite(verbose=True):            
    dipht, monopht = Separate(gender=False)
    Dipht_noTun, TotD = Govs(dipht['ay']+dipht['aw'], Tunis=False)
    Mono_noTun, TotM = Govs(monopht['i']+monopht['u'], Tunis=False)
    Dipht_Tun, TTD = Govs(dipht['ay']+dipht['aw'], Tunis=True)
    Mono_Tun, TTM = Govs(monopht['i']+monopht['u'], Tunis=True)
    tot, Ttot = TotD+TotM, TTD+TTM

    if verbose == True:
    
        print(f'________________DIATOPIC ANALYSIS_______________________\n\nThe percentage of Governorates with diphtongs ({round(TotD*100/tot,2)}% of the total) is:\n')
        print('-For AY+AW dipthongs:')
        for x in Dipht_noTun: 
            if Dipht_noTun[x] != 0:
                print(x+': '+str(round(Dipht_noTun[x]*100/TotD,2))+'%.') 

        print(f'..............................................\nThe percentage of Governorates with monophtongization ({round(TotM*100/tot,2)}% of the total) is:\n')
        print('\n-For each kind of monophtongization:')
        for x in Mono_noTun: 
            if Mono_noTun[x] != 0:
                print(x+': '+str(round(Mono_noTun[x]*100/TotM,2))+'%.')
        
        print('..............................................')
        PearsonDiatopic(verbose=True, Tunis=False) 
                
        print('_____________________________________________\nRegarding Tunis data:\n')

        print(f"The percentage of diphtongs from Tunis is {str(round(TTD*100/Ttot,2))}%\n")

        print(f"The percentage of monophtongs from Tunis is {str(round(TTM*100/Ttot,2))}%\n")
        
        # Pie chart for table 4.30:
        labels = 'Tunis Dipht.', 'Tunis Monopht.'
        sizes = [round(TTD*100/Ttot,2), round(TTM*100/Ttot,2)]
        explode = (0, 0.1)  # only "explode" the 2nd slice 
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        plt.show()        
        print('..............................................')        
        PearsonDiatopic(verbose=True, Tunis=True) 
        

def GenderWrite():    
    
    dipht, monopht = Separate(gender=True)
    File(dipht, monopht)    
    TTD = len(dipht['ay'])+len(dipht['aw'])
    #Mono_Tun, TTM = Govs(monopht['i']+monopht['u'], Tunis=True)
    m = 0
    f = 0
    for x in dipht:
        for z, y in enumerate(dipht[x]): 
            if y[-1] == 'M': 
                m += 1
            else: 
                f += 1
    print('\n______________GENDER ANALYSIS ON TUNIS DATA_____________________\n')            
    print(f"Out of the data from Tunis which contains diphthongs, the percentage of male users is: {round(m*100/TTD,2)}%,")
    print(f"while the percentage of female users is: {round(f*100/TTD,2)}%.")
   
    # Pie chart for table 4.31:
    labels = 'M', 'F'
    sizes = [round(m*100/TTD,2), round(f*100/TTD,2)]
    explode = (0.1, 0)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
   
    
DiatopicWrite(verbose=True)
GenderWrite()

