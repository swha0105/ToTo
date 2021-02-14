#%%
from IPython import get_ipython
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


#%%
def find_table_batter(soup):
    a = soup.find('div', {'class':'wrapper'})
    b = a.find('div', {'class':'content-wrapper'})
    c = b.find('div', {'class':'container'})
    d = c.find('section', {'class':'content'})
    e = d.find('div', {'class':'row'})
    f = e.find_all('div', {'class':'col-md-12 col-xs-12 col-sm-12 col-lg-12'})[-1]
    g = f.find('div', {'class':'row'})
    try:
        h = g.find_all('div', {'class':'col-xs-12', 'style': 'padding-bottom:5px;'})[-1]
    except AttributeError:
        return [],[]


    h = g.find_all('div', {'class':'col-xs-12', 'style': 'padding-bottom:5px;'})[-1]
    i = h.find('div', {'class':'box'})
    j = i.find('div', {'class':'box-body no-padding table-responsive'})
    k = j.find('table', {'class':'table table-striped table-responsive table-condensed no-space table-bordered'})
    l = k.find_all('tr', {'class':'oddrow_stz0'})

    l_colhead = k.find_all('tr', {'class':'colhead_stz0'})
    l_oddrow = k.find_all('tr', {'class':'oddrow_stz0'})
    l_evenrow = k.find_all('tr', {'class':'evenrow_stz0'})
    
    return l_oddrow, l_evenrow


#%%
def write_table_batter(l_oddrow, l_evenrow, name, year, path,birth):
    season_list = []
    for odd in l_oddrow:
        elements = odd.find_all('td', {'style':'white-space:nowrap;text-align:center;vertical-align:middle;'})
        elements2 = odd.find_all('td', {'style':'border-left:2px solid #333333;white-space:nowrap;text-align:center;vertical-align:middle;'})

        daily_list = []

        for element in elements:
            string = element.find('span', {'style':'padding-left:3px;padding-right:3px;'}).text
            daily_list.append(string)
        for element2 in elements2:
            string2= element2.find('span', {'style':'padding-left:3px;padding-right:3px;'}).text
            daily_list.append(string2)
        season_list.append(daily_list)
    for even in l_evenrow:
        elements = even.find_all('td', {'style':'white-space:nowrap;text-align:center;vertical-align:middle;'})
        elements2 = even.find_all('td', {'style':'border-left:2px solid #333333;white-space:nowrap;text-align:center;vertical-align:middle;'})

        daily_list = []

        for element in elements:
            string = element.find('span', {'style':'padding-left:3px;padding-right:3px;'}).text
            daily_list.append(string)
        for element2 in elements2[:-2]:
            string2= element2.find('span', {'style':'padding-left:3px;padding-right:3px;'}).text
            daily_list.append(string2)
        season_list.append(daily_list)
    df_season = pd.DataFrame(season_list)
    cols_index = ['Date', 'Opposite', 'Score', 'Batorder','Position', 'Atbats', 'Run', 'Hit', 'Double', 'Triple', 'HR', 'TotalHit', 'RBI', 'SB', 'SBFail', 'BB', 'HBP', 'IntentionalBB', 'SO', 'DoublePlay', 'SacriHit', 'SacriFly', 'AVG', 'SLG', 'OPS', 'Pitches', 'RE24', 'WPA', 'Started', 'OBP', 'avLI']
    df_season.columns = cols_index
    dataframe_season=df_season.sort_values(by= ['Date']).reset_index().drop(columns='index')
    dataframe_season.insert(0, 'Year', year)
    dataframe_season.insert(0, 'Name', name)
    dataframe_season.to_csv(path+name+'_'+birth+'_'+year+'.csv', encoding='cp949', index=False)


#%%
data_path = '../Data/data_processing.xlsx'

# team_names = ['SK','두산','한화','키움','KIA','삼성','롯데','LG','KT','NC']
team_names = ['두산','한화','키움','KIA','삼성','롯데','LG','KT','NC']


players = set()

for team in team_names:

    batter_sheet = pd.read_excel(data_path,sheet_name=team)
   
    position = batter_sheet['포지션'] 
    batter_name = batter_sheet['이름']
    batter_birthday = batter_sheet['생년월일']
    
    for pos,name,birth in zip(position,batter_name,batter_birthday):
        if pos != '투수':
            players.add( (name,str(birth)[:10]) )        

    

#%%

result_folder = '/home/ha/projects/Toto/Data/batter/'

path = os.path.join(str(os.getcwd()), result_folder)
if not os.path.isdir(path):
     os.mkdir(path)
#%%
yrs_list = ['2017', '2018', '2019','2020']
for name,birth in players:
    for year in yrs_list:
        print(name,year)

        url = 'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name='+name+'&birth='+birth+'&re=0&se=&da=&year='+year+'&cv='
        # url = 'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name='+name+'&birth='+birth
        # url = 'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name=%EB%AC%B8%EC%8A%B9%EC%9B%90&birth=1989-11-28'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # a = soup.find('div', {'class':'wrapper'})
        # b = a.find('div', {'class':'content-wrapper'})
        # c = b.find('div', {'class':'container'})
        # d = c.find('section', {'class':'content'})
        # e = d.find('div', {'class':'row'})
        # f = e.find_all('div', {'class':'col-md-12 col-xs-12 col-sm-12 col-lg-12'})[-1]
        # g = f.find('div', {'class':'row'})
        # try:
        #     h = g.find_all('div', {'class':'col-xs-12', 'style': 'padding-bottom:5px;'})[-1]
        # except AttributeError:
        #     continue 
        # # 타자 정보 없음.
        # i = h.find('div', {'class':'box'})
        # j = i.find('div', {'class':'box-body no-padding table-responsive'})
        # k = j.find('table', {'class':'table table-striped table-responsive table-condensed no-space table-bordered'})
        # l = k.find_all('tr', {'class':'oddrow_stz0'})

        # l_colhead = k.find_all('tr', {'class':'colhead_stz0'})
        # l_oddrow = k.find_all('tr', {'class':'oddrow_stz0'})
        # l_evenrow = k.find_all('tr', {'class':'evenrow_stz0'})


        l_oddrow, l_evenrow = find_table_batter(soup)
        if len(l_oddrow) == 0: # 그 연도에 데이터 없음 
            continue

        write_table_batter(l_oddrow, l_evenrow, name, year, path, birth)


#%%

    