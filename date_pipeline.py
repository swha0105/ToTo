#%%
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.datasets import make_regression
import pandas as pd
import numpy as np

def find_batter(player_name,date,database_path,days=3):
    '''
    타자는 특정 날짜로 부터 존재 유무과 관계없이 데이터 days만큼.
    '''    

    year = date.split('-')[0]

    raw_batter = pd.read_excel(database_path + player_name,sheet_name=str(year), \
                                index_col=0, engine='openpyxl')
    
    date_list = list(map(lambda x:x.strftime('%m-%d'), pd.date_range(end=date, periods=days+1)   ))[:-1]
    
    batter_info = [raw_batter[raw_batter.index == date_list[i]] for i in range(days) ]

    return batter_info


def find_pitcher(player_name,date,database_path,days=3):
    '''
    투수는 특정 날짜로 부터 존재하는 경기 데이터 days만큼.
    '''

    year = date.split('-')[0]
    raw_pitcher = pd.read_excel(database_path + player_name,sheet_name=str(year), \
                                index_col=0, engine='openpyxl')

    date = date.split('-')[1] + '-' +date.split('-')[2]
    date_index = int(np.where((raw_pitcher.index == date)==True)[0])
    date_list = [raw_pitcher.index[date_index-i] for i in range(days)]

    pichter_info = [raw_pitcher[raw_pitcher.index == play_day] for play_day in date_list]

    return pichter_info



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
        bat_orders = []    
        at_bat = 0; run_scored = 0; single_hits = 0; multi_hits = 0; home_run = 0; run_bat = 0
        stolen_base = 0; base_onballs = 0; sacrifice = 0; strike_out = 0; double_play = 0
        for i,day in enumerate(date_list):
            
            try:
                date = batting_info[j][i].index[0]
            except IndexError:
                break
            if date != day:
                # save_format.append([0 for _ in range(10)],ignore_index=True)
                info_list.append( [0 for _ in range(10) ])
            
            # bat_orders.append(home_batting_info[j][i].타순[0])
            at_bat += batting_info[j][i].타수[0]
            run_scored += batting_info[j][i].득점[0]
            single_hits += batting_info[j][i].안타[0]
            multi_hits += batting_info[j][i].이타[0] + batting_info[0][i].삼타[0]
            home_run += batting_info[j][i].홈런[0]
            run_bat += batting_info[j][i].타점[0]
            stolen_base += batting_info[j][i].도루[0]
            base_onballs += batting_info[j][i].볼넷[0] + batting_info[0][i].사구[0] + batting_info[0][i].고4[0]
            sacrifice += batting_info[j][i].희타[0] + batting_info[0][i].희비[0]
            strike_out += batting_info[j][i].삼진[0]
            double_play += batting_info[j][i].병살[0]

        # bat_order = collections.Counter(bat_orders).most_common()[0][0]

        info_lists.append([at_bat,run_scored,single_hits,multi_hits,home_run,\
                        stolen_base,base_onballs,sacrifice,strike_out,double_play])
        
        
    save_format = pd.DataFrame(info_lists,columns=['타수','득점','안타','장타', '홈런', '도루', '볼넷',\
                '희생', '삼진', '병살'],index=list(range(1,10)))

    return save_format


def get_pitcher_info(picther_info,ref_date,days=3):

    '''
    선발투수 최근 3경기 데이터 가져오기
    '''

    info_lists  = []

    for j in range(len(away_picther)):
        
        inning = 0; loss_scored = 0; num_batter = 0; single_hitted = 0; multi_hitted = 0; home_runed = 0; 
        base_onballs = 0; strike_out = 0; total_balls = 0; interval = 0

        inning = away_picther[j].이닝[0]
        loss_scored = away_picther[j].자책[0]
        num_batter = away_picther[j].타자[0]
        single_hitted = away_picther[j].안타[0]
        multi_hitted = away_picther[j].이타[0] + away_picther[j].삼타[0]
        home_runed = away_picther[j].홈런[0]
        base_onballs = away_picther[j].볼넷[0] + away_picther[j].고4[0] + away_picther[j].사구[0]
        strike_out = away_picther[j].삼진[0]
        total_balls = away_picther[j].투구[0]
        interval = away_picther[j].간격[0]

        info_lists.append([inning,loss_scored,num_batter,single_hitted,multi_hitted,\
                        home_runed,base_onballs,strike_out,total_balls,interval])
        
            
    save_format = pd.DataFrame(info_lists,columns=['이닝','자책','타자','안타', '장타', '홈런', '볼넷',\
                '삼진', '투구', '간격'])
        
    return save_format


#%%

game_name = '2016-07-26_라이온즈파크_05_04.xlsx'
test_game = '/home/swha/ToTo/ToTo/Data/raw/' + game_name
database_path = '/home/swha/ToTo/ToTo/Data/raw/batter/'
ref_date = '2016-07-26'
days = 3

#%%
# 타자 데이터
away_batting_order = pd.read_excel(test_game,sheet_name='AwayBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[:-1]

away_batting_info = []
home_batting_info = []

for name,birth in away_batting_order:
    player_info = f'{name}_{birth}.xlsx'
    away_batting_info.append(find_batter(player_info,ref_date,database_path))


home_batting_order = pd.read_excel(test_game,sheet_name='HomeBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[:-1]

for name,birth in home_batting_order:
    player_info = f'{name}_{birth}.xlsx'
    home_batting_info.append(find_batter(player_info,ref_date,database_path))


away_batter_info = get_batter_info(away_batting_info,ref_date)
home_batter_info = get_batter_info(home_batting_info,ref_date)



#%%

# 투수 데이터

database_path = '/home/swha/ToTo/ToTo/Data/raw/pitcher/'

away_pitcher = pd.read_excel(test_game,sheet_name='AwayBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[-1]

player_name = f'{away_pitcher[0]}_{away_pitcher[1]}.xlsx'
away_picther = find_pitcher(player_name,ref_date,database_path)



home_pitcher = pd.read_excel(test_game,sheet_name='AwayBattingOrder',\
    index_col=0, engine='openpyxl').to_numpy()[-1]

player_name = f'{home_pitcher[0]}_{home_pitcher[1]}.xlsx'
home_picther = find_pitcher(player_name,ref_date,database_path)

away_pitcher_info = get_pitcher_info(away_picther,ref_date)
home_pitcher_info = get_pitcher_info(home_picther,ref_date)

#%%
