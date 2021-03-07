#%%
import os
import pandas as pd
import get_data_from_html

soup_data = os.listdir('./soup_data')
# %%
# 팀에 속해있는 선수 이름 데이터 구성해야됨.

team_names = ['두산','한화','키움','KIA','삼성','롯데','LG','KT','NC']
yrs_list = ['2016','2017', '2018', '2019','2020']

for team_name in team_names:
    for yrs in yrs_list:

        team_soup = open(os.getcwd() + '/soup_data/' + f'{team_name}_{yrs}')
        tmp = get_data_from_html.GetPlayerList(team_soup)

        print(tmp)
        break
    break