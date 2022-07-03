# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 18:14:59 2021

@author: Elisa
"""
#==============================================================================
#          Koinaization (Trends Analyses) - Gender opposition
#==============================================================================

# ----------------------------------------------------------------------------------------------------
# |                      DATA INFORMATION                                                            |
# -------------------------------------------------------------------------
# | This script is set to work on the tarc data totality (file tarc.tsv)  |
# -------------------------------------------------------------------------
import pandas as pd 
import matplotlib.pyplot as plt
path1 = r""
from utilities import weak_verbs


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
# |  Diatopic frequency of gender opposition                               |
# |  in Tunisia                                                            |
# --------------------------------------------------------------------------

search = ['PRON_2S', 'PV-PVSUFF_SUBJ:2S', 'IV2S-IV', 'CV2S-CV']

def Idx(): 
    
    avoid = ['تمشي', 'تجيني', 'تبمبي','تعطي', 'تحكي لي', 'تسمعشي', 'سكّر لي', 'تسربي', 'ترابي', 'تولّي', 'تجيني', 'ما تريني', 'لارڨي', 'تعدّي', 'تشري', 'يزّي', 'ابكي', 'قلت لي', 'خلّي', 'ترصّي لي', 'قل لي', 'خلّيني', 'خلّينا', 'تبكي', 'اشفي', 'صلّي', 'لك', 'عليك', 'وراك', 'معك', 'فيك', 'بك', 'عكعك', 'عندك', 'متاعك', 'وينك', 'ما عندك', 'وايّاك', 'ماك', 'راك', 'هاك', 'اذا كانك', 'خير لك', 'كيفك', 'محمد اطلع', 'كانك', 'ما تساعدك', 'انّك', 'نفسك', 'ماكلك', 'بينك', 'وحدك']
    idxlis = []
    for x, y in enumerate(pos):
        if words[x] not in avoid:
            y = y.split('+')
            for morph in y: 
                if morph in search: 
                    idxlis.append((x, morph, ara[x], words[x], loc[x]))
                
    return idxlis

def Separate(): 

    idxlis = Idx()
    Ulis = ['Bizerte', 'Ariana', 'Zaghouan', 'Nabeul', 'Kairouan', 'Sousse', 'Monastir', 'Mahdia', 'Sfax'] 
    Blis = ['Béja',  'Gabès',  'Jendouba',  'Kebili',  'El_Kef',  'Manouba', 'Medenine',  'Gafsa', 'Sidi_Bouzid', 'Siliana', 'Ben_Arous', 'Tataouine', 'Tozeur', 'Kasserine']
    
    Uidx, Bidx, Tunis = [], [], []
    
    for x, y in enumerate(idxlis): 
        if y[-1] in Ulis:
            Uidx.append(y)
        elif y[-1] in Blis: 
            Bidx.append(y)
        elif y[-1] == 'Tunis': 
            Tunis.append(y)
            
            
    return Uidx, Bidx, Tunis
        
        
def Op(y): 
        
    if y[-2] == 'n': 
        w = y[:-2]
    else: 
        w = y
            
    return w

def Opposition(lis):
    avoid  = ['tjii', 'ta7ki', 'thnini', 'témchi', 'tehki', 'echefihi', 'Nahi', 'Ta7chali','a7ki', 'tetwi', 'a3ti', 'marquini', 'yezzi', 'Te7chii']
    opposed = []
    
    
    for x, y in enumerate(lis):   
        if y[2] not in avoid:
            w = Op(y[2])
            
            if y[1] == 'PRON_2S':
                if w[-1] == 'a': 
                    opposed.append((y[2], y[-1]))
            elif y[1] == 'PV-PVSUFF_SUBJ:2S':
                if w[-1] == 'i'or w[-1] == 'y': 
                    opposed.append((y[2], y[-1]))
            elif y[1] == 'IV2S-IV':
                if w[-1] == 'i'or w[-1] == 'y': 
                    opposed.append((y[2], y[-1]))
            else: 
                if w[-1] == 'i'or w[-1] == 'y': 
                    opposed.append((y[2], y[-1]))
     
    return opposed, len(lis)

def Print(): 
    Udx, Bdx, Tun = Separate() 
    opposedBU, totBU = Opposition(Bdx+Udx)
    opposedT, totT = Opposition(Tun)
    
    print(f"-The percentage of urban style writing for governorates (except Tunis) is: {round((totBU-len(opposedBU))*100/totBU,2)}%.")
    print(f"-The percentage of gender opposition for governorates (except Tunis) is: {round(len(opposedBU)*100/totBU,2)}%.")
    print(f"-The percentage of urban style writing for Tunis gov. is: {round((totT-len(opposedT))*100/totT,2)}%.")
    print(f"-The percentage of gender opposition for Tunis gov. is: {round(len(opposedT)*100/totT,2)}%.")

    # Pie chart for table 4.32 gender opposition in Tunis:
    labels = 'unique gender', 'gender opposition'
    sizes = [round((totT-len(opposedT))*100/totT,2), round(len(opposedT)*100/totT,2)]
    explode = (0.1, 0)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()



# =============================================================================         
# --------------------------------------------------------------------------
# |  distribution of the plural morpheme -w                                |
# |  in Tunisia                                                            |
# --------------------------------------------------------------------------


def Indx(): 
    
    #select contain weak verbs in plural form
    
    idxlis = []
    for x, y in enumerate(toks):
        
        y = y.split('+')
        for w in y: 
            if w[-2:] == 'وا' and w in weak_verbs:
                idxlis.append((x, w, ara[x], words[x], loc[x]))
                
    return idxlis

def Separ(): 

    idxlis = Indx()
    Ulis = ['Bizerte', 'Ariana', 'Zaghouan', 'Nabeul', 'Kairouan', 'Sousse', 'Monastir', 'Mahdia', 'Sfax'] 
    Blis = ['Béja',  'Gabès',  'Jendouba',  'Kebili',  'El_Kef',  'Manouba', 'Medenine',  'Gafsa', 'Sidi_Bouzid', 'Siliana', 'Ben_Arous', 'Tataouine', 'Tozeur', 'Kasserine']
    
    Uidx, Bidx, Tunis = [], [], []
    
    for x, y in enumerate(idxlis): 
        if y[-1] in Ulis:
            Uidx.append(y)
        elif y[-1] in Blis: 
            Bidx.append(y)
        elif y[-1] == 'Tunis': 
            Tunis.append(y)
            
            
    return Uidx, Bidx, Tunis
        
def Split(lis): 
    
    Bstyle, Ustyle = [], []
    for x, y in enumerate(lis):
        if y[1][-3:] == 'يوا' or y[1][-3:] == 'اوا': 
            Ustyle.append(y)
        else: 
            Bstyle.append(y)
    
    
    return Bstyle, Ustyle
            
    
    
    
def Write():  
    Uidx, Bidx, Tunis = Separ()  
    BstyleBU, UstyleBU = Split(Uidx+Bidx)
    BUtot = len(Uidx+Bidx)
    BstyleT, UstyleT = Split(Tunis)
    Ttot = len(Tunis)
    
    print(f"-The percentage of urban style writing for governorates (except Tunis) is: {round(len(UstyleBU)*100/BUtot,2)}%.")
    print(f"-The percentage of Bedouin style writing for governorates (except Tunis) is: {round(len(BstyleBU)*100/BUtot,2)}%.")
    
    # Pie chart for table 4.34 plural morph. Tunis excluded:
    labels = 'Urban style', 'Bedouin style'
    sizes = [round(len(UstyleBU)*100/BUtot,2), round(len(BstyleBU)*100/BUtot,2)]
    explode = (0, 0.1)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    
    print(f"-The percentage of urban style writing for Tunis gov. is: {round(len(UstyleT)*100/Ttot,2)}%.")
    print(f"-The percentage of Bedouin style writing for Tunis gov. is: {round(len(BstyleT)*100/Ttot,2)}%.")

    # Pie chart for table 4.35 plural morph in Tunis:
    labels = 'Urban style', 'Bedouin style'
    sizes = [round(len(UstyleT)*100/Ttot,2), round(len(BstyleT)*100/Ttot,2)]
    explode = (0.1, 0)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()


print("\n_________________GENDER OPPOSITION ANALYSIS_______________________________\n")
Print()
print("\n_________________Assimilation of -w plural morpheme in weak verbs_________\n")
Write()
