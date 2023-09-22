import pandas as pd
import time
import requests

from sqlalchemy import create_engine
from sqlalchemy import text

from db_functions import *





# 3. API에서 matchID를 불러와 저장하는 함수
def collect_matchID(select_df,save_name):
    """Riot API에서 puuid를 사용하여 matchID를 불러오는 함수"""

    matchid_list = []
    matchid_df = pd.DataFrame()

    print("조회할 유저는: ", len(select_df),"명 입니다.")

    for i in range(len(select_df)):
        match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + select_df["puuid"][i] + "/ids?start=0&count=20&api_key=" + api_key
        r = requests.get(match_url)
        print(f"현재 {i}번째 puuid에 대한 matchID 20개를 불러왔습니다.")


        # 디버깅 - 리밋 걸렸을 때 2분 쉬기
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
    print("matchID 정보를 모두 불러와 matchid_list에 저장했습니다.")

    # 같은 티어 내 matchID 중복 제거 작업 ------------------------------------
    print("중복 제거 전 길이: ", len(matchid_list))
    matchid_list = set(matchid_list)

    print("중복 제거 전 길이: ", len(matchid_list))
    matchid_list = list(matchid_list)

    matchid_df = pd.DataFrame({"MatchId": matchid_list})
    print("===============MatchID를 df화 하였습니다============")

    matchid_df.to_sql(name=save_name, con=conn_mat, if_exists='append', index=False)
    print("MatchID를", save_name,"이라는 테이블로 DB에 저장하였습니다.")


# 4. 저장 과정 실행히줄 함수 정의
def exe_collMatchId():
    UsrPerTier = show_tables(engine_Usr)
    for i in range(len(UsrPerTier)):

        save_name = str(UsrPerTier[i][0])[:-8] + "_mat"

        collect_matchID(select_db(table_name= UsrPerTier[i][0],
                                  conn_name=conn_Usr),
                        save_name=save_name)


# 데이터 비우기
# trun_tables(engine_mat)

# matchID 수집 실행 함수
exe_collMatchId()

















