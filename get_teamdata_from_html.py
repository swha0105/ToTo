#%%
from bs4 import BeautifulSoup
import pandas as pd

log_html = '/home/swha/ToTo/ToTo/soup_data/2017-05-14_잠실_log'
preview_html = '/home/swha/ToTo/ToTo/soup_data/2017-05-14_잠실_preview'

log_soup = BeautifulSoup(open(log_html),"html.parser")
preview_soup = BeautifulSoup(open(preview_html),"html.parser")

def game_score(soup):
    '''
    경기 log 데이터를 받아 경기 점수 생성.
    return: Away팀 득점, Home팀 득점
    '''

    away_get,home_get = soup.select_one('body > div > div.content-wrapper > div > section.content > div > div:nth-child(1) > div > div.col-xs-12.col-sm-12.col-md-12.col-lg-4 > div > div:nth-child(2) > span').get_text().split(':')

    return (away_get,home_get)

def home_batting_order(soup):
    ''' 경기 log 데이터를 받아 홈 배팅오더 데이터 생성.
    return: 선수이름, 생년월일

    '''
    HomeBattingOrder = []

    raw_table = soup.select_one('body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div.box-body.no-padding.table-responsive > table')

    for raw_data in raw_table.find_all('a'):
        birth_index = str(raw_data).index('birth')
        birth = str(raw_data)[birth_index+6:birth_index+16]
        name = raw_data.get_text()

        HomeBattingOrder.append((name,birth))

    return HomeBattingOrder

def away_batting_order(soup):
    ''' 경기 log 데이터를 받아 어웨이 배팅오더 데이터 생성.
    return: 선수이름, 생년월일

    '''
    AwayBattingOrder = []

    raw_table = soup.select_one('body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div.box-body.no-padding.table-responsive > table')

    for raw_data in raw_table.find_all('a'):
        birth_index = str(raw_data).index('birth')
        birth = str(raw_data)[birth_index+6:birth_index+16]
        name = raw_data.get_text()

        AwayBattingOrder.append((name,birth))

    return AwayBattingOrder



def get_versus_data(soup):
    '''
    Input: preview log
    Output: 팀이름, 시즌 승리, 시즌 패배, 홈/원정 승리, 홈/원정 패배, 경기당 득점, 경기당 실점, 상대전적
    '''
    raw_table = soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div.box-body.no-padding > table')
    raw_table_text = [text for text in raw_table.get_text().split('\n') if text != '']

    AwayTeamName = raw_table.find_all('th',limit=3)[1].get_text()
    HomeTeamName = raw_table.find_all('th',limit=3)[2].get_text()

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


    Feature = ['팀이름', '시즌 승리', '시즌 패배', '홈/원정 승리', '홈/원정 패배', '경기당 득점', '경기당 실점', '상대전적 승리']
    AwayInfo = pd.DataFrame([AwayTeamName,AwaySeason_Win,AwaySeason_Lose,AwayResultInStadium_Win,AwayResultInStadium_Lose,\
            AwayGetScore,AwayLoseScore,VersusDataOnlyAwayWin],Feature)

    Feature = ['팀이름', '시즌 승리', '시즌 패배', '홈/원정 승리', '홈/원정 패배', '경기당 득점', '경기당 실점', '상대전적 승리']
    HomeInfo = pd.DataFrame([HomeTeamName,HomeSeason_Win,HomeSeason_Lose,HomeResultInStadium_Win,HomeResultInStadium_Lose,\
            HomeGetScore,HomeLoseScore,VersusDataOnlyHomeWin],Feature)

    return AwayInfo, HomeInfo

def start_pitcher(soup):
    '''
    Input: preview log
    Output: (away, home) 선발투수, 시즌 승리, 시즌 패배, 시즌 자책점, 상대 승리, 상대 패배, 상대 자책점, 최근 30일 승리, 최근 30일 패배, 최근 30일 자책점
    '''
    raw_table = preview_soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div.box-body.no-padding')
    raw_table_text = [text for text in raw_table.get_text().split('\n') if text != '']

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

    Feature = ['선발 투수', '작년 경기', '작년 승리', '작년 패배', '작년 자책점', '상대 경기',\
        '상대 승리', '상대 패배','상대 자책점', '최근(30G) 경기','최근(30G) 승리','최근(30G) 패배','최근(30G) 자책점']
    AwayPitcher = pd.DataFrame([AwayPicther,AwaySeason_Game,AwaySeason_Win,AwaySeason_Lose,AwaySeason_ERA,\
        AwayVersus_Game,AwayVersus_Win,AwayVersus_Lose,AwayVersus_ERA,\
        AwayRecent_Game,AwayRecent_Win,AwayRecent_Lose,AwayRecent_ERA],Feature)

    HomePitcher = pd.DataFrame([HomePicther,HomeSeason_Game,HomeSeason_Win,HomeSeason_Lose,HomeSeason_ERA,\
        HomeVersus_Game,HomeVersus_Win,HomeVersus_Lose,HomeVersus_ERA,\
        HomeRecent_Game,HomeRecent_Win,HomeRecent_Lose,HomeRecent_ERA],Feature)

    return AwayPitcher, HomePitcher


def team_recent_result(soup):
    '''
    Input: preview log
    Output: (away, home) 득점, 실점, 승패 (승리: 1, 패배: 0 )
    '''

    raw_table = preview_soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div.box-body.no-padding > table')

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


    AwayRecentData = pd.DataFrame({'득점': GetScores, '실점': LoseScores, '승패': Result} )


    raw_table = preview_soup.select_one('body > div.wrapper > div.content-wrapper > div > section.content > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div.box-body.no-padding > table')

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


    HomeRecentData = pd.DataFrame({'득점': GetScores, '실점': LoseScores, '승패': Result} )


    return AwayRecentData,HomeRecentData

# %%
