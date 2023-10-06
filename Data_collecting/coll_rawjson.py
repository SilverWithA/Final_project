import requests
import pandas as pd
import time

from pymongo import MongoClient
from setting import *
from db_functions import *

def call_api(lowCase_tier,mat_list):
    # cnt = tier_cnt[str(lowCase_tier)]
    cnt = len(mat_list)
    print(lowCase_tier, "에서 조회할 matchid 개수는: ", cnt,"=====================")
    # print(lowCase_tier,"에서 조회할 matchid 개수는: ", len(mat_list), " ===============================")
    tier_list = []
    for i in range(cnt):  # len(mat_list)


        match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + mat_list[i] + "?api_key=" + api_key  # mat_cnt[i]
        mat_info = requests.get(match_url)

        timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + mat_list[i] + "/timeline?api_key=" + api_key
        mat_timeline = requests.get(timeline_url)


        # 리밋 걸리면 2분 쉬어 감
        if 'status' in mat_info.json() or 'status' in mat_timeline.json():
            if mat_info.json()['status']['message'] == 'Rate limit exceeded' or mat_timeline.json()['status']['message'] == 'Rate limit exceeded':
                print("리밋 걸림!!!! 2분 쉬어갑니다 ----------------------------------------")
                time.sleep(120)


                mat_info = requests.get(match_url)
                mat_timeline = requests.get(timeline_url)

            else:
                print("조회하는데 오류가 생겼습니다. 다음을 진행합니다.")
                continue
        else:
            pass


        total_json = {"mat_info": mat_info.json(),
                          "mat_timeline": mat_timeline.json()}

        print(i, "번째 데이터를 조회 후 합쳤습니다.")
        tier_list.append(total_json)  # bulk insert를 위해 list형식에 append함 -> 하나의 collection으로 들어감

    return tier_list    # 한 티어에 대한 경기 정보를 모두 담은 list



def exe_collApiinfo():

    # 모든 티어의 matchID 불러와 저장
    total_match = coll_mat.find()

    # 도큐먼트 속 모든 keys값을 가져옴: 티어별 matchid
    key_names = []   # match 정보가 있는 key값 이름들
    tier_mat = []    # 각 콜렉션의 모든 정보를 담은 딕셔너리를 원소값으로 갖는 리스트

    for x in total_match:
        key_names.append(list(x.keys())[1])
        tier_mat.append(x)
    print("MongoDB mat_info DB에 있는 matchId 콜렉션 속 도큐먼트 key 값: ", key_names)

    # print(tier_mat[0][str(key_names[0])])



    for i in range(len(key_names)):   # tier iterate   # len(key_names)
        lowCase_tier = str(key_names[i])[:-4]  #  str(key_names[i])[:-4]

        # api_info에 저장할 collection 이름
        if lowCase_tier == 'chall':
            use_col = db_raw.chall_total
        elif lowCase_tier == 'grand':
            use_col = db_raw.grand_total
        elif lowCase_tier == 'mast':
            use_col = db_raw.mast_total

        elif lowCase_tier == 'dia':
            use_col = db_raw.dia_total
        elif lowCase_tier == 'em':
            use_col = db_raw.em_total
        elif lowCase_tier == 'pla':
            use_col = db_raw.pla_total
        elif lowCase_tier == 'gold':
            use_col = db_raw.gold_total
        elif lowCase_tier == 'sil':
            use_col = db_raw.sil_total
        elif lowCase_tier == 'bro':
            use_col = db_raw.bro_total
        else:
            use_col = db_raw.iron_total


        use_col.drop()         # 콜렉션 비우기
        print("mat_info의 모든 콜렌션을 비웠습니다.")

        print("lowCase_tier: ", lowCase_tier)  # tier에 해당하는 소문자

        # 조회할 때 사용할 티어별 모든 matchID 리스트에 저장하기
        mat_list = list(tier_mat[i][str(key_names[i])])  # list(tier_mat[i][str(key_names[i])])
        # print(mat_list)

        # api 전체 데이터 불러오기
        info_list = call_api(lowCase_tier,mat_list)


        # 각 collection에 insert 한꺼번에 하기
        use_col.insert_many(info_list)
        print(lowCase_tier,"_total collection에 데이터를 저장했습니다.")

exe_collApiinfo()

