#%%

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 
import get_data_from_html

yrs_list = ['2016','2017', '2018', '2019','2020']
date_list = []

path = '/home/swha/ToTo/ToTo/Data/team_info/'

for year in yrs_list:
    year_2017 = pd.date_range(year + '-04-01', periods = 180, freq = '1d')
    date_list.append(list(map(lambda x:str(x)[:10],year_2017.to_list())))

date_list = sum(date_list,[])
stadiums = ['라이온즈파크','고척돔','잠실','마산','인천문학','대전한밭','챔피언스필드','케이티위즈파크','부산사직']


#%%

# 경기 정보, 최근 팀정보, 선발수투 정보.

for date in date_list:
    for stadium in stadiums:
        url = 'http://www.statiz.co.kr/boxscore.php?opt=5&date=' + date + '&stadium=' + stadium 
        response = requests.get(url)
        html = response.text
        log_soup = BeautifulSoup(html, 'html.parser')
        
        url = 'http://www.statiz.co.kr/boxscore.php?opt=2&date=' + date + '&stadium=' + stadium 
        response = requests.get(url)
        html = response.text
        preview_soup = BeautifulSoup(html, 'html.parser')


        with open(os.getcwd() + '/soup_data/' + f'{date}_{stadium}_log', "w", encoding='utf-8') as file:
            file.write(str(log_soup))

        with open(os.getcwd() + '/soup_data/' + f'{date}_{stadium}_preview', "w", encoding='utf-8') as file:
            file.write(str(preview_soup))


        print(date, stadium)

#%%     
# players soup data

# all players name include same name
team_names = ['두산','한화','키움','KIA','삼성','롯데','LG','KT','NC']
yrs_list = ['2016','2017', '2018', '2019','2020']
player_list = []
for team in team_names:
    for year in yrs_list:
        print(team,year)
        url = 'http://www.statiz.co.kr/team.php?opt=0&sopt=8&year=' +year+ '&team=' + team

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        player_list.extend(get_data_from_html.GetPlayerList_wo_birth(soup))


#%%
# player soup 


for player in player_list:
    for year in yrs_list:
        
        url = 'http://www.statiz.co.kr/player.php?name=' + player
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        birth = get_data_from_html.GetPlayerBirth(soup)

        if birth == False:
            continue
        else:

            # url = 'http://www.statiz.co.kr/player.php?opt=1&name=' + player + '&birth=' + birth
            # response = requests.get(url)
            # html = response.text
            # year_soup = BeautifulSoup(html, 'html.parser')

            # with open(os.getcwd() + '/player_soup_data/' + f'{player}_{birth}_{year}_year', "w", encoding='utf-8') as file:
            #     file.write(str(year_soup))

            url = 'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name=' + player + '&birth=' + birth +'&re=0&se=&da=&year=' + year + '&cv='
            
            response = requests.get(url)
            html = response.text
            day_soup = BeautifulSoup(html, 'html.parser')
            
            if (day_soup.find_all('tr')[-1].getText()).startswith('데이터'):
                continue
            else:
                with open(os.getcwd() + '/player_soup_data/' + f'{player}_{birth}_{year}', "w", encoding='utf-8') as file:
                    file.write(str(day_soup))

        print(year,player)
    

