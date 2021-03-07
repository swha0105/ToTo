import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def find_order_data(soup):
    a = soup.find('div', {'class':'wrapper'})
    b = a.find('div', {'class':'content-wrapper'})
    c = b.find('div', {'class':'container'})
    d = c.find('section', {'class':'content'})
    e = d.find('div', {'class':'row'})
    f = e.find_all('div', {'class':'col-md-12 col-xs-12 col-sm-12 col-lg-12'})[-1]
    g = f.find('div', {'class':'row'})
    l_oddrow = g.find_all('tr', {'class':'oddrow_stz'})
    l_colhead = g.find_all('tr', {'class':'colhead_stz'})
    l_evenrow = g.find_all('tr', {'class':'evenrow_stz'})

    f1 = e.find_all('div', {'class':'col-md-12 col-xs-12 col-sm-12 col-lg-12'})[0]
    g1 = f1.find('div', {'class':'row'})
    h1 = g1.find('div', {'class':'col-xs-12 col-sm-12 col-md-12 col-lg-4'})
    try:
        i1 = h1.find('div',{'class':'callout'})
    except AttributeError:
        return [],[],[],[]

    j1 = i1.find('div',{"style":"float:left;width:50%;text-align:center;"})
    scores = j1.find('span').get_text()

    return l_oddrow, l_evenrow, scores.split(":")[0],scores.split(":")[1]


def write_order_table(l_oddrow, l_evenrow,away_score,home_score):
    names = [ ]
    births = []
    length = len(l_oddrow)
    for i in range(length):
        tmp_info = l_oddrow[i].find('a')
        names.append(tmp_info.get_text())       
        birth_index = str(tmp_info).index('birth')
        births.append(str(tmp_info)[birth_index+6:birth_index+16])

        tmp_info = l_evenrow[i].find('a')
        names.append(tmp_info.get_text())       
        birth_index = str(tmp_info).index('birth')
        births.append(str(tmp_info)[birth_index+6:birth_index+16])

        # order_tuple = list(map(tuple,zip(names,births)))
        # order_tuple.append([away_score,home_score])
        # order_data = pd.DataFrame(order_tuple)
        
        cols_index = ['away_name', 'away_birth','home_name', 'home_birth']
        
    frame_data =  [ names[:length],births[:length],names[length:],births[length:] ]
    # frame_data.append([away_score,away_score,home_score,home_score])
    
    order_frame = pd.DataFrame(zip(*frame_data),columns=cols_index)
    # order_frame.append([away_score,away_score,home_score,home_score])
        # order_data.columns = cols_index
   
        # order_data.to_csv(path+date+'_'+stadium+'.csv', encoding='cp949', index=False)
    # order_frame = pd.DataFrame(list(map(list,zip(*[order_data[0],order_data[1]]))),columns=cols_index)
    return order_frame,away_score,home_score


def GetVersusData(soup):

    a = soup.find('div', {'class':'wrapper'})
    b = a.find('div', {'class':'content-wrapper'})
    c = b.find('div', {'class':'container'})
    d = c.find('section', {'class':'content'})
    e = d.find('div', {'class':'row'})

    f = e.find_all('div', {'class':'col-md-12 col-xs-12 col-sm-12 col-lg-12'})[-1]
    g = f.find('div', {'class':'row'})
    h = g.find_all('div',{'class': 'col-xs-12 col-sm-6'})[0]
    i = h.find('div',{'class': 'box'})
    j = i.find('div',{'class': 'box-body no-padding'})
    k = j.find('table',{'class': 'table table-striped'})

    away_team = k.find_all('th')[1].text
    home_team = k.find_all('th')[2].text

    season_away = k.find_all('tr')[2].text.split('\n')[1]
    season_home = k.find_all('tr')[2].text.split('\n')[2]

    AwayTeam_AwaySeasonResult = k.find_all('tr')[4].text.split('\n')[1]
    HwayTeam_HomeSeasonResult = k.find_all('tr')[3].text.split('\n')[2]

    GetScore = k.find_all('tr')[5].text.split('\n')
    Away_GetScore = GetScore[1]
    Home_GetScore = GetScore[2]

    GiveScore = k.find_all('tr')[6].text.split('\n')
    Away_GiveScore = GiveScore[1]
    Home_GiveScore = GiveScore[2]

    VersusResult = k.find_all('tr')[7].text.split('\n')[1]

    away = [season_away,AwayTeam_AwaySeasonResult,Away_GetScore,Away_GiveScore]
    home = [season_home,HwayTeam_HomeSeasonResult,Home_GetScore,Home_GiveScore]

    index = ['시즌','홈원정결과','득점','실점']
    versus_data = pd.DataFrame(list(map(list,zip(*[away,home]))),columns=[away_team,home_team],index=index)

    return versus_data


def GetPitcher(soup):

    a = soup.find('div', {'class':'wrapper'})
    b = a.find('div', {'class':'content-wrapper'})
    c = b.find('div', {'class':'container'})
    d = c.find('section', {'class':'content'})
    e = d.find('div', {'class':'row'})

    f = e.find_all('div', {'class':'col-md-12 col-xs-12 col-sm-12 col-lg-12'})[-1]
    g = f.find('div', {'class':'row'})
    h = g.find_all('div',{'class': 'col-xs-12 col-sm-6'})[-1]
    i = h.find('div',{'class': 'box'})
    j = i.find('div',{'class': 'box-body no-padding'})
    k = j.find('table',{'class': 'table table-striped'})

    away_pitcher = k.find_all('tr')[2].text.split('\n')[1]
    home_pitcher = k.find_all('tr')[2].text.split('\n')[2]

    AwayPitcher_Season = k.find_all('tr')[4].text.split('\n')[1]
    HomePitcher_Season = k.find_all('tr')[4].text.split('\n')[2]

    AwayPitcher_Season_game = AwayPitcher_Season.split(" ")[0]
    HomePitcher_Season_game = HomePitcher_Season.split(" ")[0]
    
    try:
        AwayPitcher_Season_win = AwayPitcher_Season.split(" ")[1]
    except IndexError:  # 선발투수 정보 누락
        return False 
    HomePitcher_Season_win = HomePitcher_Season.split(" ")[1]
    
    AwayPitcher_Season_lose = AwayPitcher_Season.split(" ")[2]
    HomePitcher_Season_lose = HomePitcher_Season.split(" ")[2]

    AwayPitcher_Season_defense = AwayPitcher_Season.split(" ")[3]
    HomePitcher_Season_defense = HomePitcher_Season.split(" ")[3]


    AwayPitcher_Versus = k.find_all('tr')[5].text.split('\n')[1]
    HomePitcher_Versus = k.find_all('tr')[5].text.split('\n')[2]

    AwayPitcher_Versus_game = AwayPitcher_Versus.split(" ")[0]
    HomePitcher_Versus_game = HomePitcher_Versus.split(" ")[0]
    
    AwayPitcher_Versus_win = AwayPitcher_Versus.split(" ")[1]
    HomePitcher_Versus_win = HomePitcher_Versus.split(" ")[1]
    
    AwayPitcher_Versus_lose = AwayPitcher_Versus.split(" ")[2]
    HomePitcher_Versus_lose = HomePitcher_Versus.split(" ")[2]

    AwayPitcher_Versus_defense = AwayPitcher_Versus.split(" ")[3]
    HomePitcher_Versus_defense = HomePitcher_Versus.split(" ")[3]


    AwayPitcher_Recent = k.find_all('tr')[6].text.split('\n')[1]
    HomePitcher_Recent = k.find_all('tr')[6].text.split('\n')[2]

    AwayPitcher_Recent_game = AwayPitcher_Recent.split(" ")[0]
    HomePitcher_Recent_game = HomePitcher_Recent.split(" ")[0]
    
    AwayPitcher_Recent_win = AwayPitcher_Recent.split(" ")[1]
    HomePitcher_Recent_win = HomePitcher_Recent.split(" ")[1]
    
    AwayPitcher_Recent_lose = AwayPitcher_Recent.split(" ")[2]
    HomePitcher_Recent_lose = HomePitcher_Recent.split(" ")[2]

    AwayPitcher_Recent_defense = AwayPitcher_Recent.split(" ")[3]
    HomePitcher_Recent_defense = HomePitcher_Recent.split(" ")[3]


    away = [AwayPitcher_Season_game,AwayPitcher_Season_win,AwayPitcher_Season_lose,\
        AwayPitcher_Season_defense,AwayPitcher_Versus_game,AwayPitcher_Versus_win, \
            AwayPitcher_Versus_lose,AwayPitcher_Versus_defense,AwayPitcher_Recent_game, \
                AwayPitcher_Recent_win,AwayPitcher_Recent_lose,AwayPitcher_Recent_defense]
    

    home = [HomePitcher_Season_game,HomePitcher_Season_win,HomePitcher_Season_lose,\
        HomePitcher_Season_defense,HomePitcher_Versus_game,HomePitcher_Versus_win, \
            HomePitcher_Versus_lose,HomePitcher_Versus_defense,HomePitcher_Recent_game, \
                HomePitcher_Recent_win,HomePitcher_Recent_lose,HomePitcher_Recent_defense]

    index = ['시즌경기수','시즌승리','시즌패','시즌자책','상대경기수','상대승리','상대패','상대자책','최근경기수','최근승리','최근패','최근자책']
    pitcher_data = pd.DataFrame(list(map(list,zip(*[away,home]))),columns=[away_pitcher,home_pitcher],index=index)

    return pitcher_data



def GetPlayerList_wo_birth(soup):

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

    return player_list

def GetPlayerBirth(soup):

    a = soup.find('div', {'class':'wrapper'})
    b = a.find('div', {'class':'content-wrapper'})
    c = b.find('div', {'class':'container'})
    d = c.find('section', {'class':'content'})
    e = d.find('div', {'class':'row'})
    f = e.find_all('div', {'class':'col-md-12 col-xs-12 col-sm-12 col-lg-12'})[0]
    g = f.find('div', {'class':'row'})
    h = g.find('div', {'class':'col-xs-12 col-sm-4 col-md-4 col-lg-4'})
    i = h.find('div', {'class':'callout'})
    j = i.find('div', {'class':'btn-group'})
    k = j.find('ul', {'class':'dropdown-menu dropdown-menu-left'})
    try:
        l = k.find_all('li')[0]
    except AttributeError:
        return False
    n = re.compile('[0-9]').findall(l.getText())

    return ''.join(n[0:4]) + '-' + ''.join(n[4:6]) + '-' + ''.join(n[6:8])