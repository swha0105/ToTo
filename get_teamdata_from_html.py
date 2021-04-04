#%%
from bs4 import BeautifulSoup
import pandas as pd

# log_html = '/home/swha/ToTo/ToTo/soup_data/2017-05-14_잠실_log'
# preview_html = '/home/swha/ToTo/ToTo/soup_data/2017-05-14_잠실_preview'

# log_soup = BeautifulSoup(open(log_html),"html.parser")
# preview_soup = BeautifulSoup(open(preview_html),"html.parser")

def game_score(soup):
    '''
    경기 log 데이터를 받아 경기 점수 생성.
    return: Away팀 득점, Home팀 득점
    '''

    away_get,home_get = soup.select_one('body > div > div.content-wrapper > div > section.content > div > div:nth-child(1) > div > div.col-xs-12.col-sm-12.col-md-12.col-lg-4 > div > div:nth-child(2) > span').get_text().split(':')

    return (away_get.strip().zfill(2),home_get.strip().zfill(2))

def home_batting_order(soup):
    ''' 경기 log 데이터를 받아 홈 배팅오더 데이터 생성.
    return: 선수이름, 생년월일

    '''
    Names = []
    Births = []
    raw_table = soup.select_one('body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div.box-body.no-padding.table-responsive > table')


    for raw_data in raw_table.find_all('a'):
        birth_index = str(raw_data).index('birth')
        birth = str(raw_data)[birth_index+6:birth_index+16]
        name = raw_data.get_text()

        Names.append(name)
        Births.append(birth)
    
    orders = [''.join(str(num)) for num in range(1,10)]
    orders += 'P'
    if Names:
        HomeBattingOrder = pd.DataFrame({'선수 이름': Names, '생년월일': Births},orders)
        return HomeBattingOrder
    else:
        return False

def away_batting_order(soup):
    ''' 경기 log 데이터를 받아 어웨이 배팅오더 데이터 생성.
    return: 선수이름, 생년월일

    '''
    Names = []
    Births = []

    raw_table = soup.select_one('body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div.box-body.no-padding.table-responsive > table')

    for raw_data in raw_table.find_all('a'):
        birth_index = str(raw_data).index('birth')
        birth = str(raw_data)[birth_index+6:birth_index+16]
        name = raw_data.get_text()

        Names.append(name)
        Births.append(birth)

    orders = [''.join(str(num)) for num in range(1,10)]
    orders += 'P'
    
    if Names:
        AwayBattingOrder = pd.DataFrame({'선수 이름': Names, '생년월일': Births},orders)
        return AwayBattingOrder
    else:
        return False



def get_versus_data(soup):
    '''
    Input: preview log
    Output: 팀이름, 시즌 승리, 시즌 패배, 홈/원정 승리, 홈/원정 패배, 경기당 득점, 경기당 실점, 상대전적
    '''
    raw_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div.box-body.no-padding > table')
    raw_table_text = [text for text in raw_table.get_text().split('\n') if text != '']

    AwayTeamName = raw_table.find_all('th',limit=3)[1].get_text()
    HomeTeamName = raw_table.find_all('th',limit=3)[2].get_text()
    

    #  raw_table_text[raw_table_text.index('시즌전적')+1]:
    AwaySeason = raw_table_text[raw_table_text.index('시즌전적')+1]
    AwaySeason_Win = AwaySeason.split(',')[0].split('-')[0]
    AwaySeason_Lose = AwaySeason.split(',')[0].split('-')[1]
    AwaySeason_Rank = AwaySeason.split(',')[1]

    HomeSeason = raw_table_text[raw_table_text.index('시즌전적')+2]
    HomeSeason_Win = HomeSeason.split(',')[0].split('-')[0]
    HomeSeason_Lose = HomeSeason.split(',')[0].split('-')[1]
    HomeSeason_Rank = HomeSeason.split(',')[1]

    AwayResultInStadium = raw_table_text[raw_table_text.index('원정 성적')+1]
    AwayResultInStadium_Win = AwayResultInStadium.split('-')[0]
    AwayResultInStadium_Lose = AwayResultInStadium.split('-')[1]

    HomeResultInStadium = raw_table_text[raw_table_text.index('홈 성적')+2]
    HomeResultInStadium_Win = HomeResultInStadium.split('-')[0]
    HomeResultInStadium_Lose = HomeResultInStadium.split('-')[1]

    AwayGetScore =  raw_table_text[raw_table_text.index('경기당 득점')+1]
    AwayLoseScore =  raw_table_text[raw_table_text.index('경기당 실점')+1]

    HomeGetScore =  raw_table_text[raw_table_text.index('경기당 득점')+2]
    HomeLoseScore =  raw_table_text[raw_table_text.index('경기당 실점')+2]

    VersusDataOnlyAwayWin = raw_table_text[raw_table_text.index('상대전적')+1].split(' ')[0]
    VersusDataOnlyHomeWin = raw_table_text[raw_table_text.index('상대전적')+2].split(' ')[0]



    Feature = ['시즌 승리', '시즌 패배', '홈/원정 승리', '홈/원정 패배', '경기당 득점', '경기당 실점', '상대전적 승리']
    AwayInfo = pd.DataFrame({AwayTeamName:[AwaySeason_Win,AwaySeason_Lose,AwayResultInStadium_Win,AwayResultInStadium_Lose,\
            AwayGetScore,AwayLoseScore,VersusDataOnlyAwayWin]},Feature)


    # Feature = ['팀이름', '시즌 승리', '시즌 패배', '홈/원정 승리', '홈/원정 패배', '경기당 득점', '경기당 실점', '상대전적 승리']
    # AwayInfo = pd.DataFrame([AwayTeamName,AwaySeason_Win,AwaySeason_Lose,AwayResultInStadium_Win,AwayResultInStadium_Lose,\
    #         AwayGetScore,AwayLoseScore,VersusDataOnlyAwayWin],Feature,index=False)

    Feature = [ '시즌 승리', '시즌 패배', '홈/원정 승리', '홈/원정 패배', '경기당 득점', '경기당 실점', '상대전적 승리']
    HomeInfo = pd.DataFrame({HomeTeamName:[HomeSeason_Win,HomeSeason_Lose,HomeResultInStadium_Win,HomeResultInStadium_Lose,\
            HomeGetScore,HomeLoseScore,VersusDataOnlyHomeWin]},Feature)

    return AwayInfo, HomeInfo


def start_pitcher(soup):
    '''
    Input: preview log
    Output: (away, home) 선발투수, 시즌 승리, 시즌 패배, 시즌 자책점, 상대 승리, 상대 패배, 상대 자책점, 최근 30일 승리, 최근 30일 패배, 최근 30일 자책점
    '''
    raw_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div.box-body.no-padding')
    try:
        raw_table_text = [text for text in raw_table.get_text().split('\n') if text != '']
    except AttributeError:
        return False,False

    AwayPicther = raw_table_text[raw_table_text.index('선발')+1]
    HomePicther = raw_table_text[raw_table_text.index('선발')+2]
    
    
    AwaySeason = raw_table_text[raw_table_text.index('시즌 성적')+1]
    AwaySeason_Game = AwaySeason.split(',')[0].split(' ')[0]
    AwaySeason_Win = AwaySeason.split(',')[0].split(' ')[1]
    AwaySeason_Lose = AwaySeason.split(',')[0].split(' ')[2]
    AwaySeason_ERA = AwaySeason.split(',')[0].split(' ')[3]

    HomeSeason = raw_table_text[raw_table_text.index('시즌 성적')+2]
    HomeSeason_Game = HomeSeason.split(',')[0].split(' ')[0]
    HomeSeason_Win = HomeSeason.split(',')[0].split(' ')[1]
    HomeSeason_Lose = HomeSeason.split(',')[0].split(' ')[2]
    HomeSeason_ERA = HomeSeason.split(',')[0].split(' ')[3]

    AwayVersus = raw_table_text[raw_table_text.index('상대 전적(14~)')+1]
    AwayVersus_Game = AwayVersus.split(',')[0].split(' ')[0]
    AwayVersus_Win = AwayVersus.split(',')[0].split(' ')[1]
    AwayVersus_Lose = AwayVersus.split(',')[0].split(' ')[2]
    AwayVersus_ERA = AwayVersus.split(',')[0].split(' ')[3]

    HomeVersus = raw_table_text[raw_table_text.index('상대 전적(14~)')+2]
    HomeVersus_Game = HomeVersus.split(',')[0].split(' ')[0]
    HomeVersus_Win = HomeVersus.split(',')[0].split(' ')[1]
    HomeVersus_Lose = HomeVersus.split(',')[0].split(' ')[2]
    HomeVersus_ERA = HomeVersus.split(',')[0].split(' ')[3]

    AwayRecent = raw_table_text[raw_table_text.index('최근 30일')+1]
    AwayRecent_Game = AwayRecent.split(',')[0].split(' ')[0]
    AwayRecent_Win = AwayRecent.split(',')[0].split(' ')[1]
    AwayRecent_Lose = AwayRecent.split(',')[0].split(' ')[2]
    AwayRecent_ERA = AwayRecent.split(',')[0].split(' ')[3]

    HomeRecent = raw_table_text[raw_table_text.index('최근 30일')+2]
    HomeRecent_Game = HomeRecent.split(',')[0].split(' ')[0]
    HomeRecent_Win = HomeRecent.split(',')[0].split(' ')[1]
    HomeRecent_Lose = HomeRecent.split(',')[0].split(' ')[2]
    HomeRecent_ERA = HomeRecent.split(',')[0].split(' ')[3]

    Feature = ['작년 경기', '작년 승리', '작년 패배', '작년 자책점', '상대 경기',\
        '상대 승리', '상대 패배','상대 자책점', '최근(30G) 경기','최근(30G) 승리','최근(30G) 패배','최근(30G) 자책점']
    AwayPitcher = pd.DataFrame({AwayPicther:[AwaySeason_Game,AwaySeason_Win,AwaySeason_Lose,AwaySeason_ERA,\
        AwayVersus_Game,AwayVersus_Win,AwayVersus_Lose,AwayVersus_ERA,\
        AwayRecent_Game,AwayRecent_Win,AwayRecent_Lose,AwayRecent_ERA]},Feature)

    HomePitcher = pd.DataFrame({HomePicther:[HomeSeason_Game,HomeSeason_Win,HomeSeason_Lose,HomeSeason_ERA,\
        HomeVersus_Game,HomeVersus_Win,HomeVersus_Lose,HomeVersus_ERA,\
        HomeRecent_Game,HomeRecent_Win,HomeRecent_Lose,HomeRecent_ERA]},Feature)

    return AwayPitcher, HomePitcher


def team_recent_result(soup):
    '''
    Input: preview log
    Output: (away, home) 득점, 실점, 승패 (승리: 1, 패배: 0 )
    '''

    raw_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div.box-body.no-padding > table')

    GetScores = []
    LoseScores = []
    Result = []
    Dates = []
    for raw in raw_table.find_all('tr')[1:]:

        DateIdx = str(raw.find_all('a')[1]).find('date')
        Date = str(raw.find_all('a')[1])[DateIdx+5:DateIdx+15]

        Dates.append(Date)

        GetScore = raw.find_all('a')[1].get_text().split(':')[0]
        LoseScore = raw.find_all('a')[1].get_text().split(':')[-1]

        GetScores.append(GetScore)
        LoseScores.append(LoseScore)

        
        if int(GetScore) > int(LoseScore):
            Result.append('1')
        else:
            Result.append('0')


    AwayRecentData = pd.DataFrame({'득점': GetScores, '실점': LoseScores, '승패': Result},Dates)


    raw_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div.box-body.no-padding > table')

    GetScores = []
    LoseScores = []
    Result = []
    Dates = []

    for raw in raw_table.find_all('tr')[1:]:

        DateIdx = str(raw.find_all('a')[1]).find('date')
        Date = str(raw.find_all('a')[1])[DateIdx+5:DateIdx+15]

        Dates.append(Date)

        GetScore = raw.find_all('a')[1].get_text().split(':')[0]
        LoseScore = raw.find_all('a')[1].get_text().split(':')[-1]

        GetScores.append(GetScore)
        LoseScores.append(LoseScore)

        if int(GetScore) > int(LoseScore):
            Result.append('1')
        else:
            Result.append('0')


    HomeRecentData = pd.DataFrame({'득점': GetScores, '실점': LoseScores, '승패': Result},Dates)


    return AwayRecentData,HomeRecentData


def GetAllGameData(preview_soup,log_soup,GameInfo):

    AwayBattingOrder = away_batting_order(log_soup)
    
    HomeBattingOrder = home_batting_order(log_soup)
    AwayScore, HomeScore = game_score(log_soup)
    AwayVersus,HomeVersus = get_versus_data(preview_soup)
    AwayRecent,HomeRecent = team_recent_result(preview_soup)
    Awaypitcher,Homepitcher = start_pitcher(preview_soup)

    
    if type(AwayBattingOrder) == bool or type(HomeBattingOrder) == bool \
        or type(Awaypitcher) == bool or type(Homepitcher) == bool:
        return False
    

    with pd.ExcelWriter(f'/home/swha/ToTo/ToTo/Data/raw/game/{GameInfo}_{AwayScore}_{HomeScore}.xlsx') as tmp:
    
        AwayVersus.to_excel(tmp,sheet_name='AwayVersus')
        AwayRecent.to_excel(tmp,sheet_name='AwayRecent')
        Awaypitcher.to_excel(tmp,sheet_name='Awaypitcher')
        AwayBattingOrder.to_excel(tmp,sheet_name='AwayBattingOrder')

        HomeVersus.to_excel(tmp,sheet_name='HomeVersus')
        HomeRecent.to_excel(tmp,sheet_name='HomeRecent')
        Homepitcher.to_excel(tmp,sheet_name='Homepitcher')
        HomeBattingOrder.to_excel(tmp,sheet_name='HomeBattingOrder')

#%%

if __name__ == "__main__":

    import os 
    import numpy as np
    from bs4 import BeautifulSoup

    data_path = '/home/swha/ToTo/ToTo/Data/soup/team_soup_data/'
    exist_data_path = '/home/swha/ToTo/ToTo/Data/raw/game/'
    batters = []
    pitchers = []

    # newDataList = np.setdiff1d(os.listdir(data_path),os.listdir(exist_data_path))

    for soupLog in sorted(os.listdir(data_path)):
        if soupLog.endswith('log'):
            GameInfo = soupLog[:-4]
            # GameInfo = '2017-09-14_부산사직'
            print(soupLog)
            soupPreview = data_path + GameInfo + '_preview'
            soupLog = data_path + soupLog

            logParser = BeautifulSoup(open(soupLog),"html.parser")
            previewParser = BeautifulSoup(open(soupPreview),"html.parser")

            # if not GetAllGameData(previewParser,logParser,GameInfo):
            #     continue
            if not GetAllGameData(previewParser,logParser,GameInfo):
                continue
            else:
                pass
            
        
            for i in range(10):
                
                if i == 9:
                    pitcher = tuple(away_batting_order(logParser).to_numpy().tolist()[i])
                    if pitcher not in pitchers:
                        pitchers.append(pitcher)
                    pitcher = tuple(home_batting_order(logParser).to_numpy().tolist()[i])
                    if pitcher not in pitchers:
                        pitchers.append(pitcher)
                else:
                    batter = tuple(away_batting_order(logParser).to_numpy().tolist()[i])
                    if batter not in batters:
                        batters.append(batter)
                    batter = tuple(home_batting_order(logParser).to_numpy().tolist()[i])
                    if batter not in batters:
                        batters.append(batter)
                
        # break
            
#%%
with pd.ExcelWriter(f'/home/swha/ToTo/ToTo/Data/raw/all_players.xlsx') as tmp:
    pd.DataFrame(batters).to_excel(tmp,sheet_name='Batters')
    pd.DataFrame(pitchers).to_excel(tmp,sheet_name='Pitchers')



#%%

previewParser = BeautifulSoup(open('/home/swha/ToTo/ToTo/Data/soup/team_soup_data/2016-08-16_챔피언스필드_preview'),"html.parser")

soup = previewParser
raw_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div.box-body.no-padding > table')

GetScores = []
LoseScores = []
Result = []
Dates = []
for raw in raw_table.find_all('tr')[1:]:

    DateIdx = str(raw.find_all('a')[1]).find('date')
    Date = str(raw.find_all('a')[1])[DateIdx+5:DateIdx+15]

    Dates.append(Date)

    GetScore = raw.find_all('a')[1].get_text().split(':')[0]
    LoseScore = raw.find_all('a')[1].get_text().split(':')[-1]

    GetScores.append(GetScore)
    LoseScores.append(LoseScore)

    
    if int(GetScore) > int(LoseScore):
        Result.append('1')
    else:
        Result.append('0')


AwayRecentData = pd.DataFrame({'득점': GetScores, '실점': LoseScores, '승패': Result},Dates)

#%%

raw_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div.box-body.no-padding > table')

GetScores = []
LoseScores = []
Result = []
for raw in raw_table.find_all('tr')[1:]:
    GetScore = raw.find_all('a')[1].get_text().split(':')[0]
    LoseScore = raw.find_all('a')[1].get_text().split(':')[-1]

    GetScores.append(raw.find_all('a')[1].get_text().split(':')[0])
    LoseScores.append(raw.find_all('a')[1].get_text().split(':')[-1])

    if GetScore > LoseScore:
        Result.append('1')
    else:
        Result.append('0')


HomeRecentData = pd.DataFrame({'득점': GetScores, '실점': LoseScores, '승패': Result})
