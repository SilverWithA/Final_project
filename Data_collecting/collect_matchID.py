import pandas as pd
import time
import requests

from sqlalchemy import create_engine
from sqlalchemy import text

from db_functions import *


# 0. 기본 설정
# (1) product api키 설정
api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"


# (2) MongoClient를 이용한 연결 기본 설정
client = MongoClient('mongodb://localhost:27017/')

# # 1. DB 연결
# # (1) MongoDB - 사용할 db를 use_db  변수에 저장
db_mat = client.mat_info   # 연결할 db 선택
use_matcoll = db_mat.matchIds   # 연결할 때 마다 collection의 형태임 -- collection이 없으면 새로 만드는 구조


# 3. API에서 matchID를 불러와 저장하는 함수
def collect_matchID(select_df,lowCase_tier):
    """Riot API에서 puuid를 사용하여 matchID를 불러오는 함수"""

    matchid_list = []

    print(lowCase_tier, "에서 조회할 유저는: ", len(select_df),"명 입니다=======================================")

    for i in range(len(select_df)):
        match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + select_df["puuid"][i] + "/ids?start=0&count=20&api_key=" + api_key
        r = requests.get(match_url)
        print(f"현재 {i}번째 puuid에 대한 matchID 20개를 불러왔습니다.")


        # api 키 리밋 걸렸을 때 2분 쉬기
        if 'status' in  r.json():
            # 2분에 조회가능한 api 횟수는 100번임
            if r.json()['status']['message'] == 'Rate limit exceeded':
                print("api 조회 리밋에 걸렸습니다. 2분 쉬어갑니다.")
                time.sleep(120)
                r = requests.get(match_url)
                print("리밋이 풀렸습니다.", i,"번째 데이터를 다시 가져오고 있습니다.: ", r.json())
            else:
                # api 조회 제한 이외의 오류는 그냥 넘어가 다음 정보를 조회하도록 설정
                continue

        matchid_list += r.json()

    # 같은 티어 내 matchID 중복 제거 작업 ------------------------------------
    print(lowCase_tier,"중복 제거 전 길이: ", len(matchid_list))
    matchid_list = set(matchid_list)

    print(lowCase_tier,"중복 제거된 길이: ", len(matchid_list))
    matchid_list = list(matchid_list)


    # mat_doc 딕셔너리에 value값에 동일 티어 matchId를 모두 넣는다
    tier_mat = lowCase_tier + "_mat"
    mat_doc = {str(tier_mat):matchid_list}
    print(lowCase_tier, " 의 MatchID를 도큐먼트로 보내기위해 딕셔너리 타입으로 변환하였습니다.")
    return mat_doc


# 4. 저장 과정 실행히줄 함수 정의
def exe_collMatchId():
    use_matcoll.drop()  # 콜렉션 비우기


    UsrPerTier = show_tables(engine_Usr)   # MySQL usrinfo DB에 있는 모든 table 저장
    for i in range(len(UsrPerTier)):

        # MySQL DB에 저장된 table을 데이터 프레임으로 받아오기
        usr_df = select_db(UsrPerTier[i][0], conn_Usr)
        lowCase_tier = str(UsrPerTier[i][0])[:-8]

        # 데이터프레임으로 받아온 정보를 기반으로 api에서 matchID 조회
        mat_doc = collect_matchID(usr_df,lowCase_tier)

        # 조회한 matchID를 딕셔너리 형태(mat_doc)으로 만들어 MongoDB로 쏴준다
        # 티어별로 하난의 도큐먼트가 만들어지고 해당 티어의 경기코드가 전부 value값으로 들어간다
        result = use_matcoll.insert_one(mat_doc)   # 콜랙션에 티어별 도큐먼트 insert
        print("MongDB에 저장했습니다.")



# 데이터 비우기
# trun_tables(engine_mat)

# matchID 수집 실행 함수
# df = show_tables(engine_Usr)
# print(df[1][0])
# print(len(df[1][0]))

exe_collMatchId()

















