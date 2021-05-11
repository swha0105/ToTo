#%%
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.datasets import make_regression
import pandas as pd
import numpy as np
import os
from csv import writer

def find_batter(player_name,date,database_path,days=3):
    '''
    타자는 특정 날짜로 부터 존재 유무과 관계없이 데이터 days만큼.
    '''    

    year = date.split('-')[0]
    date_list = list(map(lambda x:x.strftime('%m-%d'), pd.date_range(end=date, periods=days+1)   ))[:-1]

    try:
        raw_batter = pd.read_excel(database_path + player_name,sheet_name=str(year), \
                                    index_col=0, engine='openpyxl')
        batter_info = [raw_batter[raw_batter.index == date_list[i]] for i in range(days) ]

        return batter_info

    except:
        raw_batter = pd.read_excel(database_path + '김상수_1990-03-23.xlsx',sheet_name=str(year), \
                                    index_col=0, engine='openpyxl')
        batter_info = pd.DataFrame(index = date_list, columns=raw_batter.columns)
        batter_info.fillna(0)

        return batter_info
    

def find_pitcher(player_name,date,database_path,days=3):
    '''
    투수는 특정 날짜로 부터 존재하는 경기 데이터 days만큼.
    '''

    year = date.split('-')[0]
    try:
        raw_pitcher = pd.read_excel(database_path + player_name,sheet_name=str(year), \
                                    index_col=0, engine='openpyxl')

        date = date.split('-')[1] + '-' +date.split('-')[2]
        date_index = int(np.where((raw_pitcher.index == date)==True)[0])
        date_list = [raw_pitcher.index[date_index-i] for i in range(days)]

        pichter_info = [raw_pitcher[raw_pitcher.index == play_day] for play_day in date_list]

        return pichter_info
    
    except:
        return None


def get_batter_info(batting_info,ref_date,days=3):

    '''
    경기에 해당되는 타자들 데이터 가져오기
    타자는 경기 유무와 관계 없이 최근 n(3)일만 보기
    타순은 제외.
    선발,포지션 제외.
    2루타 3루타는 장타로 합침
    희생번트, 희생플라이 합침.
    '''

    date_list = list(map(lambda x:x.strftime('%m-%d'), pd.date_range(end=ref_date, periods=days+1)))[:-1]

    info_lists  = []

    for j in range(len(batting_info)):
        
        at_bat = 0; run_scored = 0; single_hits = 0; multi_hits = 0; home_run = 0; run_bat = 0
        stolen_base = 0; base_onballs = 0; sacrifice = 0; strike_out = 0; double_play = 0
        for i,day in enumerate(date_list):
            
            try:
                date = batting_info[j][i].index[0]
                at_bat += batting_info[j][i].타수[0]
                run_scored += batting_info[j][i].득점[0]
                single_hits += batting_info[j][i].안타[0]
                multi_hits += batting_info[j][i].이타[0] + batting_info[j][i].삼타[0]
                home_run += batting_info[j][i].홈런[0]
                run_bat += batting_info[j][i].타점[0]
                stolen_base += batting_info[j][i].도루[0]
                base_onballs += batting_info[j][i].볼넷[0] + batting_info[j][i].사구[0] + batting_info[j][i].고4[0]
                sacrifice += batting_info[j][i].희타[0] + batting_info[j][i].희비[0]
                strike_out += batting_info[j][i].삼진[0]
                double_play += batting_info[j][i].병살[0]

            except:
                continue
                
        info_lists.append([at_bat,run_scored,single_hits,multi_hits,home_run,\
                stolen_base,base_onballs,sacrifice,strike_out,double_play])


        # bat_order = collections.Counter(bat_orders).most_common()[0][0]

        
        
    save_format = pd.DataFrame(info_lists,columns=['타수','득점','안타','장타', '홈런', '도루', '볼넷',\
                '희생', '삼진', '병살'],index=list(range(1,10)))

    return save_format


def get_pitcher_info(picther_info,ref_date,days=3):

    '''
    선발투수 최근 3경기 데이터 가져오기
    '''

    info_lists  = []

    for j in range(len(picther_info)):
        
        inning = 0; loss_scored = 0; num_batter = 0; single_hitted = 0; multi_hitted = 0; home_runed = 0; 
        base_onballs = 0; strike_out = 0; total_balls = 0; interval = 0

        inning = picther_info[j].이닝[0]
        loss_scored = picther_info[j].자책[0]
        num_batter = picther_info[j].타자[0]
        single_hitted = picther_info[j].안타[0]
        multi_hitted = picther_info[j].이타[0] + picther_info[j].삼타[0]
        home_runed = picther_info[j].홈런[0]
        base_onballs = picther_info[j].볼넷[0] + picther_info[j].고4[0] + picther_info[j].사구[0]
        strike_out = picther_info[j].삼진[0]
        total_balls = picther_info[j].투구[0]
        interval = picther_info[j].간격[0][0]

        info_lists.append([inning,loss_scored,num_batter,single_hitted,multi_hitted,\
                        home_runed,base_onballs,strike_out,total_balls,interval])
        
            
    save_format = pd.DataFrame(info_lists,columns=['이닝','자책','타자','안타', '장타', '홈런', '볼넷',\
                '삼진', '투구', '간격'])
        
    return save_format




batter_database_path = os.getcwd() + '/Data/raw/batter/'
pitcher_database_path = os.getcwd() + '/Data/raw/pitcher/'
game_database_path = os.getcwd() + '/Data/raw/game/'
days = 3
whole_data = []

for game_name in sorted(os.listdir(game_database_path)):
    
    
    print(game_name)
    

    game_path = game_database_path + game_name
    ref_date = game_name.split('_')[0]
    away_get_score = int(game_name.split('_')[2])
    home_get_score = int(game_name.split('_')[3].split('.')[0])


    ### 팀 데이터 추출

    away_team_data = []

    away_team_versus = pd.read_excel(game_path,sheet_name='AwayVersus',\
        index_col=0, engine='openpyxl')

    away_team_versus = away_team_versus.fillna(0).to_numpy()
    away_team_versus = sum(list(map(list,away_team_versus)),[])
    away_team_data = []

    for away_team_versus_data in away_team_versus[:-1]:
        
        away_team_data.append(away_team_versus_data)
        
    away_team_data.append(int(away_team_versus[-1][:-1]))


    away_team_recent = pd.read_excel(game_path,sheet_name='AwayRecent',\
        index_col=0, engine='openpyxl').to_numpy()

    for away_team_recent_data_bulk in away_team_recent:
        for away_team_recent_data in away_team_recent_data_bulk:
            away_team_data.append(away_team_recent_data)


    home_team_data = []

    home_team_versus = pd.read_excel(game_path,sheet_name='HomeVersus',\
        index_col=0, engine='openpyxl')

    home_team_versus = home_team_versus.fillna(0).to_numpy()
    home_team_versus = sum(list(map(list,home_team_versus)),[])
    home_team_data = []

    for home_team_versus_data in home_team_versus[:-1]:
        
        home_team_data.append(home_team_versus_data)
        
    home_team_data.append(int(home_team_versus[-1][:-1]))


    home_team_recent = pd.read_excel(game_path,sheet_name='HomeRecent',\
        index_col=0, engine='openpyxl').to_numpy()

    for home_team_recent_data_bulk in home_team_recent:
        for home_team_recent_data in home_team_recent_data_bulk:
            home_team_data.append(home_team_recent_data)

    # 팀 최근경기 10경기에 대해 데이터가 없으면 패스
    if len(home_team_data) != 37 or  len(away_team_data) != 37:
        continue



    ### 각 팀 타순 데이터 추출

    away_batting_info = []
    home_batting_info = []

    away_batting_order = pd.read_excel(game_path,sheet_name='AwayBattingOrder',\
        index_col=0, engine='openpyxl').to_numpy()[:-1]

    for name,birth in away_batting_order:
        player_info = f'{name}_{birth}.xlsx'
        away_batting_info.append(find_batter(player_info,ref_date,batter_database_path))

    home_batting_order = pd.read_excel(game_path,sheet_name='HomeBattingOrder',\
        index_col=0, engine='openpyxl').to_numpy()[:-1]

    for name,birth in home_batting_order:
        player_info = f'{name}_{birth}.xlsx'
        home_batting_info.append(find_batter(player_info,ref_date,batter_database_path))


    ### 타순 데이터를 기반으로 타자들의 정보 추출

    away_batter_info = get_batter_info(away_batting_info,ref_date)
    home_batter_info = get_batter_info(home_batting_info,ref_date)

    away_batter_data = []
    home_batter_data = []

    for away_bat_order,home_bat_order in zip(away_batter_info.to_numpy(),home_batter_info.to_numpy()):
        for away_data,home_data in zip(away_bat_order,home_bat_order):
            away_batter_data.append(away_data)
            home_batter_data.append(home_data)    
    

    ### 투수 데이터 추출

    away_pitcher = pd.read_excel(game_path,sheet_name='AwayBattingOrder',\
        index_col=0, engine='openpyxl').to_numpy()[-1]

    player_name = f'{away_pitcher[0]}_{away_pitcher[1]}.xlsx'
    away_picther = find_pitcher(player_name,ref_date,pitcher_database_path)
    

    home_pitcher = pd.read_excel(game_path,sheet_name='HomeBattingOrder',\
        index_col=0, engine='openpyxl').to_numpy()[-1]

    player_name = f'{home_pitcher[0]}_{home_pitcher[1]}.xlsx'
    home_picther = find_pitcher(player_name,ref_date,pitcher_database_path)
    
    if away_picther == None or home_picther == None:
        continue        

    away_pitcher_info = get_pitcher_info(away_picther,ref_date)
    home_pitcher_info = get_pitcher_info(home_picther,ref_date)


    # away_batter = list(map(sum ,zip(*away_batter_info.values)))
    # home_batter = list(map(sum ,zip(*home_batter_info.values)))


    away_pitcher_data = []
    home_pitcher_data = []

    for away_pit_order,home_pit_order in zip(away_pitcher_info.to_numpy(),home_pitcher_info.to_numpy()):
        for away_data,home_data in zip(away_pit_order,home_pit_order):
            away_pitcher_data.append(int(away_data))
            home_pitcher_data.append(int(home_data))


    
    data = []
    data = away_batter_data + home_batter_data + away_pitcher_data + home_pitcher_data \
        + away_team_data + home_team_data + [away_get_score] + [home_get_score]
    
    print(f'away_batter_data: {len(away_batter_data)}  home_batter_data: {len(home_batter_data)} \
        away_pitcher_data: {len(away_pitcher_data)} home_pitcher_data: {len(home_pitcher_data)}  \
        away_team_data: {len(away_team_data)} home_team_data: {len(home_team_data)} ' )
    
    
    print(game_name,len(data),'it will saved')
    with open('data_renew.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(data)
        f_object.close()
    

#%%
away_batter_data + home_batter_data + away_pitcher_data + home_pitcher_data \
        + away_team_data + home_team_data + [away_get_score] + [home_get_score]
# %%

away_bat_scheme = ['타수','득점','안타','장타', '홈런', '도루', '볼넷','희생', '삼진', '병살']
home_bat_scheme = ['타수','득점','안타','장타', '홈런', '도루', '볼넷','희생', '삼진', '병살']

away_pit_scheme = ['이닝','자책','타자','안타', '장타', '홈런', '볼넷','삼진', '투구', '간격']
home_pit_scheme = ['이닝','자책','타자','안타', '장타', '홈런', '볼넷','삼진', '투구', '간격']


away_versus = ['시즌 승리','시즌 패배','홈/원정 승리','홈/원정 패배','경기당 득점','경기당 실점','상대전적 승리']
away_recent = ['득점','실점','승패']

home_versus = ['시즌 승리','시즌 패배','홈/원정 승리','홈/원정 패배','경기당 득점','경기당 실점','상대전적 승리']
home_recent = ['득점','실점','승패']

#%%
all_schema = []

for i in range(1,10):
    for scheme in away_bat_scheme:
        all_schema.append(f'away_batter_{i}_{scheme}')

for i in range(1,10):
    for scheme in home_bat_scheme:
        all_schema.append(f'home_batter_{i}_{scheme}')        


for i in range(1,4):
    for scheme in away_pit_scheme:
        all_schema.append(f'away_pitcher_{i}_{scheme}')

for i in range(1,4):
    for scheme in home_pit_scheme:
        all_schema.append(f'home_pitcher_{i}_{scheme}')

for scheme in away_versus:
    all_schema.append(f'away_versus_{scheme}')

for i in range(1,11):
    for scheme in away_recent:
        all_schema.append(f'away_recent_{i}_{scheme}')


for scheme in home_versus:
    all_schema.append(f'home_versus_{scheme}')

for i in range(1,11):
    for scheme in home_recent:
        all_schema.append(f'home_recent_{i}_{scheme}')
all_schema.append('away_get_score')
all_schema.append('home_get_score')


with open("meta_data.txt", "w") as text_file:
    scheme = "\n".join(str(x) for x in all_schema)
    text_file.write(scheme)


