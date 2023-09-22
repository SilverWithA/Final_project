import requests
import pandas as pd
import time
from sqlalchemy import create_engine
from sqlalchemy import text
from db_functions import *


api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"
def exe_collUsrinfo(CollectPerTier):
    """CollectPerTier: 티어별로 모을 유저 정보의 개수로 딕셔너리 타입으로 넣어주세요"""
    print("티어별 데이터를 조회 후 스테이징 영역에 저장을 시작합니다.")

    for i in range(len(db_talbes)):

        print(db_talbes[i][0],"의 티어 유저 정보를 저장하기 전 5초 쉬어갑니다.")
        # time.sleep(5)

        lowCase_tier = str(db_talbes[i][0])[:-8]
        print("데이터를 수집할 티어의 소문자 철자는: ", lowCase_tier)
        if lowCase_tier == 'chall':
            puuid_Chall(CollectPerTier['chall_cnt'])

        elif lowCase_tier == "grand":
            puuid_grand(CollectPerTier['grand_cnt'])

        elif lowCase_tier == "mast":
            puuid_mast(CollectPerTier['mast_cnt'])

        else:
            cnt = lowCase_tier + "_cnt"
            puuid_underdia(lowCase_tier, CollectPerTier[cnt])



# 3. 닉네임을 받으면(summnorName) -> puuid를 알려주는 함수:collect_puuid
def collect_puuid(collect_cnt, summoner_list):
    """닉네임 리스트(summnor_names)를 받아 puuid와 닉네임을 담은 playerinfo_df를 반환하는 함수"""
    playerinfo_df = pd.DataFrame(columns=['summnorName', 'puuid'])


    for i in range(collect_cnt):

        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_list[i] + "?api_key=" + api_key

        r = requests.get(puuid_url)
        print(i, "번째 puuid 데이터를 가져오고 있습니다.")

        if 'status' in r.json():
            # (1) 조회할 수 없는 회원 일 때 - 'Data not found - summoner not found'
            if r.json()['status']['message'] == 'Data not found - summoner not found':
                print("조회할 수 없는 회원입니다.")
                continue
            # (2) 조회 리밋이 걸렸을 때 - 'Rate limit exceeded' -> 시간 텀(2분)을 뒀다가 다시 조회 시작
            elif r.json()['status']['message'] == 'Rate limit exceeded':

                print("리밋에 걸렸습니다. 2분 쉬어갑니다.")
                time.sleep(120)
                print("정보를 다시 조회합니다.")
                r = requests.get(puuid_url)

            # (1),(2)번의 경우도 아닐 때 해당 닉네임 조회는 넘어감  - continue
            else:
                continue

        # 정보가 행단위로 playerinfo_df에 생성되도록 구성
        meta_summonerName = r.json()["name"]
        meta_puuid = r.json()["puuid"]

        playerinfo_df.loc[i] = [meta_summonerName, meta_puuid]
    return playerinfo_df

# 4. 티어별로 닉네임을 받아오고 -> collect_puuid를통해 puuid까지 받아 df로 저장
# collect_cnt개수만큼 유저 닉네임,puuid를 저장한다.
def puuid_Chall(collect_cnt):
    "Challenger의 닉네임과 puuid를 불러와 저장하는 함수"


    # API에서 챌린저 닉네임 불러오기
    challen_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(challen_url)

    # callen_count = len(r.json()["entries"])
    # print("챌린저 거주 인구 수: ", callen_count)

    # puuid 조회를 위해 모든 닉넨임을 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(collect_cnt):
        summonerNames.append(r.json()["entries"][i]["summonerName"])


    playerinfo_df = collect_puuid(collect_cnt, summonerNames)

    # # MySQL의 저장하기
    playerinfo_df.to_sql(name="chall_usrinfo", con=conn_Usr, if_exists='append', index=False)
def puuid_grand(collect_cnt):
    """grandmaster의 닉네임과 puuid를 불러와 저장하는 함수"""

    # API에서 그마 닉네임 불러오기
    grand_url = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(grand_url)

    # grand_count = len(r.json()["entries"])
    # print("그마 거주 인구 수: ", grand_count)

    # puuid 조회를 위해 모든 닉넨임을 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(collect_cnt):
        summonerNames.append(r.json()["entries"][i]["summonerName"])


    # puuidID 추출하기:SUMMONER-V4 ---------------------------------------
    playerinfo_df = collect_puuid(collect_cnt,summonerNames)

    # DB에 저장
    playerinfo_df.to_sql(name="grand_usrinfo", con=conn_Usr, if_exists='append', index=False)
def puuid_mast(collect_cnt):
    """master 닉네임과 puuid를 불러와 저장하는 함수"""

    # API에서 마스터 닉네임 불러오기
    grand_url = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(grand_url)

    # mast_count = len(r.json()["entries"])
    # print("마스터 거주 인구 수: ", mast_count)

    # puuid 조회를 위해 모든 닉넨임을 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(collect_cnt):
        summonerNames.append(r.json()["entries"][i]["summonerName"])

    # puuidID 추출하기:SUMMONER-V4 ---------------------------------------
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)

    # MySQL의 저장하기
    playerinfo_df.to_sql(name="mast_usrinfo", con=conn_Usr, if_exists='append', index=False)
def puuid_underdia(lowCase_tier, collect_cnt):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt // 4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt + mod]
    div_num = ["I", "II", "III", "IV"]
    summonerNames = []

    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for i in range(len(div_cnt)):
        # print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
        pages = (div_cnt[i] // 200) + 1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")

        for page in range(1, int(pages) + 1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + API_tiers[str(lowCase_tier)] + "/" + \
                           div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)

    save_name = str(lowCase_tier) + "_usrinfo"
    # MySQL의 저장하기
    playerinfo_df.to_sql(name=save_name, con=conn_Usr, if_exists='append', index=False)





# [2]. 함수 실행 구문
# 1. 티어별로 수집할 유저 정보의 개수 미리 지정

# 티어별 lowerCase 이름과 대응되는 API상에 티어 이름 지정 - (다이아 이하 티어만)
API_tiers = {"dia":"DIAMOND","em":"EMERALD","pla":"PLATINUM",
             "gold":"GOLD","sil":"SILVER","bro":"BRONZE","iron":"IRON"}

# 티어별 받아올 유저 정보 개수 지정
CollectPerTier = {'chall_cnt':10, 'grand_cnt':20,'mast_cnt':70,
                      'dia_cnt':250, 'em_cnt': 850, 'pla_cnt': 1500,
                      'gold_cnt':1900, 'sil_cnt':1800,'bro_cnt':1800, 'iron_cnt':800}

try:
    db_talbes = show_tables(engine_Usr)
    print("데이터를 조회할 테이블의 순서: ",db_talbes)

    # 모든 테이블에 데이터 삭제
    trun_tables(engine_Usr)

    # 2. DB 저장 실행
    exe_collUsrinfo(CollectPerTier)
    conn_Usr.close()

except Exception as e:
    print(e)