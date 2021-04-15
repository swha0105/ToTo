#%%
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.datasets import make_regression
import pandas as pd
import numpy as np
#%%

def find_batter(player_name,date,database_path,days=3):
    
    year = date.split('-')[0]

    raw_batter = pd.read_excel(database_path + player_name,sheet_name=year, \
                                index_col=0, engine='openpyxl')
    
    date_list = list(map(lambda x:x.strftime('%m-%d'), pd.date_range(date, periods=days)   ))
    
    batter_info = [raw_batter[raw_batter.index == date_list[i]] for i in range(days) ]

    return batter_info
#%%
test_game = '/home/swha/ToTo/ToTo/Data/raw/2016-07-26_라이온즈파크_05_04.xlsx'
database_path = '/home/swha/ToTo/ToTo/Data/raw/batter/'
date = '2016-07-26'



away_batting_order = pd.read_excel(test_game,sheet_name='AwayBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[:-1]

away_batting_info = []
home_batting_info = []

for name,birth in away_batting_order:
    player_info = f'{name}_{birth}'

    player_name = player_info + '.xlsx'
    # year = date.split('-')[0]
    
    away_batting_info.append(find_batter(player_name,date,database_path))


home_batting_order = pd.read_excel(test_game,sheet_name='HomeBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[:-1]

for name,birth in home_batting_order:
    player_info = f'{name}_{birth}'

    player_name = player_info + '.xlsx'
    # year = date.split('-')[0]
    
    home_batting_info.append(find_batter(player_name,date,database_path))


#%%



away_pitcher_order = pd.read_excel(test_game,sheet_name='AwayBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[-1]

database_path = '/home/swha/ToTo/ToTo/Data/raw/pitcher/'



for name,birth in away_batting_order:
    player_info = f'{name}_{birth}'

    player_name = player_info + '.xlsx'
    # year = date.split('-')[0]
    
    away_picther = find_batter(player_name,date,database_path)


home_pitcher_order = pd.read_excel(test_game,sheet_name='HomeBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[:-1]

for name,birth in home_batting_order:
    player_info = f'{name}_{birth}'

    player_name = player_info + '.xlsx'
    # year = date.split('-')[0]
    
    home_picher = find_batter(player_name,date,database_path)





# %%
