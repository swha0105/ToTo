#%%

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 
import re


# 2016 ~ 2020년까지 4월 1일부터 180일 동안 날짜 데이터 생성

yrs_list = ['2016','2017', '2018', '2019','2020']
date_list = []

path = '/home/swha/ToTo/ToTo/Data/team_info/'

for year in yrs_list:
    year_2017 = pd.date_range(year + '-04-01', periods = 180, freq = '1d')
    date_list.append(list(map(lambda x:str(x)[:10],year_2017.to_list())))

date_list = sum(date_list,[])
stadiums = ['라이온즈파크','고척돔','잠실','마산','인천문학','대전한밭','챔피언스필드','케이티위즈파크','부산사직']


#%%
# 팀정보 크롤링
# 경기 정보, 최근 팀정보, 선발투수 정보를 크롤링으로 긁어와 html 원본 저장

# log: 각 팀의 배팅오더
# preview: 각 팀의 선발투수 정보, 최근 10경기, 상대전적

for date in date_list:
    for stadium in stadiums:
        log_url = 'http://www.statiz.co.kr/boxscore.php?opt=5&date=' + date + '&stadium=' + stadium 
        response = requests.get(log_url)
        html = response.text
        log_soup = BeautifulSoup(html, 'html.parser')
        
        preview_url = 'http://www.statiz.co.kr/boxscore.php?opt=2&date=' + date + '&stadium=' + stadium 
        response = requests.get(preview_url)
        html = response.text
        preview_soup = BeautifulSoup(html, 'html.parser')


        with open(os.getcwd() + '/soup_data/' + f'{date}_{stadium}_log', "w", encoding='utf-8') as file:
            file.write(str(log_soup))

        with open(os.getcwd() + '/soup_data/' + f'{date}_{stadium}_preview', "w", encoding='utf-8') as file:
            file.write(str(preview_soup))


        print(date, stadium)


#%%
# 데이터 없는 soup 삭제
from get_teamdata_from_html  import away_batting_order
from bs4 import BeautifulSoup
import os 
data_path = '/home/swha/ToTo/ToTo/Data/soup/soup_data/'

# deleteCandidate = []

for dataName in sorted(os.listdir(data_path)):
    if dataName.endswith('log'):
        soup = BeautifulSoup(open(data_path + dataName),"html.parser")
        try:
            away_batting_order(soup)
        except AttributeError:
            os.remove(f'{data_path}{dataName}')
            os.remove(f'{data_path}{dataName[:-4]}_preview')
            # deleteCandidate.append(dataName)
            # deleteCandidate.append(f'{dataName[:-4]}_preview')
            print(f'{data_path}{dataName}')
        
            


#------------------------------------------------
#%%
# 선수 정보 크롤링!! 
# all_players 엑셀 sheet에 담겨있는 선수 정보를 이용하여 크롤링


batters = pd.read_excel('/home/swha/ToTo/ToTo/Data/raw/all_players.xlsx',sheet_name='Batters',engine = 'openpyxl',index_col=0)


#%%

# 타자 데이터
existPlayerList = os.listdir('/home/swha/ToTo/ToTo/Data/soup/batter_soup_data/')
existPlayer = list(map(lambda x:(x.split('_')[0],x.split('_')[1] ),existPlayerList))


for player,birth in batters.to_numpy():
    if (player,birth) in existPlayer:
        print(f'{player} passed')
        continue

    for year in yrs_list:

        url = 'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name=' + player + '&birth=' + birth +'&re=0&se=&da=&year=' + year + '&cv='
        
        response = requests.get(url)
        html = response.text
        day_soup = BeautifulSoup(html, 'html.parser')
        
        if not day_soup.find_all('tr') or (day_soup.find_all('tr')[-1].getText()).startswith('데이터'):
            continue
        else:
            
            with open(f'/home/swha/ToTo/ToTo/Data/soup/batter_soup_data/{player}_{birth}_{year}', "w", encoding='utf-8') as file:
                file.write(str(day_soup))
                print(player,year)
        

#%%
picthers = pd.read_excel('/home/swha/ToTo/ToTo/Data/raw/all_players.xlsx',sheet_name='Pitchers',engine = 'openpyxl',index_col=0)

existPlayerList = os.listdir('/home/swha/ToTo/ToTo/Data/soup/picther_soup_data/')
existPlayer = list(map(lambda x:(x.split('_')[0],x.split('_')[1] ),existPlayerList))


for player,birth in picthers.to_numpy():
    if (player,birth) in existPlayer:
        print(f'{player} passed')
        continue
    
    for year in yrs_list:

        url = 'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name=' + player + '&birth=' + birth +'&re=1&se=&da=&year=' + year + '&cv='
        
        response = requests.get(url)
        html = response.text
        day_soup = BeautifulSoup(html, 'html.parser')
        
        if not day_soup.find_all('tr') or (day_soup.find_all('tr')[-1].getText()).startswith('데이터'):
            continue
        else:
            
            with open(f'/home/swha/ToTo/ToTo/Data/soup/picther_soup_data/{player}_{birth}_{year}', "w", encoding='utf-8') as file:
                file.write(str(day_soup))
                print(player,year)
            

    




#---
#%%

