#%%
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.datasets import make_regression
import pandas as pd
import numpy as np
#%%

def find_batter(player_name,date,database_path,days=3):
    '''
    타자는 특정 날짜로 부터 존재 유무과 관계없이 데이터 days만큼.
    '''    

    year = date.split('-')[0]

    raw_batter = pd.read_excel(database_path + player_name,sheet_name=year, \
                                index_col=0, engine='openpyxl')
    
    date_list = list(map(lambda x:x.strftime('%m-%d'), pd.date_range(date, periods=days)   ))
    
    batter_info = [raw_batter[raw_batter.index == date_list[i]] for i in range(days) ]

    return batter_info


def find_pitcher(player_name,date,database_path,days=3):
    '''
    투수는 특정 날짜로 부터 존재하는 경기 데이터 days만큼.
    '''

    year = date.split('-')[0]
    raw_pitcher = pd.read_excel(database_path + player_name,sheet_name=year, \
                                index_col=0, engine='openpyxl')

    date = date.split('-')[1] + '-' +date.split('-')[2]
    date_index = int(np.where((raw_pitcher.index == date)==True)[0])
    date_list = [raw_pitcher.index[date_index-i] for i in range(days)]

    pichter_info = [raw_pitcher[raw_pitcher.index == play_day] for play_day in date_list]

    return pichter_info
#%%
# 타자 데이터

test_game = '/home/swha/ToTo/ToTo/Data/raw/2016-07-26_라이온즈파크_05_04.xlsx'
database_path = '/home/swha/ToTo/ToTo/Data/raw/batter/'
date = '2016-07-26'

away_batting_order = pd.read_excel(test_game,sheet_name='AwayBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[:-1]

away_batting_info = []
home_batting_info = []

for name,birth in away_batting_order:
    player_info = f'{name}_{birth}.xlsx'
    away_batting_info.append(find_batter(player_info,date,database_path))


home_batting_order = pd.read_excel(test_game,sheet_name='HomeBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[:-1]

for name,birth in home_batting_order:
    player_info = f'{name}_{birth}.xlsx'
    home_batting_info.append(find_batter(player_info,date,database_path))


#%%
# 투수 데이터
database_path = '/home/swha/ToTo/ToTo/Data/raw/pitcher/'

away_pitcher = pd.read_excel(test_game,sheet_name='AwayBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[-1]

player_name = f'{away_pitcher[0]}_{away_pitcher[1]}.xlsx'
away_picther = find_pitcher(player_name,date,database_path)




home_pitcher = pd.read_excel(test_game,sheet_name='AwayBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[-1]

player_name = f'{home_pitcher[0]}_{home_pitcher[1]}.xlsx'
home_picther = find_pitcher(player_name,date,database_path)




# %%

# %%
