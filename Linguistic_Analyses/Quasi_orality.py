# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 17:20:49 2021

@author: Elisa
"""
#==============================================================================
#           Prepositional Phrase (Quasi-Orality Analyses)
#==============================================================================

# -----------------------------------------------------------------------------
# |                      DATA INFORMATION                                     |
# -----------------------------------------------------------------------------
# | This script is set to work on the tarc data totality (file tarc.tsv)      |                                                                      |
# -----------------------------------------------------------------------------
import argparse
import pandas as pd 
import matplotlib.pyplot as plt
path = r""


def upload(filename="", path = path):
    tsv = path+filename
    df = pd.read_csv(tsv, sep="\t", encoding='utf-8').astype(str)
    words = list(df['CODA'])
    ara = list(df['arabish'])
    toks = list(df['token'])
    pos = list(df['pos'])
    
    return df, words, toks, ara, pos 
        


# =============================================================================         
# ---------------------------------------------------------------------
# |  To get the list of percentages of the various realizations       |
# |  of Prepositional Phrases made of Prep+(det+)N                    |
# ---------------------------------------------------------------------

def extraRemoving(l, nope, extra): 
    
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


def findCompounds(ara, pos, words, verbose=True):

    nope = ['<eos>', 'SYM', 'PUNC', 'NOUN_PROP', 'NOUN_QUANT', 'ADV',
            'REL_PRON' , 'REL_ADV', 'NEG_PART', 'DEM_PRON_3MP', 'DEM_PRON_3MS',
            'DEM_PRON_3FS', 'DEM_PRON', 'ABBREV', 'PRON_INDEF', 'CONJ', 
            'SUB_CONJ', 'FOCUS_PART']
    extra = []
    idxs = []
    
#__________________[PREP+N]____________________________________________________
    PREPNOUN = [] 
    for x, y in enumerate(pos): 
        if 'PREP+NOUN' in y: #'PREP+NOUN'
            tup = (ara[x], words[x], y)
            PREPNOUN.append(tup)
            
    PREPNOUN = extraRemoving(PREPNOUN, nope, extra)               
        
#__________________[PREP N]____________________________________________________
    PREP_NOUN = []
    for x, y in enumerate(pos): 
        if y == 'PREP' and 'DET' not in pos[x+1]:
            tup = (ara[x], ara[x+1], words[x], words[x+1], y, pos[x+1])
            PREP_NOUN.append(tup)
    
    PREP_NOUN = extraRemoving(PREP_NOUN, nope, extra)    

#__________________[PREP+DET+N]_______________________________________________   
    PREPDETN = [] 
    for x, y in enumerate(pos): 
        if 'PREP+DET+NOUN' in y: 
            tup = (ara[x], words[x], y)
            idxs.append(x)
            PREPDETN.append(tup)   
    
#__________________[PREP+DET N]_______________________________________________
    PREPDET_N = []
    for x, y in enumerate(pos): 
        if y == 'PREP+DET' and 'NOUN' in pos[x+1]: 
            tup = (ara[x], ara[x+1], words[x], words[x+1], y, pos[x+1])
            PREPDET_N.append(tup)
      
    PREPDET_N = extraRemoving(PREPDET_N, nope, extra)    

    for x, y in enumerate(PREPDET_N):
        idxs.append(ara.index(PREPDET_N[x][1]))
     
    
#__________________[PREP DET+N]_______________________________________________
    PREP_DETN = []
    for x, y in enumerate(pos): 
        if y == 'PREP' and 'DET+NOUN' in pos[x+1]: 
            tup = (ara[x], ara[x+1], words[x], words[x+1], y, pos[x+1])
            PREP_DETN.append(tup)
    
    PREP_DETN = extraRemoving(PREP_DETN, nope, extra)    

    for x, y in enumerate(PREP_DETN):
        idxs.append(ara.index(PREP_DETN[x][1]))
    
    
#__________________[PREP DET N]________________________________________________
    PREP_DET_N = []
    for x, y in enumerate(pos): 
        if y == 'PREP' and pos[x+1] == 'DET': 
            if 'NOUN' in pos[x+2]:
                tup = (ara[x], ara[x+1], ara[x+2], words[x], words[x+1], words[x+2], y, pos[x+1], pos[x+2])
                PREP_DET_N.append(tup)
    
    PREP_DET_N = extraRemoving(PREP_DET_N, nope, extra)           

    for x, y in enumerate(PREP_DET_N):
        idxs.append(ara.index(PREP_DET_N[x][2]))
    
    if verbose:
        tot_no_det = len(PREPNOUN) + len(PREP_NOUN) 
        tot =  len(PREPDETN) + len(PREPDET_N) + len(PREP_DETN) + len(PREP_DET_N)
        print(f'___________________________________________________________________\n'
              f'                                                    \n'
              f'The different types of prepositional phrases have the following frequencies: \n\n'
              f'[PREP+N]: {round(len(PREPNOUN)*100/tot_no_det,2)}%,\n'
              f'[PREP N]: {round(len(PREP_NOUN)*100/tot_no_det,2)}%,\n\n' 
              f'[PREP+DET+N]: {round(len(PREPDETN)*100/tot,2)}%,\n' 
              f'[PREP+DET N]: {round(len(PREPDET_N)*100/tot,2)}%,\n' 
              f'[PREP DET+N]: {round(len(PREP_DETN)*100/tot,2)}%,\n' 
              f'[PREP DET N]: {round(len(PREP_DET_N)*100/tot,2)}%\n')
        
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = '[PREP+DET+N]', '[PREP+DET N]', '[PREP DET+N]', '[PREP DET N]'
        sizes = [round(len(PREPDETN)*100/tot,2), round(len(PREPDET_N)*100/tot,2), round(len(PREP_DETN)*100/tot,2), round(len(PREP_DET_N)*100/tot,2)]
        explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. '[PREP+DET N]')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()
        
        labels = '[PREP+N]', '[PREP N]'
        sizes = [round(len(PREPNOUN)*100/tot_no_det,2), round(len(PREP_NOUN)*100/tot_no_det,2)]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. '[PREP N]')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()
        
    return PREPNOUN, PREP_NOUN, PREPDETN, PREPDET_N, PREP_DETN, PREP_DET_N, idxs
     
# =============================================================================         
# ---------------------------------------------------------------------
# |  To observe the internal composition of the different types of    |
# |  Prepositional Phrases (what kind of preposition are composed of) |
# ---------------------------------------------------------------------

def internalComposition(p):    
    dic = {}
    for x in range(len(p)): 
        c = p[x][0].split('+')
        if c[0] == 'و': 
            try:
                if c[1] not in dic.keys():
                    dic[c[1]] = 1
                else: 
                    dic[c[1]] += 1 
            except: IndexError
            
        elif c[0] not in dic.keys():
            dic[c[0]] = 1
        else: 
            dic[c[0]] += 1 
    
    print(f'___________________________________________________________________\n'
          f'                                                    \n'
          f'The prepositions that compose the selected PP type\n' 
          f'and the number of their occurrences are as follows:\n\n' 
          f'{dic}\n'
          f'___________________________________________________________________')

#==============================================================================

# --------------------------------------------------------------------------------
# | Based on the internal composition to be investigated, insert the type of the |
# | syntagma in place of ***pp1*** (in line 196). For matches, refer to the      |
# | reference table below.                                                       |
# --------------------------------------------------------------------------------

def starter(ara, toks, pos, words, Composition=False, PP= False, codeSw = False, compound=None):
    
    # To get the list of percentages of the various realizations
    if PP: 
        if codeSw:
            p1, p2, p3, p4, p5, p6, idx = findCompounds(ara, pos, words, verbose = False)
        else: 
            p1, p2, p3, p4, p5, p6, idx = findCompounds(ara, pos, words, verbose = True)

                
        
        return p1, p2, p3, p4, p5, p6, idx

    # To investigate the internal structure of the various realizations
    if Composition: 

        pp1, pp2, pp3, pp4, pp5, pp6, _ = findCompounds(toks, pos, words, verbose= False) 
        if compound == 'pp6':
            compound = pp6
        elif compound == 'pp5':
            compound = pp5
        elif compound == 'pp4':
            compound = pp4
        elif compound == 'pp3':
            compound = pp3
        elif compound == 'pp2':
            compound = pp2
        else: 
            compound = pp1
            
        internalComposition(compound) 
        
        return pp1, pp2, pp3, pp4, pp5, pp6, _ 


# ===============================================================================
#                        -------------------
#                        | REFERENCE TABLE |
#                        -------------------
                        
#                         p1/pp1 [PREP+N] 
#                         p2/pp2 [PREP N]

#                         p3/pp3 [PREP+DET+N] 
#                         p4/pp4 [PREP+DET N] 
#                         p5/pp5 [PREP DET+N] 
#                         p6/pp6 [PREP DET N]

# =:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:==:=:=:=:=:=:=:=:=:=:=:=:=
#                      ***p1 structure sample*** 
    
# ('arabizi', 'word', 'POS') = [('bou9alb', 'بوقلب', '[PREP+NOUN]ADJ'), (...)

# =:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:==:=:=:=:=:=:=:=:=:=:=:=:=
#      ***pp1 structure sample (mirrored reading for Arabic tokens)***
    
# ('tokenization', 'word', 'POS') = [('بو+قلب', 'بوقلب', '[PREP+NOUN]ADJ'), (...)
# ================================================================================


def main():
    parser = argparse.ArgumentParser(description="Script description. Use --pp to specify the pattern to observe the composition. If no arguments are provided, PP schemes percentages will be visualized by default. \n-------------------\n| REFERENCE TABLE |\n-------------------\n pp1=>[PREP+N]\n pp2=>[PREP N]\n pp3=>[PREP+DET+N]\n pp4=>[PREP+DET N]\n pp5=>[PREP DET+N]\n pp6=>[PREP DET N]\n")
    parser.add_argument("--pp", choices=["pp1", "pp2", "pp3", "pp4", "pp5", "pp6"], help="Pattern to observe the composition")
    args = parser.parse_args()
      
    df, words, toks, ara, pos = upload(filename = "tarc.tsv", path = path)
    
    # To observe the internal composition
    if args.pp:
        if args.pp in ["pp1", "pp2", "pp3", "pp4", "pp5", "pp6"]:
            pp1, pp2, pp3, pp4, pp5, pp6, _ = starter(ara, toks, pos, words, Composition=True, compound=args.pp)
        else:
            print("Invalid pattern specified. Please choose from pp1, pp2, pp3, pp4, pp5, pp6.")
            return
    else:
    	#to observe the PP schemes percentages
        p1, p2, p3, p4, p5, p6, idxs = starter(ara, toks, pos, words, PP=True)

if __name__ == "__main__":
    main()
    

