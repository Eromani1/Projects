# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 16:58:21 2018

@author: Romani Edoardo
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 11:20:45 2018

@author: Romani Edoardo
"""

""" Loading necessary packages/modules"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st


"""Fetching data"""
url = 'https://www.basketball-reference.com/leagues/NBA_2018_totals.html'
r = requests.get(url)
r_html = r.text

"""Extracting raw player_stats data"""
soup = BeautifulSoup(r_html,'html.parser')
table=soup.find_all(class_="full_table")

""" Extracting List of column names"""
head=soup.find(class_="thead")
column_names_raw=[head.text for item in head][0]
column_names_polished=column_names_raw.replace("\n",",").split(",")[2:-1]


"""Extracting full list of player_data"""
players=[]

for i in range(len(table)):
    
    player=[]
    
    for td in table[i].find_all("td"):
        player.append(td.text)

    players.append(player)
    
    
"""Creating Player Dictionary"""  
    
player_dict={}


Player=[x[0] for x in players]
Pos=[x[1] for x in players]
Age=[int(x[2]) for x in players]
Tm=[x[3] for x in players]
G=[int(x[4]) for x in players] 
GS=[int(x[5]) for x in players] 
MP=[float(x[6]) for x in players]
FG=[float(x[7]) for x in players]
FGA=[float(x[8]) for x in players]
FG_perc=[x[9] for x in players]
Three_point=[float(x[10]) for x in players]
Three_point_A=[float(x[11]) for x in players]
Three_point_perc=[x[12] for x in players]
Two_point=[float(x[13]) for x in players] 
Two_point_A=[float(x[14]) for x in players] 
Two_point_perc=[x[15] for x in players]
eFG_perc=[x[16] for x in players]
FT=[float(x[17]) for x in players]
FTA=[float(x[18]) for x in players]
FT_perc=[x[19] for x in players]
ORB=[float(x[20]) for x in players]
DRB=[float(x[21]) for x in players]
TRB=[float(x[22]) for x in players] 
AST=[float(x[23]) for x in players] 
STL=[float(x[24]) for x in players]
BLK=[float(x[25]) for x in players]
TOV=[float(x[26]) for x in players]
PF=[float(x[27]) for x in players]
PTS=[float(x[28]) for x in players]

player_dict={"Player":Player,
            "Pos":Pos,
            "Age":Age,
            "Tm":Tm,
            "G":G,
            "MP":MP,
            "FG":FG,
            "FGA":FGA,
            "FG%":FG_perc,
            "3P":Three_point,
            "3PA":Three_point_A,
            "3P%":Three_point_perc,
            "2P":Two_point,
            "2PA":Two_point_A,
            "2P%":Two_point_perc,
            "eFG%":eFG_perc,
            "FT":FT,
            "FTA":FTA,
            "FT%":FT_perc,
            "ORB":ORB,
            "DRB":DRB,
            "TRB":TRB,
            "AST":AST,
            "STL":STL,
            "BLK":BLK,
            "TOV":TOV,
            "PF":PF,
            "PTS":PTS}

"""Converting dictionary to dataframe and displaying it"""
"""Turn perc fields into floats??"""
df=pd.DataFrame(player_dict).set_index("Player")

"""Selecting columns with shooting percentages,
and converting them to float numbers, removing the "." at the beginning """
x=df.select(lambda col: "%" in col, axis=1).columns

for item in x:
    df[item]= pd.to_numeric(df[item].str.split(".", n = 1, expand = True)[1])/10


""" PLOT FT% by pos, highligthing older vs younger players

A veteran player is defined as a player whose age is higher than the average age + 1 positive standard deviation of the age feature
"""
df["Veteran"]=df["Age"]>=df["Age"].mean()+df["Age"].std()
sns.catplot(x="Pos", y="FT%",hue="Veteran",data=df[df["FT%"]>50])

"""testing for difference in the means among FT% proportion between Veteran and non-Veteran players"""
x1=int(df[df["Veteran"]==True]["FTA"].sum())
p1=df[df["Veteran"]==True]["FT"].sum()/x1

n1=len(df[df["Veteran"]==True])

x2=int(df[df["Veteran"]==False]["FTA"].sum())
p2=df[df["Veteran"]==False]["FT"].sum()/x2

n2=len(df[df["Veteran"]==False])

p=(df[df["Veteran"]==True]["FT"].sum()+df[df["Veteran"]==False]["FT"].sum())/(x1+x2)

Z=(p1-p2)/(p*(1-p)*((1/n1)+(1/n2)))**0.5



result=st.norm.cdf(Z)>st.norm.cdf(1.96)

print(result)


