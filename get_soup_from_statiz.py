#%%

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 
import re
import get_data_from_html

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



#------

#%%     
# 각 팀의 선수들의 이름을 긁어옴
# 팀 정보 -> 연봉정보에 모든 선수이름이 적혀있음
# 특정연도는 누락된 선수이름이 있어 5년간 선수 이름 데이터를 모아 합침.

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
# 긁어온 html 데이터에서 이름만 추출

existPlayerList = os.listdir(os.getcwd()+'/player_soup_data/')
existPlayerList = list(map(lambda x:re.compile('[가-힣]+').findall(x)[0],existPlayerList))

#%%

# 선수의 이름과 그에 해당되는 생년월일을 긁어와 최근 N경기 데이터가 담긴 html 크롤링. (투수, 타자 상관없음)

for player in player_list:
    if player in existPlayerList:
        continue
    else:
        url = 'http://www.statiz.co.kr/player.php?name=' + player
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        birth = get_data_from_html.GetPlayerBirth(soup)

        print(player,birth)

        if birth == False:
            continue

        for year in yrs_list:

            url = 'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name=' + player + '&birth=' + birth +'&re=0&se=&da=&year=' + year + '&cv='
            
            response = requests.get(url)
            html = response.text
            day_soup = BeautifulSoup(html, 'html.parser')
            
            # if (day_soup.find_all('tr')[-1].getText()).startswith('데이터'):
            #     continue
            # else:
            with open(os.getcwd() + '/player_soup_data/' + f'{player}_{birth}_{year}', "w", encoding='utf-8') as file:
                file.write(str(day_soup))
                print(player,year)

        
    

