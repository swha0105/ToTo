## 들어가기 전.. 
2019년 6~7월쯤 예전에 다니던 회사에서 야구좋아하는 친한동료들끼리 언제나처럼 수다떨다가 아이디어가 나왔다. 야구 데이터는 수치화가 잘되어있어 머신러닝으로 비교적 간단히 승부 예측이 잘되지 않을까 라는 이야기가 오고갔었다.  
하지만.. 9월에 퇴사하고 울산으로 귀양(?)가는 바람에 아이디어만 오고갔고 제대로 구체화 된건 없었다.  그렇게 잊고 지내다가 최근에 시간이 조금 생겼고 이 아이디어를 구체화시킬 기회라 생각하여 작업중에 있다.  
    
대학 동기인 [QUOPA](https://github.com/QUOPA) 와 함께 작업중에있다.  
 
[Git Repo](https://github.com/swha0105/ToTo)

<br/>

---

## 개요
- [스탯티즈](http://www.statiz.co.kr/main.php) 홈페이지에서 크롤링 하기 쉽게 데이터가 정리 잘되어있고 이를 이용해 데이터를 생성한다.
- 데이터베이스를 구축하여 많은양의 데이터를 처리하기 쉽게 만들 예정이다.  
- 모델은 schema가 잘 정리가 잘되어있는 야구 데이터의 특성을 이용하여 Random forest쓸 예정이고, Fine tuning에 대해서는 아직 구체화된 아이디어는 없다.  
- 모델 Fine tuning을 끝낸 뒤, 매일 생성되는 데이터를 처리하여 새로운 학습데이터로 사용할 수 있는 Pipeline까지 구축하는게 이 프로젝트의 목표이다.  
  
개인적인 목표로는 모델의 정확도, 승부예측의 정확도가 70% 이상이 되는것이 목표이다.


### ~~1. 데이터 생성~~ (완료)
[크롤링](https://github.com/swha0105/ToTo/blob/main/get_soup_from_statiz.py), [경기 데이터 추출](https://github.com/swha0105/ToTo/blob/main/get_teamdata_from_html.py), [선수 데이터 추출](https://github.com/swha0105/ToTo/blob/main/get_playerdata_from_html.py)  코드를 만들어 데이터 생성을 완료했다.

[타자](https://github.com/swha0105/ToTo/blob/main/Data/raw/%EA%B9%80%EC%83%81%EC%88%98_1990-03-23.xlsx) [투수](https://github.com/swha0105/ToTo/blob/main/Data/raw/%EB%B0%B0%EC%98%81%EC%88%98_1981-05-04.xlsx) [경기](https://github.com/swha0105/ToTo/blob/main/Data/raw/2016-07-26_%EB%9D%BC%EC%9D%B4%EC%98%A8%EC%A6%88%ED%8C%8C%ED%81%AC_05_04.xlsx) 데이터 샘플

### 2. 데이터 베이스 구축 및 전처리 (진행중)
- AWS에서 postgresql로 데이터 베이스 구축중. 

### 3. 모델 생성
- random forest 예상.

### 4. fine tuning


### 5. Pipeline 구축
- 매일 경기하는 야구 특성상 매일 생성되는 새로운 데이터를 자동으로 처리해야함.
- 생성되는 데이터를 sql에 넣고, 전처리 과정을 거쳐 모델의 학습데이터로 사용하는 pipeline 구축


