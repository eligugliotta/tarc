# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 16:54:19 2021

@author: Elisa
"""
#==============================================================================
#          General Analyses (Text Genra Analyses) 
#==============================================================================

# -------------------------------------------------------------------------
# |                      DATA INFORMATION                                 |
# -------------------------------------------------------------------------
# | This script is set to work on the tarc data totality (file tarc.tsv)  |
# -------------------------------------------------------------------------
import pandas as pd 
import matplotlib.pyplot as plt
path1 = r""
from Trends import Analyze

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

def GenraSplit(): 
    SN, forum, blog = {'ara':[], 'pos':[]}, {'ara':[], 'pos':[]}, {'ara':[], 'pos':[]}
    
    for x, y in enumerate(tipo):
        if y == 'social':
            SN['ara'].append(ara[x])
            SN['pos'].append(pos[x])
        elif y == 'forum':
            forum['ara'].append(ara[x])
            forum['pos'].append(pos[x])
        elif y == 'blog':
            blog['ara'].append(ara[x])
            blog['pos'].append(pos[x])
            
    return SN, forum, blog

def Count(lis): 
    
    interj, emot, final_p = 0, 0, 0
    for x, y in enumerate(lis): 
        if y == 'emotag':
            emot += 1
        if 'INTERJ' in y: 
            interj += 1
        if y == '<eos>' and 'PUNC' in lis[x-1]:
            final_p += 1
            
    return interj, emot, final_p
        
def Write(): 
    SN, forum, blog = GenraSplit()
    
    Sinterj, Semot, Sfinal_p = Count(SN['pos'])
    Finterj, Femot, Ffinal_p = Count(forum['pos'])
    Binterj, Bemot, Bfinal_p = Count(blog['pos'])
    TS, TF, TB = Sinterj+Semot+Sfinal_p, Finterj+Femot+Ffinal_p, Binterj+Bemot+Bfinal_p
    
    print(f"Regarding Social Network data, tot = {len(SN['pos'])},\n-The total number of interjections is: {round(Sinterj*100/TS,2)}%,\n-The total number of emotags is: {round(Semot*100/TS,2)}%,\n-The total number of final punctuation is: {round(Sfinal_p*100/TS,2)}%,\n")
    print(f"Regarding forum data, tot = {len(forum['pos'])},\n-The total number of interjections is: {round(Finterj*100/TF,2)}%,\n-The total number of emotags is: {round(Femot*100/TF,2)}%,\n-The total number of final punctuation is: {round(Ffinal_p*100/TF,2)}%,\n")
    print(f"Regarding blog data, tot = {len(blog['pos'])},\n-The total number of interjections is: {round(Binterj*100/TB,2)}%,\n-The total number of emotags is: {round(Bemot*100/TB,2)}%,\n-The total number of final punctuation is: {round(Bfinal_p*100/TB,2)}%,")

    # Pie chart for table 4.11 Social:
    labels = 'Interj.', 'Emotags', 'Punc.'
    sizes = [round(Sinterj*100/TS,2), round(Semot*100/TS,2), round(Sfinal_p*100/TS,2)]
    explode = (0.1, 0.1, 0)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    
    # Pie chart for table 4.12 Forum:
    labels = 'Interj.', 'Emotags', 'Punc.'
    sizes = [round(Finterj*100/TF,2), round(Femot*100/TF,2), round(Ffinal_p*100/TF,2)]
    explode = (0.1, 0.1, 0)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    
    # Pie chart for table 4.13 Blog:
    labels = 'Interj.', 'Emotags', 'Punc.'
    sizes = [round(Binterj*100/TB,2), round(Bemot*100/TB,2), round(Bfinal_p*100/TB,2)]
    explode = (0.1, 0.1, 0)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
Write()       

#____________NP distibution___________________________
print('\nNominal Phrase distribution through text genders\n')

def reductio(): 
    forum = []
    blog = []
    social = []
    for x, y in enumerate(tipo):
        if y == 'blog': 
            blog.append(x)
    
    for x, y in enumerate(tipo): 
        if y == 'forum' and len(forum) < len(blog): 
            forum.append(x)
            
    for x, y in enumerate(tipo):
        if y == 'social' and len(social) < len(blog):
            social.append(x)
    
    return forum, blog, social


#the function returns 3 lists of indices of the same length as the blogs for the three types
def File(social, forum, blog): 
    #social, forum, blog, _ = find()
    
    file = path1+'\\textgenre_NPdistribution.txt'
    
    f = open(file, 'w', encoding='utf-8')
    f.write('The following are the NPs of tipe [prep+det n] found in blogs:\n\n')
    for x, y in enumerate(blog): 
        f.write(f'<idx: {y[0]}> <NP: {y[2]}> <POS: {y[3]}>\n\n')
    
    f.write('\n\t***********************************************\n')
    f.write('The following are the NPs of tipe [prep+det n] found in social:\n\n')
    for x, y in enumerate(social): 
        f.write(f'<idx: {y[0]}> <NP: {y[2]}>  <POS: {y[3]}>\n\n')
        
    f.write('\n\t***********************************************\n')
    f.write('The following are the NPs of tipe [prep+det n] found in forums:\n\n')
    for x, y in enumerate(forum): 
        f.write(f'<idx: {y[0]}> <NP: {y[2]}>  <POS: {y[3]}>\n\n')
   
    
    f.close() 

def find():
    #prepSS, spaceSS, prepNN, spaceNN = Analyze()
    forum, blog, social = reductio()
    _, spaceSS, _, spaceNN, _, _ = Analyze()
    s, f, b, n = [], [], [], []
    #s1, f1, b1, n1 = [], [], [], []
    
    for x, y in enumerate(spaceNN): 
        if int(spaceNN[x][0]) in social:
            s.append(y)
        elif int(spaceNN[x][0]) in forum:
            f.append(y)
        elif int(spaceNN[x][0]) in blog:
            b.append(y)
        else: 
            n.append(y)
            
    print(f' NP in social: {round(len(s)*100/len(spaceNN),2)}%,\n NP in forums: {round(len(f)*100/len(spaceNN),2)}%,\n NP in blogs: {round(len(b)*100/len(spaceNN),2)}%')
    File(s, f, b)
    
    # Pie chart for table 4.37 DP with space:
    labels = 'Social', 'Forum', 'Blog', 'Others'
    sizes = [round(len(s)*100/len(spaceNN),2), round(len(f)*100/len(spaceNN),2), round(len(b)*100/len(spaceNN),2), round(len(n)*100/len(spaceNN),2) ]
    explode = (0, 0, 0.1, 0)  # only "explode" the 2nd slice 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    return s, f, b, n

s, f, b, n = find() 


