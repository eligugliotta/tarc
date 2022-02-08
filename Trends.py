# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 17:08:56 2021

@author: Elisa
"""
#==============================================================================
#           Prepositional Phrase (Trends Analyses)
#==============================================================================

# ----------------------------------------------------------------------------------------------------
# |                      DATA INFORMATION                                                            |
# -------------------------------------------------------------------------
# | This script is set to work on the tarc data totality (file tarc.tsv)  |
# -------------------------------------------------------------------------

import pandas as pd 
path = r""
from utilities import solar
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt


def upload(filename="", path = path):
    tsv = path+filename
    df = pd.read_csv(tsv, sep="\t", encoding='utf-8').astype(str)
    date = list(df['data'])
    words = list(df['CODA'])
    ara = list(df['arabish'])
    toks = list(df['token'])
    pos = list(df['pos'])
    loc = list(df['governorate'])
    age = list(df['age'])
    gend = list(df['gender'])
    
    
    return df, date, words, ara, pos, toks, loc, age, gend 
        
df, date, words, ara, pos, toks, loc, age, gend = upload(filename = "\\tarc.tsv", path = path)

# =============================================================================         
# --------------------------------------------------------------------------
# |  analysis 4.3                                                           |
# |  Arithmographemes occurrences in TArC                                   |
# --------------------------------------------------------------------------


nope = ['NOUN_PROP', 'NOUN_NUM', 'emotag', 'foreign']
numb = [str(x) for x in range(2,10)]

def extraRemoving(l): 
    
    for x in range(3):    
        for x, y in enumerate(l):
            c = y[-3]
            cs = c.split('+')
            for x in cs: 
                if x in nope: 
                    
                    if y in l:
                        l.remove(y)
                        
    return l

def numbers():    
    elements = []
    for x, y in enumerate(ara): 
        lett = [l for l in y]
        for a, b in enumerate(lett):
            if b in numb and pos[x] not in nope: 
                if (y, words[x], pos[x], date[x], x) not in elements: 
                    tup = (y, words[x], pos[x], date[x], x)
                    elements.append(tup)
    
    elements = extraRemoving(elements)
    
    return elements


def organizing(verbose = False): 
    dic = {}
    elements = numbers()
    for x, y in enumerate(elements): 
        a, w, p, d, idx = y
        lett = [l for l in a]
        for j, z in enumerate(lett): 
            if z in numb and z not in dic.keys(): 
                dic[z] = [(a, w, d, idx)]
            elif z in numb and z in dic.keys():
                if (a, w, d, idx) not in dic[z]:
                    dic[z].append((a, w, d, idx))
    
    if verbose: 
        print(f'___Numbers Occurrences in TArC___\n\n'
          f'The number {numb[0]} occurs {len(dic[numb[0]])} times\n'
          f'The number {numb[1]} occurs {len(dic[numb[1]])} times\n'
          f'The number {numb[2]} occurs {len(dic[numb[2]])} times\n'
          f'The number {numb[3]} occurs {len(dic[numb[3]])} times\n'
          f'The number {numb[4]} occurs {len(dic[numb[4]])} times\n'
          f'The number {numb[5]} occurs {len(dic[numb[5]])} times\n'
          f'The number {numb[6]} occurs {len(dic[numb[6]])} times\n'
          f'The number {numb[7]} occurs {len(dic[numb[7]])} times')
    
    return dic


def buildDict(diz, x, date):
    
    if x not in diz.keys(): 
        diz[x] = [date]
    else: 
        diz[x].append(date)
    
    return diz


def diachronyDic():
    
    dic = organizing(verbose = False)
    diz = {}
    for x in numb: 
        for y in dic[x]: 
            if y[-2].isnumeric() == True: 
                date = y[-2][:4]
                diz = buildDict(diz, x, date)
            else: 
                date = y[-2][-4:] 
                diz = buildDict(diz, x, date)
    
    
    d = {}
    for x in numb: 
        d[x] = []
        for y in diz[x]: 
            occ = diz[x].count(y)
            y = y+'_'+str(occ)
            if y not in d[x]: 
                d[x].append(y)
    
    return diz, d
  
    

def dictio(d, dizio, k): 
    
    dizio[d].append(d)
        
    return dizio

def YearsPerc(verbose = False): #works with each year
    
    k = ['05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    dizio = {}
    for x in k:
        dizio[x] = []
    for y in date: 
        if y.isnumeric() == True: 
            d = y[2:4]
            dizio = dictio(d, dizio, k)
        else: 
            d = y[-2:] 
            dizio = dictio(d, dizio, k)
    
    if verbose:
        for k in dizio.keys(): 
            print(f'{len(dizio[k])} total tokens for years {k} \n')
    
    return dizio


def Percentages(): 
    
    dic, d = diachronyDic()  
    #dizio = YearsPerc(verbose = False)
    fs, se, nt, et, tf, fsx, sei, ntw = 0, 0,  0, 0, 0, 0, 0, 0
    Lfs, Lse, Lnt, Let, Ltf, Lfsx, Lsei, Lntw = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}, {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}, {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}, {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}, {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}, {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}, {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}, {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
    # a list of (2x, 3x, 4x, 5x, 6x, 7x, 8x, 9x ) where x is the numb occ per that couple of years 
    print('_____________________________________________\n')


    for x in numb:
             
        for y in range(len(d[x])):
            
            if d[x][y][:4] == '2005' or d[x][y][:4] == '2006' : #
               fs += int(d[x][y][5:])
               if d[x][y][:4] == '2006':
                   n = Lfs[x]+int(d[x][y][5:])
                   Lfs[x] = n
               else:
                   Lfs[x] = int(d[x][y][5:])
                   
            if d[x][y][:4] == '2007' or d[x][y][:4] == '2008' : #
               se += int(d[x][y][5:]) 
               if d[x][y][:4] == '2008':
                   n = Lse[x]+int(d[x][y][5:])
                   Lse[x] = n
               else:
                   Lse[x] = int(d[x][y][5:])
                   
            if d[x][y][:4] == '2009' or d[x][y][:4] == '2010' : #
               nt += int(d[x][y][5:]) 
               if d[x][y][:4] == '2010':
                   n = Lnt[x]+int(d[x][y][5:])
                   Lnt[x] = n
               else:
                   Lnt[x] = int(d[x][y][5:])
                   
            if d[x][y][:4] == '2011' or d[x][y][:4] == '2012' : #
               et += int(d[x][y][5:]) 
               if d[x][y][:4] == '2012':
                   n = Let[x]+int(d[x][y][5:])
                   Let[x] = n
               else:
                   Let[x] = int(d[x][y][5:])
                   
            if d[x][y][:4] == '2013' or d[x][y][:4] == '2014' : #
               tf += int(d[x][y][5:]) 
               if d[x][y][:4] == '2014':
                   n = Ltf[x]+int(d[x][y][5:])
                   Ltf[x] = n
               else:
                   Ltf[x] = int(d[x][y][5:])
                   
            if d[x][y][:4] == '2015' or d[x][y][:4] == '2016' : #
               fsx += int(d[x][y][5:]) 
               if d[x][y][:4] == '2016':
                   n = Lfsx[x]+int(d[x][y][5:])
                   Lfsx[x] = n
               else:
                   Lfsx[x] = int(d[x][y][5:])
                   
            if d[x][y][:4] == '2017' or d[x][y][:4] == '2018' : #
               sei += int(d[x][y][5:])
               if d[x][y][:4] == '2018':
                   n = Lsei[x]+int(d[x][y][5:])
                   Lsei[x] = n
               else:
                   Lsei[x] = int(d[x][y][5:])
                   
            if d[x][y][:4] == '2019' or d[x][y][:4] == '2020' : #
               ntw += int(d[x][y][5:])      
               if d[x][y][:4] == '2020':
                   n = Lntw[x]+int(d[x][y][5:])
                   Lntw[x] = n
               else:
                   Lntw[x] = int(d[x][y][5:])
    
    l = [(2005, fs, Lfs), (2007, se, Lse), (2009, nt, Lnt), (2011, et, Let), (2013, tf, Ltf), (2015, fsx, Lfsx), (2017, sei, Lsei), (2019, ntw, Lntw)]                                                                   

    for x, y in enumerate(l):
        print(str(y[1])+' is the arithmographs tot for years '+str(y[0])+'-'+str(y[0]+1)) #
        print('\n in the same years, the distribution is:\n')
        print(' 2: '+str(round(y[2]['2']*100/y[1],2))+'%'+ '\n 3: '+str(round(y[2]['3']*100/y[1],2))+'%', '\n 4: '+str(round(y[2]['4']*100/y[1], 2))+'%', '\n 5: '+str(round(y[2]['5']*100/y[1],2))+'%', '\n 6: '+str(round(y[2]['6']*100/y[1],2))+'%', '\n 7: '+str(round(y[2]['7']*100/y[1],2))+'%', '\n 8: '+str(round(y[2]['8']*100/y[1],2))+'%', '\n 9: '+str(round(y[2]['9']*100/y[1],2))+'%')
        print('\n')
    print('_____________________________________________\n')    #            
        
    print('\n')
        
    return l
    


# =============================================================================         
# ---------------------------------------------------------------------
# |  analysis 4.3.1                                                   |
# |  Prepositional Phrase distribution                                |
# ---------------------------------------------------------------------

def dateExtraction(x):
    
    if len(date[x]) != 8:
        dd = date[x][-4:]
    else: 
        dd = date[x][:4]
            
    return dd 
    

def extraRem(l, nope, extra): 
    
    for x in range(3):    
        for x, y in enumerate(l):
            c = y[-1]
            cs = c.split('+')
            for x in cs: 
                if x in nope: 
                    extra.append(y)
                    if y in l:
                        l.remove(y)
    return l


def findCompounds(ara, verbose=False):

    nope = ['<eos>', 'SYM', 'PUNC', 'NOUN_PROP', 'NOUN_QUANT', 'ADV',
            'REL_PRON' , 'REL_ADV', 'NEG_PART', 'DEM_PRON_3MP', 'DEM_PRON_3MS',
            'DEM_PRON_3FS', 'DEM_PRON', 'ABBREV', 'PRON_INDEF', 'CONJ', 
            'SUB_CONJ', 'FOCUS_PART']
    extra = []
    
#__________________[PREP+N]____________________________________________________
    PREPNOUN = [] 
    for x, y in enumerate(pos): 
        if 'PREP+NOUN' in y: 
            dd = dateExtraction(x)
            tup = (dd, ara[x], words[x], y)
            PREPNOUN.append(tup)
            
    PREPNOUN = extraRem(PREPNOUN, nope, extra)               
    
#__________________[PREP N]____________________________________________________
    PREP_NOUN = []
    for x, y in enumerate(pos): 
        if y == 'PREP' and 'DET' not in pos[x+1]:
            dd = dateExtraction(x)
            tup = (dd, ara[x], ara[x+1], words[x], words[x+1], y, pos[x+1])
            PREP_NOUN.append(tup)
    
    PREP_NOUN = extraRem(PREP_NOUN, nope, extra)
   

#__________________[PREP+DET+N]_______________________________________________   
    PREPDETN = [] 
    for x, y in enumerate(pos): 
        if 'PREP+DET+NOUN' in y: 
            dd = dateExtraction(x)
            tup = (dd, ara[x], words[x], y)
            PREPDETN.append(tup)

    
#__________________[PREP+DET N]_______________________________________________
    PREPDET_N = []
    for x, y in enumerate(pos): 
        if y == 'PREP+DET' and 'NOUN' in pos[x+1]: 
            dd = dateExtraction(x)
            tup = (dd, ara[x], ara[x+1], words[x], words[x+1], y, pos[x+1])
            PREPDET_N.append(tup)
      
    PREPDET_N = extraRem(PREPDET_N, nope, extra)    
     
    
#__________________[PREP DET+N]_______________________________________________
    PREP_DETN = []
    for x, y in enumerate(pos): 
        if y == 'PREP' and 'DET+NOUN' in pos[x+1]:
            dd = dateExtraction(x)
            tup = (dd, ara[x], ara[x+1], words[x], words[x+1], y, pos[x+1])
            PREP_DETN.append(tup)
    
    PREP_DETN = extraRem(PREP_DETN, nope, extra)    
    
    
#__________________[PREP DET N]________________________________________________
    PREP_DET_N = []
    for x, y in enumerate(pos): 
        if y == 'PREP' and pos[x+1] == 'DET': 
            if 'NOUN' in pos[x+2]:
                dd = dateExtraction(x)
                tup = (dd, ara[x], ara[x+1], ara[x+2], words[x], words[x+1], words[x+2], y, pos[x+1], pos[x+2])
                PREP_DET_N.append(tup)
    
    PREP_DET_N = extraRem(PREP_DET_N, nope, extra)           
    #   after removing extras (2) = 18 occurrences
    
    if verbose:
        tot_no_det = len(PREPNOUN) + len(PREP_NOUN) 
        tot =  len(PREPDETN) + len(PREPDET_N) + len(PREP_DETN) + len(PREP_DET_N)
        print(f'___________________________________________________________________\n'
              f'                                                    \n'
              f'The different types of PP, with the following frequencies, appear in following years: \n\n'
              f'[PREP+N]: {round(len(PREPNOUN)*100/tot_no_det,2)}%,\n'
              f'[PREP N]: {round(len(PREP_NOUN)*100/tot_no_det,2)}%,\n\n' 
              f'[PREP+DET+N]: {round(len(PREPDETN)*100/tot,2)}%,\n' 
              f'[PREP+DET N]: {round(len(PREPDET_N)*100/tot,2)}%,\n' 
              f'[PREP DET+N]: {round(len(PREP_DETN)*100/tot,2)}%,\n' 
              f'[PREP DET N]: {round(len(PREP_DET_N)*100/tot,2)}%')
        
    return PREPNOUN, PREP_NOUN, PREPDETN, PREPDET_N, PREP_DETN, PREP_DET_N

def LkCount(lk, Yrs):
    T = []    
    for pr, lis in enumerate(Yrs): 
        ty = 0
        for x, y in enumerate(lis):
            if y == '2019': 
                ty += lk.count(y)/2
            else:
                ty += lk.count(y)
        
        T.append(ty)
    
    return T

def TypesCount(lk, Yrs): 
    
    for x,y in enumerate(lk): 
        if x == 0: 
            ty0 = LkCount(lk[x], Yrs)  
        elif x == 1: 
            ty1 = LkCount(lk[x], Yrs)  
        elif x == 2: 
            ty2 = LkCount(lk[x], Yrs) 
        elif x == 3: 
            ty3 = LkCount(lk[x], Yrs) 
        elif x == 4: 
            ty4 = LkCount(lk[x], Yrs) 
        else: 
            ty5 = LkCount(lk[x], Yrs) 
            
    return ty0, ty1, ty2, ty3, ty4, ty5

years = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']    
def CompDiachrony(verbose = True): 
    
    PREPNOUN, PREP_NOUN, PREPDETN, PREPDET_N, PREP_DETN, PREP_DET_N = findCompounds(ara, verbose=False)
    #l, prepnoun, prep_noun, prepdetn, prepdet_n, prep_detn, prep_det_n = [], [], [], [], [], [], []
    l = []
    l.append(PREPNOUN) #l[0]
    l.append(PREP_NOUN) #l[1]
    l.append(PREPDETN)
    l.append(PREPDET_N)
    l.append(PREP_DETN)
    l.append(PREP_DET_N)
    lk = [[], [], [], [], [], []]
    for x, y in enumerate(l): #y[0] tup / y[0][0] year
        for e in y: #('2016', 'fwest', 'فوسط', 'PREP+NOUN')
            lk[x].append(e[0]) # is the year

    tot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    for x, y in enumerate(lk): 
        for t, yy in enumerate(years):
            tt = lk[x].count(yy)
            tot[t] += tt
            
    Ygr = [tot[0]+tot[1]+tot[2]+tot[3]+tot[4]+tot[5], tot[6]+tot[7]+tot[8]+tot[9], tot[10]+tot[11]+tot[12], tot[13]+int(tot[14]/2), int(tot[14]/2)+tot[15] ]
    Yrs = [['2005', '2006', '2007', '2008', '2009', '2010'], ['2011', '2012', '2013', '2014'], ['2015', '2016', '2017'], ['2018', '2019'], ['2019','2020']]  
 
    
    if verbose:
        n = ['PREPNOUN', 'PREP_NOUN', 'PREPDETN', 'PREPDET_N', 'PREP_DETN', 'PREP_DET_N']
    
    
        ty0, ty1, ty2, ty3, ty4, ty5 = TypesCount(lk, Yrs)
        ty = [ty0, ty1, ty2, ty3, ty4, ty5]
    
        print('\n________Diachronic Analyses of PP types________\n')
        
        for l in range(len(ty)): 
            print(f'Type{l} presents:\n') 
            
            for x in range(len(Yrs)):
                           
                print(f'\t{round(int(ty[l][x])*100/Ygr[x],2)}% occurrences of {n[l]} in {Yrs[x][0]}-{Yrs[x][-1]}')#, means {round(lk[x].count(yy)*100/tot[p],2)}%') #on the total occurrences of this type of scheme
            print('\n')
    
    
        
    return lk

#lk contains 6lists of years: 
    
# lk[0] = years of PREPNOUN     #type0
# lk[1] = years of PREP_NOUN    #type1
# lk[2] = years of PREPDETN     #type2
# lk[3] = years of PREPDET_N    #type3
# lk[4] = years of PREP_DETN    #type4
# lk[5] = years of PREP_DET_N   #type5


#__________________PEARSON CHI2________________________________________________


def PearsonData(): 
    year = []
    typ = []
    lk = CompDiachrony(verbose = False)
    for x, y in enumerate(lk): 
        for z, w in enumerate(lk[x]):
            year.append(int(w))
            typ.append(x)
            
    Pdf= pd.DataFrame({'Y':year,'T':typ})
    
    return Pdf

def PearsonChi2(verbose = True): 
    # years and kind of PP 
    pdf = PearsonData()
    x_ = pdf['Y']
    y_ = pdf['T']

    contigency= pd.crosstab(x_, y_)
    contigency_pct= pd.crosstab(x_, y_, normalize='index')
    chi2, p_value, dof, expected = chi2_contingency(contigency)

    
    if p_value < 0.05: 
        p = 'significant'
    else: 
        p = 'not significant'
    
    if verbose:     
        print('The Pearson’s chi-square test between years and kind of PP presents a p-value (of '+str(round(p_value, 4))+') which is '+p+'\n')



# =============================================================================         
# ---------------------------------------------------------------------
# |  Diachronic distribution of Det+N                                 |
# |  (where N starts with a coronal consonant)                        |
# ---------------------------------------------------------------------

# The function iterate on POS columns to detect idx.DET+N or idx.DET+idx.N 
# if the N in words starts with a coronal it is added to the list of NP 
# with det's assimilation else it is added to the other list.

# tuples contains info on each word in Arabic script, in Arabizi and the POS 
# tup = (idx, Arabic-script word, Arabizi word, POS)

def nominalPhrases(): 
    nope = ['NOUN_QUANT', 'NOUN_NUM', 'NOUN_PROP']
    idx_lis=[]
    for x, y in enumerate(pos):
        if 'DET+N' in y:
            if 'NOUN_' not in y:
                tup = (x, toks[x], ara[x], pos[x])               
                if tup not in idx_lis:
                    idx_lis.append(tup)
                    
        elif 'DET' in y and 'NOUN' not in y:
            try:
                if 'NOUN' in pos[x+1]: 
  
                    if 'NOUN_' not in pos[x+1]:  
                        tup = (x, toks[x]+'#'+toks[x+1], ara[x]+'#'+ara[x+1], pos[x]+'#'+pos[x+1])
                        if tup not in idx_lis:
                            idx_lis.append(tup)
                
                                
            except: IndexError
    
    return idx_lis 


def Write(y, f, Cor = True):
    

    if Cor: 
        for x in y:
            f.write(str(x)+'\t')
        f.write('\n')
    else:
        for x in y:
            f.write(str(x)+'\t')
        f.write('\n')
        
    

#The function select only Arabizi words that present assimilation
#and write a txt file with them

def Coronal(): 
    idx_lis = nominalPhrases() 
    
    
    Cor_file = path+'\\Coronals.txt'
    NotCor_file = path+'\\NotCoronals.txt'
    fCor = open(Cor_file, 'w', encoding='utf-8') 
    fCor.write('idx\ttok\tarabish\tpos\tanalysis\n')
    fNCor = open(NotCor_file, 'w', encoding='utf-8')
    fNCor.write("idx\ttok\tarabish\tpos\n")
    for x, y in enumerate(idx_lis): 
        w = y[1]
        
        if 'ال+' in w:
            w_ = w.split('ال+')
            if w_[-1][0] in solar: 
                Write(y, fCor, Cor = True)
    
            else: 
                Write(y, fNCor, Cor = False)
        else: 
            w_ = w.split('ال#')

            if w_[-1][0] in solar: 
                Write(y, fCor, Cor = True)
    
            else: 
                Write(y, fNCor, Cor = False)

        
    fCor.close() 
    fNCor.close() 

#Coronal() un comment this command to print a txt file with all the NP which include Ns starting with a coronal                                     
#Txt file has been manually checked and:
#if assimilation has been represented in Arabizi, the phrase has been markes with _yes
#if assimilation has not been represented in Arabizi, the phrase has been marked with _no
#if determiner is absent in Arabizi, the phrase has been marked with _abs

#The file with sentences manually checked (annotated_coronals.tsv) is uploaded
def Analysisupload(filename="", path = path):
    tsv = path+filename
    df = pd.read_csv(tsv, sep="\t", encoding='utf-8').astype(str)
    
    idx = list(df['idx'])
    tok = list(df['tok'])
    arabish = list(df['arabish'])
    pos = list(df['pos'])
    analysis = list(df['analysis'])


    return df, idx, tok, arabish, pos, analysis
            
#The information within the file annotated_coronals.tsv are counted
def Count(ss): 
    prep = []
    space = []
    for x, y in enumerate(ss): 
        p = y[-1]
        if 'PREP' in p: 
           prep.append(y)
    
    for x, y in enumerate(ss): 
        p = y[-1]
        if '#' in p: 
            space.append(y)
     
    return prep, space
           

def Analyze(): #internal analysis of NPs with coronals 
    d_analyzed, idx, tok, arabish, pos, analysis = Analysisupload(filename="\\annotated_Coronals.tsv", path = path)
    #yes = analysis.count('_yes') #269 |  #no = analysis.count('_no') #190 | #ab = analysis.count('_abs') #19

    ss = []
    nn = []
    for x, y in enumerate(analysis): 
        if y == '_yes': 
            ss.append((idx[x], tok[x], arabish[x], pos[x]))
        if y == '_no':
            nn.append((idx[x], tok[x], arabish[x], pos[x]))
    
    prepSS, spaceSS = Count(ss) #len: 70 / 10
    # the syntagmas that assimilate (269) have 70 occurrences part of a PP and 10 (3.7%) occurrences where there is a graphic space between det and n
    prepNN, spaceNN = Count(nn) #len: 65 / 169
    # the syntagmas that do not assimilate (190) present 65 occurrences part of a PP and 169 (88.9%) occurrences where there is a graphic space between det and n

    return prepSS, spaceSS, prepNN, spaceNN, ss, nn


 
def PearsonDataPP(): 
    prepSS, spaceSS, prepNN, spaceNN, ss, nn = Analyze()
    typ1 = prepNN+spaceNN #type where there is no rendering of assimilation
    typ2 = prepSS+spaceSS #type where there is rendering of assimilation

    prep = [] #1 = part of a PP / 0 = not part of a PP
    typ = [] #1 = typ1 / 2 = typ2 
    
    for x, y in enumerate(typ1): 
        p = typ1[x][-1]
        if 'PREP' in p:
            prep.append(1)
            typ.append(1)
        else: 
            prep.append(0)
            typ.append(1)
            
    for x, y in enumerate(typ2): 
        p = typ2[x][-1]
        if 'PREP' in p:
            prep.append(1)
            typ.append(2)
        else: 
            prep.append(0)
            typ.append(2)
                
            
        PPdf= pd.DataFrame({'PP':prep,'T':typ})
    
    return PPdf


def PearsonChi2PP(verbose = True):
    #assimilation rendering and participation of PP
    ppdf = PearsonDataPP()
    x_ = ppdf['PP']
    y_ = ppdf['T']

    contigency= pd.crosstab(x_, y_)
    contigency_pct= pd.crosstab(x_, y_, normalize='index')
    chi2, p_value, dof, expected = chi2_contingency(contigency)
    
    if p_value < 0.01: 
        p = 'significant'
    else: 
        p = 'not significant'
    
    if verbose:     
        print('The Pearson’s chi-square test between assimilation rendering and participation of PPs presents a p_value of ('+str(round(p_value, 3))+') being thus '+p)



def PearsonDataSP(): 
    prepSS, spaceSS, prepNN, spaceNN, ss, nn = Analyze()
    typ1 = prepNN+spaceNN # In this type falls the PP with graphical rendering of det's assimilation
    typ2 = prepSS+spaceSS # In this type falls the PP without graphical rendering of det's assimilation

    space = [] #1 = DET_N / 0 = DETN
    typ = [] #1 = typ1 / 2 = typ2 
    
    for x, y in enumerate(typ1): 
        p = typ1[x][-1]
        if '#' in p:
            space.append(1)
            typ.append(1)
        else: 
            space.append(0)
            typ.append(1)
            
    for x, y in enumerate(typ2): 
        p = typ2[x][-1]
        if '#' in p:
            space.append(1)
            typ.append(2)
        else: 
            space.append(0)
            typ.append(2)
                
            
        spdf= pd.DataFrame({'Sp':space,'T':typ})
        
    # Pie chart for table 1.17-NP where Det is assimilated:
    labels = 'Det-assimilated+N', 'Det-assimilated N'
    sizes = [96.3, 3.7]
    explode = (0, 0.1)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    
    # Pie chart for table 1.17-NP where Det is not assimilated:
    labels = 'Det+N', 'Det N'
    sizes = [11.09, 88.9]
    explode = (0, 0.1)   
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  
    
    plt.show()
    
    return spdf


        
def PearsonChi2SP(verbose = True):
    
    spdf = PearsonDataSP()
    x_ = spdf['Sp']
    y_ = spdf['T']
    contigency= pd.crosstab(x_, y_)
    contigency_pct= pd.crosstab(x_, y_, normalize='index')
    chi2, p_value, dof, expected = chi2_contingency(contigency)
    if p_value < 0.01: 
        p = 'significant'
    else: 
        p = 'not significant'
        
    print('The Pearson’s chi-square test between assimilation (rendered or not) and the space before the N presents a p_value ('+str(round(p_value, 2))+') which is '+p)




#_______DIACHRONIC ANALYSIS OF DPs WITH AND WITHOUT ASSIMILATION_______

def diachronicAssim(verbose= True): 
    
    Yrs = [['2005', '2006', '2007','2008'], ['2009', '2010', '2011'], ['2012','2013'], ['2014', '2015', '2016'], ['2017', '2018', '2019'], ['2019','2020']]  

    _, _, _, _, ss, nn = Analyze()  #coronals which assimilate and coronals which do not
    ssd = []
    nnd = []
    Stot2019 = 0
    Ntot2019 = 0
    for x, y in enumerate(ss): 
        d = date[int(y[0])]
        if d.isnumeric() == True:
            d = d[:4]
            if d == '2019':
                Stot2019 += 1
            for ix, iy in enumerate(Yrs):
                if d != '2019' and d in iy: 
                    ssd.append(Yrs[ix])
        else: 
            d = d[-4:]

            for ix, iy in enumerate(Yrs):
                if d != '2019' and d in iy: 
                    ssd.append(Yrs[ix])
    
    
    for x in range(int(Stot2019/2)): 
        ssd.append(Yrs[-2])
        ssd.append(Yrs[-1])

    for x, y in enumerate(nn): 
        d = date[int(y[0])]
        if d.isnumeric() == True:
            d = d[:4]
            if d == '2019':
                Ntot2019 += 1
            for ix, iy in enumerate(Yrs):
                if d != '2019' and d in iy: 
                    nnd.append(Yrs[ix])
        else: 
            d = d[-4:]

            for ix, iy in enumerate(Yrs):
                if d != '2019' and d in iy: 
                    nnd.append(Yrs[ix])
    
    for x in range(int(Ntot2019/2)+1): 
        nnd.append(Yrs[-2])
        nnd.append(Yrs[-1])
        
    if verbose:
        print('Diachronic % of assimilated and not-assimilated DETs:\n')
        for x, y in enumerate(Yrs):
            tot = ssd.count(y)+nnd.count(y)

            
            print(f'in {y[0]}-{y[-1]} (tot of {tot}) - assimilated: {round(ssd.count(y)*100/tot, 2)}%, not-assimilated: {round(nnd.count(y)*100/tot,2)}%')
            
    return ssd, nnd


def PearsonDataY(): 
    typ2, typ1 = diachronicAssim(verbose= False)
    #typ1 type where there is no rendering of assimilation
    #typ2 type where there is rendering of assimilation

    yy = [] #years group list
    typ = [] #1 = nnd/ 2 = ssd
    
    for x, y in enumerate(typ1): 
        typ.append(1)
        yy.append(int(y[0]))
            
    for x, y in enumerate(typ2): 
        typ.append(2)
        yy.append(int(y[0]))
            
        ypdf= pd.DataFrame({'Y':yy,'T':typ})
    
    return ypdf

def PearsonChi2Y(verbose = True):
    #dependence between graphical assimilation and years data
    ypdf = PearsonDataY()
    x_ = ypdf['Y']
    y_ = ypdf['T']
    contigency= pd.crosstab(x_, y_)
    contigency_pct= pd.crosstab(x_, y_, normalize='index')
    chi2, p_value, dof, expected = chi2_contingency(contigency)
    
    if p_value < 0.01: 
        p = 'significant'
    else: 
        p = 'not significant'
        
    print('\nThe Pearson’s chi-square test of graphical assimilation and years has a '+p+' p_value (of '+str(round(p_value, 2))+')')



#____________DIACHRONIC ANALYSIS OF DPs WITH AND WITHOUT ASSIMILATION + Genre_____________

def MetaAssim(verbose= True): 
 
    _, _, _, _, ss, nn = Analyze() 
    ssMF, nnMF = [], []
    ssLOC, nnLOC = [], []
    ssAge, nnAge = [], []
    for x, y in enumerate(ss): 
        g = gend[int(y[0])]
        if g != '/' or g != 'nan':
            ssMF.append(g)

    for x, y in enumerate(nn): 
        g = gend[int(y[0])]
        if g != '/' or g != 'nan':
            nnMF.append(g)

    for x, y in enumerate(ss): 
        l = loc[int(y[0])]
        if l != '/' or l != 'nan':
            ssLOC.append(l)
    
    for x, y in enumerate(nn): 
        l = loc[int(y[0])]
        if l != '/' or l != 'nan':
            nnLOC.append(l)
            
    for x, y in enumerate(ss): 
        a = age[int(y[0])]
        if a != '/' or a != 'nan':
            ssAge.append(a)
            
    for x, y in enumerate(nn): 
        a = age[int(y[0])]
        if a != '/' or a != 'nan':
            nnAge.append(a)
    
    ages, gender= ['-25', '25-35', '35-50', '50+'], ['M', 'F']
    if verbose: 
        print("\nDistribution of det's assimilation through ages:\n")
        for x, y in enumerate(ages):
            print(f'\tfor age {y} - assimilated: {round(ssAge.count(y)*100/(ssAge.count(y)+nnAge.count(y)), 2)}%, not-assimilated: {round(nnAge.count(y)*100/(ssAge.count(y)+nnAge.count(y)), 2)}%')
        # Pie chart for table 1.17-age and assimilation:
            labels = f'{y}Gr', f'{y}notGr'
            sizes = [round(ssAge.count(y)*100/(ssAge.count(y)+nnAge.count(y)), 2), round(nnAge.count(y)*100/(ssAge.count(y)+nnAge.count(y)), 2)]
                 
            explode = (0, 0)  
        
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
            plt.show()
        print("\nDistribution of det's assimilation through gender:\n")
        for x, y in enumerate(gender):
            print(f'\tfor gender {y} - assimilated: {round(ssMF.count(y)*100/(ssMF.count(y)+nnMF.count(y)), 2)}%, not-assimilated: {round(nnMF.count(y)*100/(ssMF.count(y)+nnMF.count(y)), 2)}%')
            # Pie chart for table 1.17-age and assimilation:
            labels = f'{y} - Gr', f'{y} - not Gr'
            sizes = [round(ssMF.count(y)*100/(ssMF.count(y)+nnMF.count(y)), 2), round(nnMF.count(y)*100/(ssMF.count(y)+nnMF.count(y)), 2)]
                 
            explode = (0, 0)  
        
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
            ax1.axis('equal')  
        
            plt.show()
    return ssMF, nnMF, ssLOC, nnLOC, ssAge, nnAge
           

def PearsonDataMeta(): 
    ssMF, nnMF, _, _, ssAge, nnAge =  MetaAssim(verbose = True) 

    MF = [] #list of genres 1 = M / 2 = F
    Age = [] #list of ages: 1 = -25, 2= 25-35, 3= 35-50, 4= 50+
    
    typMF = [] #1 = nnMF/ 2 = ssMF
    typAGE = [] #1 = nnAGE/ 2 = ssAGE
    
    for x, y in enumerate(ssMF): 
        if y == 'M':
            MF.append(1)
            typMF.append(2)
        elif y == 'F':
            MF.append(2)
            typMF.append(2)
            
    for x, y in enumerate(nnMF): 
        if y == 'M':
            MF.append(1)
            typMF.append(1)
        elif y == 'F':
            MF.append(2)
            typMF.append(1)
            
    for x, y in enumerate(ssAge): 
        if y == '-25':
            Age.append(1)
            typAGE.append(2)
        elif y == '25-35':
            Age.append(2)
            typAGE.append(2)
        elif y == '35-50':
            Age.append(3)
            typAGE.append(2)
        elif y == '50+':
            Age.append(4)
            typAGE.append(2)
            
    for x, y in enumerate(nnAge): 
        if y == '-25':
            Age.append(1)
            typAGE.append(1)
        elif y == '25-35':
            Age.append(2)
            typAGE.append(1)
        elif y == '35-50':
            Age.append(3)
            typAGE.append(1)
        elif y == '50+':
            Age.append(4)
            typAGE.append(1)
            
    Gpdf= pd.DataFrame({'G':MF,'T':typMF})
    Apdf= pd.DataFrame({'A':Age,'T':typAGE})
    
    
    return Gpdf, Apdf

def PearsonChi2Meta():
    
    Gpdf, Apdf = PearsonDataMeta()
    xG = Gpdf['G']
    yG = Gpdf['T']
    xA = Apdf['A']
    yA = Apdf['T']
    Acontigency= pd.crosstab(xA, yA)
    chi2, p_value, dof, expected = chi2_contingency(Acontigency)
    
    Gcontigency= pd.crosstab(xG, yG)
    Gchi2, Gp_value, dof, expected = chi2_contingency(Gcontigency)

    
    if p_value < 0.05: 
        p = 'significant'
        
    else: 
        p = 'not significant'
        
    if Gp_value < 0.05: 
        Gp = 'significant'
        
    else: 
        Gp = 'not significant'
                
    
    print(f'\nThe Pearson’s chi-square test of gender data presents a p_value is {Gp}, being: {round(Gp_value, 2)}')
    print(f'\nThe Pearson’s chi-square test of age data presents a p_value is {p}, being: {round(p_value, 2)}')


#Percentages() #To visualize the arithmographemes precentages, uncomment this command and run the file

#lk = CompDiachrony(verbose = True) #To visualize the PP patterns uncomment this command and run
#PearsonChi2(verbose = True)   #To visualize the Pearson coeff. between years and PP patterns uncomment this command and run

#PearsonChi2PP(verbose = True)  #To visualize the Pearson coef between assimilation rendering and participation of a PP run this command 
#PearsonChi2SP(verbose = True) # -0.80285419 To plot (and table 1.17)


#ssd, nnd =  diachronicAssim(verbose = True) #To visualize GR diachronic percentages (table 1.18), run this command
#PearsonChi2Y(verbose = True) #To visualiza the correlation between graphical assimilation and years     

#PearsonChi2Meta() #To visualize the diastratic percentages uncomment this command and run






        

 
