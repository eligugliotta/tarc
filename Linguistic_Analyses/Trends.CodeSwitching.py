# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 10:58:09 2021

@author: Elisa
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 16:13:32 2021

@author: Elisa
"""
#==============================================================================
#               Code-switching (Trends Analyses)
#==============================================================================

# -----------------------------------------------------------------------------
# |                      DATA INFORMATION                                     |
# -----------------------------------------------------------------------------
# | This script is set to work on the tarc data totality (file tarc.tsv)      |
# -----------------------------------------------------------------------------
import pandas as pd 
path = r""
from scipy.stats import chi2_contingency
from Quasi_orality import starter

def upload(filename="", path = path):
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
        
# ============================================================================= 

def Bounds(tokenIDX, pos):
    i = 1
    stop = 0
    b = []
    while stop == 0:        
        if pos[tokenIDX-i] == '<eos>': 
            b.append(tokenIDX-i)
            i = 1 
            stop = 1
        else: 
            i+=1 
            
    while stop == 1:       
        if pos[tokenIDX+i] == '<eos>':
            b.append(tokenIDX+i)
            i = 1
            stop += 1
        else:
            i+=1
      
    return b[0], b[1]

def DetFor(pos): 
    idxLis = []
    count = 1
    for x, y in enumerate(pos):
        y = y.split('+')
        if 'DET' in y and 'foreign' in pos[x+1]: 
            if 'NOUN' not in y: 
                if len(y) == 1:
                    start, end = Bounds(x, pos)
                    idxLis.append((x, start,end))                
                if len(y) <= 2 and y[0] == 'PREP': 
                    start, end = Bounds(x, pos)
                    idxLis.append((x, start,end, count))
                    count += 1
                if pos[x-1] == 'PREP': 
                    start, end = Bounds(x, pos)
                    idxLis.append((x, start,end, 'p',count))
                    count += 1
        
    return idxLis

 
            
def Write():
    idxLis = DetFor(pos)
    output_file = path+'\\Det_followed_by_foreign.txt'
    f = open(output_file, 'w', encoding='utf-8')
    count = 1
    met = {}
    met['origin'], met['age'], met['gend'] = [], [], []
    for x, y in enumerate(idxLis): 
        sent = range(y[1]+1,y[2])
        if len(y) == 4: 
            c = y[-1]
            f.write(f'{count}. PP({c}). <Mixed PP: [{ara[y[0]]} {ara[y[0]+1]}]> <POS: {pos[y[0]]}_{pos[y[0]+1]}>\n<TArC idx: {y[0]}-{y[0]+1}>\n<Within sentence: ')
        elif len(y) == 5: 
            c, a = y[-1], 'PREP_'
            f.write(f'{count}. PP({c}).  <Mixed PP: [{ara[y[0]-1]} {ara[y[0]]} {ara[y[0]+1]}]> <POS: {a}{pos[y[0]]}_{pos[y[0]+1]}>\n<TArC idx: {y[0]}-{y[0]+1}>\n<Within sentence: ')

        else: 
            f.write(f'{count}. <Mixed NP: [{ara[y[0]]} {ara[y[0]+1]}]> <POS: {pos[y[0]]}_{pos[y[0]+1]}>\n<TArC idx: {y[0]}-{y[0]+1}>\n<Within sentence: ')
        count += 1
        for x in sent:       
            f.write(ara[x]+' ')
        f.write('>\n')
        f.write(f"<Genre: {df['TYPE'][y[0]]}>\n")
        f.write(f"<Users' metadata:> <origin:{loc[y[0]]}> <age:{age[y[0]]}> <gender:{gend[y[0]]}>\n")
        met['origin'].append(loc[y[0]])
        met['age'].append(age[y[0]])
        met['gend'].append(gend[y[0]])
        f.write('\n\n')
    return count, c, met
       
#met = Write() 

def Gov(met): 
    
    govlis = ['Ariana', 'Béja', 'Sousse', 'Bizerte', 'Gabès', 'Nabeul', 'Jendouba', 'Kairouan', 'Zaghouan', 'Kebili', 'El_Kef', 'Mahdia', 'Manouba', 'Medenine', 'Monastir', 'Gafsa', 'Sfax', 'Sidi_Bouzid', 'Siliana', 'Ben_Arous', 'Tataouine', 'Tozeur', 'Tunis', 'Kasserine']
    totGov = 0
    Govs = []
    
    for x in govlis: 
        n = met['origin'].count(x)
        if n != 0:
            totGov += n
            Govs.append((x, n))
    
    return Govs, totGov

def Age(met):
    agelis = ['-25', '25-35', '35-50', '50+']
    totAge = 0
    Ages = []
    for x in agelis: 
        n = met['age'].count(x)
        totAge += n
        Ages.append((x, n))
        
    return Ages, totAge


def Print(): 
    
    count, c, met = Write()
    print('_________________________________\n\nCode-Switching Analyses\nThe pattern Det_foreign have been selected\nResults are below:\n')
    print('_________________________________\nGovernatorate Percentages:\n_________________________________\n')

    Govs, totGov = Gov(met)                    
    for x in Govs:
        print(x[0]+':', str(round(x[1]*100/totGov,2))+'%')
                    
    print('_________________________________\nAge Percentages:\n_________________________________\n')
    
    Ages, totAge = Age(met)
    for x in Ages:
        print(x[0]+':', str(round(x[1]*100/totAge,2))+'%')
    
    print('_________________________________\nGender Percentages:\n_________________________________\n')
    
    print('Male:', str(round(met['gend'].count('M')*100/(met['gend'].count('M')+met['gend'].count('F')),2))+'%')
    
    print('Female:', str(round(met['gend'].count('F')*100/(met['gend'].count('M')+met['gend'].count('F')),2))+'%')
    
    
    print('_________________________________\nType Percentages:\n_________________________________\n')
    print("As shown in the generated file (Det_followed_by_foreign.txt):\nThe total number of NP is "+str(count-1)+" and "+str(c)+" of those make part of a PP.\nIn 111 occurrences the prep is graphically joined with the det.\nOnly in 25 occurrences the prep is separated from the det.\n")
    print("\n30 NP are in blog (means 10.8%),\n58 are in forum (means 20.9%),\n25 in social net. (means 8.99%),\n165 in rap lyrics. (means 59.35%)")
        
#Print()
    
#__________________PEARSON CHI2.________________________________________________


def PearsonData(ara, toks, pos, words): 
    _, _, _, _, _, _, idxsNCS = starter(ara, toks, pos, words, PP=True, codeSw = True) #lista di indici di tutti i PPs (dal QuasiOralityAnalisi file)
    idxLis = DetFor(pos)
    NPs = [] #Not-Code-Sw = 0, Code-Sw = 1
    Gen = [] #M =0, F =1, / = 2
    Txt = [] #Social =0, Forum =1, Blog =2 
    
    for x, y in enumerate(idxsNCS):
        NPs.append(0)
        if gend[y] == 'M':
            Gen.append(0)
        elif gend[y] == 'F': 
            Gen.append(1)
        else: Gen.append(3)
        
        if tipo[y] == 'facebook':
            Txt.append(0)
        elif tipo[y] == 'forum':
            Txt.append(1)
        elif tipo[y] == 'blog':
            Txt.append(2)
        else: Txt.append(3) #rap
    
    for z, w in enumerate(idxLis):
        NPs.append(1)
        if gend[w[0]] == 'M':
            Gen.append(0)
        elif gend[w[0]] == 'F': 
            Gen.append(1)
        else: Gen.append(3) # gener not recorded (/)
        
        if tipo[w[0]] == 'facebook':
            Txt.append(0)
        elif tipo[w[0]] == 'forum':
            Txt.append(1)
        elif tipo[w[0]] == 'blog': 
            Txt.append(2)
        else: Txt.append(3) #rap

    
    
    Pdf= pd.DataFrame({'Switching':NPs,'Sex':Gen, 'GenreTxt':Txt})
    
    for x in range(2):
        
        try:
        
            for x, y in enumerate(Gen):
                if y == 3: 
                    Pdf = Pdf.drop(index=x)
                    
            for x, y in enumerate(Txt):
                if y == 3:
                    Pdf = Pdf.drop(index=x)
    
        except KeyError:
            pass
    
    return Pdf

def PearsonChi2(ara, toks, pos, words, verbose = True, Gend = True):
    
    pdf = PearsonData(ara, toks, pos, words)
    if Gend:             
        x_ = pdf['Switching']
        y_ = pdf['Sex']
        
        contigency= pd.crosstab(x_, y_)
        #contigency_pct= pd.crosstab(x_, y_, normalize='index')
        chi2, p_value, dof, expected = chi2_contingency(contigency)
        #sns.heatmap(contigency, annot=True, cmap="YlGnBu")
        print('Sex', contigency)
    
        if p_value < 0.05: 
            p = 'significant'
        else: 
            p = 'not significant'
    

    else: 
        x_ = pdf['Switching']
        y_ = pdf['GenreTxt']
        
        contigency= pd.crosstab(x_, y_)
        #contigency_pct= pd.crosstab(x_, y_, normalize='index')
        chi2, p_value, dof, expected = chi2_contingency(contigency)
        print('GenreTxt', contigency)
        #sns.heatmap(contigency, annot=True, cmap="YlGnBu")
    
        if p_value < 0.05: 
            p = 'significant'
        else: 
            p = 'not significant' 
        
    if verbose: 
        
        #plt.scatter(x_,y_) 
        
        if Gend:   
            print(f'The Pearson’s chi-square test concerning code-switched NPs and gender gave a {p} p-value, being {round(p_value,2)}')
            #plt.ylabel("Sex")
        else: 
            print(f'The Pearson’s chi-square test concerning code-switched Nps and textual genre gave a {p} p-value, being {round(p_value, 2)}')
            #plt.ylabel("GenreTxt")
        #plt.xlabel("Switching")
        #plt.show() 


def main():

	df, date, words, ara, pos, toks, tipo, loc, age, gend  = upload(filename = "tarc.tsv", path=path)
	
	PearsonChi2(ara, toks, pos, words, verbose = True, Gend = True) #data dependence between code-switched NPs and Gender
	PearsonChi2(ara, toks, pos, words, verbose = True, Gend = False) # data dependence between code-switched NPs and textual gender

df, date, words, ara, pos, toks, tipo, loc, age, gend  = upload(filename = "tarc.tsv", path=path)
if __name__ == "__main__":
    main()
