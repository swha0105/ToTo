#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys

#%%


## 타자 
def batter_get_from_soup(soup):

    featureName = ['날짜','상대','결과','타순','P','선발','타수','득점','안타','이타','삼타','홈런','루타','타점'\
        ,'도루','도실','볼넷','사구','고4','삼진','병살','희타','희비','타율','출루','장타','OPS'\
            ,'투구','avLI','RE24','WPA']
    feature = []

    batter_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div > div:nth-child(3) > div > div > table')
    batterInfo = pd.DataFrame()
    for table in batter_table.find_all('tr'):
        
        if table.find_all('span')[-1].get_text() == 'P':
            continue
        else:
            tmp = []
            for rows in table.find_all('span'):
                tmp.append(rows.get_text())
            batterInfo = batterInfo.append([tmp])
    batterInfo.columns = featureName
    return batterInfo




data_path = '/home/swha/ToTo/ToTo/Data/soup/batter_soup_data/'
save_path = '/home/swha/ToTo/ToTo/Data/raw/batter/'
years = ['2016','2017','2018','2019','2020']

playerList = os.listdir(data_path)
NameBirth = list(map(lambda x:(x.split('_')[0],  x.split('_')[1] ),playerList ))


for name,birth in NameBirth:

    Info = pd.DataFrame()

    flag = 0    
    for year in years:
        print(name,year)
        fileName = f'{name}_{birth}_{year}'
        try:
            soup = BeautifulSoup(open(data_path + fileName),"html.parser")
            Info = (batter_get_from_soup(soup))
        except FileNotFoundError:
            continue

        if len(Info) == 0:
            continue   
        else:
            if flag == 0:
                with pd.ExcelWriter(f'{save_path}{name}_{birth}.xlsx', engine='openpyxl') as tmp:
                    Info.to_excel(tmp,sheet_name=year,index=False)
                    flag = 1 
            else:
                with pd.ExcelWriter(f'{save_path}{name}_{birth}.xlsx',mode='a', engine='openpyxl') as tmp:
                    Info.to_excel(tmp,sheet_name=year,index=False)


#%%

## 투수 

def pitcher_get_from_soup(soup):

    featureName = ['날짜','상대','결과','선발','이닝','실점','자책','타자','타수','안타'\
        ,'이타','삼타','홈런','볼넷','고4','사구','삼진','투구','WHIP','타율','출루율'\
        ,'OPS','ERA','avLI','RE24','WPA','GSC','DEC','간격']
    feature = []

    pitcher_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div > div:nth-child(3) > div > div > table')
    pitcherInfo = pd.DataFrame()


    for table in pitcher_table.find_all('tr'):
        
        if table.find_all('span')[-1].get_text() == '간격':
            continue
            
        else:
            tmp = []
            
            for rows in table.find_all('span'):
                tmp.append(rows.get_text())
            pitcherInfo = pitcherInfo.append([tmp])
    pitcherInfo.columns = featureName

    return pitcherInfo    



data_path = '/home/swha/ToTo/ToTo/Data/soup/picther_soup_data/'
save_path = '/home/swha/ToTo/ToTo/Data/raw/pitcher/'
years = ['2016','2017','2018','2019','2020']

playerList = os.listdir(data_path)
NameBirth = list(map(lambda x:(x.split('_')[0],  x.split('_')[1] ),playerList ))


for name,birth in NameBirth:

    Info = pd.DataFrame()

    flag = 0    
    for year in years:
        print(name,year)
        fileName = f'{name}_{birth}_{year}'
        try:
            soup = BeautifulSoup(open(data_path + fileName),"html.parser")
            Info = (pitcher_get_from_soup(soup))
        except FileNotFoundError:
            continue

        if len(Info) == 0:
            continue   
        else:
            if flag == 0:
                with pd.ExcelWriter(f'{save_path}{name}_{birth}.xlsx', engine='openpyxl') as tmp:
                    Info.to_excel(tmp,sheet_name=year,index=False)
                    flag = 1 
            else:
                with pd.ExcelWriter(f'{save_path}{name}_{birth}.xlsx',mode='a', engine='openpyxl') as tmp:
                    Info.to_excel(tmp,sheet_name=year,index=False)


    

# %%
