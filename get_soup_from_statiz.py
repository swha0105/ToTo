#%%

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 

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

# players 이름 정보

team_names = ['두산','한화','키움','KIA','삼성','롯데','LG','KT','NC']
yrs_list = ['2016','2017', '2018', '2019','2020']

for team in team_names:
    for year in yrs_list:
        print(team,year)
        url = 'http://www.statiz.co.kr/team.php?opt=0&sopt=8&year=' +year+ '&team=' + team

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        with open(os.getcwd() + '/soup_data/' + f'{team}_{year}_players', "w", encoding='utf-8') as file:
            file.write(str(soup))
#%%

# 테스트. 

a = soup.find('div', {'class':'wrapper'})
b = a.find('div', {'class':'content-wrapper'})
c = b.find('div', {'class':'container'})
d = c.find('section', {'class':'content'})
e = d.find('div', {'class':'row'})
f = e.find_all('div', {'class':'col-md-12 col-xs-12 col-sm-12 col-lg-12'})[-1]
g = f.find('div', {'class':'row'})
h = g.find('div', {'class':'col-xs-12 col-sm-6'})
i = h.find('div', {'class':'box'})    
j = i.find('div', {'class':'box-body no-padding'})
# k = j.find('div', {'class':'table table-striped'})

player_list = re.compile('[가-힣]+').findall(j.getText())[2:]

for player in player_list:
    player_url = 'http://www.statiz.co.kr/player.php?name=' + player 

#%%

print()
# %%
