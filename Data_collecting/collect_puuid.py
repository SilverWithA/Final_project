import requests
import pandas as pd
import time
import pymysql.cursors

from db_functions import *
from setting import *


def collect_puuid(collect_cnt, summoner_names):
    """collect_cnt만큼의 유저수, 닉네임 리스트(summnor_names)를 받아 puuid와 닉네임을 담은 playerinfo_df를 반환하는 함수"""
    playerinfo_df = pd.DataFrame(columns=['summonerName', 'puuid'])

    for i in range(collect_cnt):

        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_names[i] + "?api_key=" + api_key
        r = requests.get(puuid_url)
        print(i, "번째 데이터를 가져오고 있습니다.")

        if 'status' in r.json():
            # (1) 조회할 수 없는 회원 일 때 - 'Data not found - summoner not found'
            if r.json()['status']['message'] == 'Data not found - summoner not found':
                print("조회할 수 없는 회원입니다.")
                continue
            # (2) 조회 리밋이 걸렸을 때 - 'Rate limit exceeded' -> 시간 텀(2분)을 뒀다가 다시 조회 시작
            elif r.json()['status']['message'] == 'Rate limit exceeded':

                print("2분 쉬어갑니다.")
                time.sleep(120)
                r = requests.get(puuid_url)
                print(i, "번째 데이터를 다시 가져오고 있습니다.: ", r.json())

            # (1),(2)번의 경우도 아닐 때 해당 닉네임 조회는 넘어감  - continue
            else:
                continue

        # 정보가 행단위로 playerinfo_df에 생성되도록 구성
        meta_summonerName = r.json()["name"]
        meta_puuid = r.json()["puuid"]

        playerinfo_df.loc[i] = [meta_summonerName, meta_puuid]
    return playerinfo_df
def puuid_Chall(collect_cnt):
    "Challenger의 닉네임과 puuid를 불러와 저장하는 함수"
    print("challenger의 usrinfo 조회를 시작합니다. -----------------------------")

    # API에서 puuid 불러오기
    challen_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(challen_url)

    callen_count = len(r.json()["entries"])
    print("챌린저 거주 인구 수: ", callen_count)


    # puuid 조회를 위해 모든 닉네임 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(callen_count):
        summonerNames.append(r.json()["entries"][i]["summonerName"])

    # API에서 puuidID 호출
    playerinfo_df = collect_puuid(collect_cnt,summonerNames)

    # MySQL의 저장하기
    playerinfo_df.to_sql(name='chall_usrinfo', con=conn_Usr, if_exists='append',index=False)
    print("chall_usrinfo Table에 데이터를 저장하였습니다.")
def puuid_grand(collect_cnt):
    """grandmaster의 닉네임과 puuid를 불러와 저장하는 함수"""

    print("grandmaster의 usrinfo 조회를 시작합니다. -----------------------------")

    # API에서 그마 닉네임 불러오기
    grand_url = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(grand_url)

    # grand_count = len(r.json()["entries"])
    # print("그마 거주 인구 수: ", grand_count)

    # puuid 조회를 위해 모든 닉넨임을 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(collect_cnt):
        summonerNames.append(r.json()["entries"][i]["summonerName"])


    # puuidID까지 조회해서 playerinfo_df에 저장하기
    playerinfo_df = collect_puuid(collect_cnt,summonerNames)

    # MySQL의 저장하기
    playerinfo_df.to_sql(name='grand_usrinfo', con=conn_Usr, if_exists='append', index=False)
    print("grand_usrinfo Table에 데이터를 저장하였습니다.")
def puuid_mast(collect_cnt):
    """master 닉네임과 puuid를 불러와 저장하는 함수"""
    print("master의 usrinfo 조회를 시작합니다. -----------------------------")

    # API에서 마스터 닉네임 불러오기
    mast_url = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(mast_url)

    # mast_count = len(r.json()["entries"])
    # print("마스터 거주 인구 수: ", mast_count)

    # puuid 조회를 위해 모든 닉넨임을 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(collect_cnt):
        summonerNames.append(r.json()["entries"][i]["summonerName"])

    # puuidID 추출하기:SUMMONER-V4 ---------------------------------------
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)

    # MySQL의 저장하기
    playerinfo_df.to_sql(name='mast_usrinfo', con=conn_Usr, if_exists='append', index=False)
    print("mast_usrinfo Table에 데이터를 저장하였습니다.")
def under_dia(tier_lowCase, collect_cnt):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    print(tier_lowCase,"티어의 usrinfo를 조회합니다--------------------------------------------")

    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt//4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt+mod]
    div_num = ["I","II","III","IV"]


    summonerNames = []
    # 티어별 닉네임만 가져오기 API
    for i in range(len(div_cnt)):
        pages = (div_cnt[i]// 200)+1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")


        for page in range(1,int(pages)+1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + str(api_tier[tier_lowCase]) + "/" + div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

        # print("summoner_df의 정보의 길이: ", len(summonerNames))


    # puuid 따오기
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)

    # MySQL의 저장하기
    save_name = str(tier_lowCase) + "_usrinfo"
    playerinfo_df.to_sql(name=save_name, con=conn_Usr, if_exists='append', index=False)

    print(save_name,"Table에 데이터를 저장하였습니다.")
def exe_coll_puuid():
    """usrinfo DB에 데이터를 모으는 작업을 실행하는 함수"""

    # 저장 전 DB 데이터 초기화
    trun_tables(engine_name=engine_Usr)

    # 티어 순서대로 데이터 불러오기 -> 저장하기
    puuid_Chall(tier_cnt['chall'])
    puuid_grand(tier_cnt['grand'])
    puuid_mast(tier_cnt['mast'])

    # 다이아 이하의 티어에 대해 데이터 저장하기
    for i in range(len(lowCase[3:])):
        under_dia(tier_lowCase=lowCase[i+3],
                  collect_cnt=tier_cnt[lowCase[i+3]])

    # 완료
    print("모든 usrinfo 데이터가 저장되었습니다 ----------fin---------")
    conn_Usr.close()


# 함수 실행
# exe_coll_puuid()