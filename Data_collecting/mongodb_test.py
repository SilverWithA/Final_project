import requests
import pandas as pd
import time
import pprint

from pymongo import MongoClient
from db_functions import *


# 0. 기본 설정
# (1) api키 설정
api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"


# (2) MongoClient를 이용한 연결 기본 설정
client = MongoClient('mongodb://localhost:27017/')

# # 1. DB 연결
# # (1) matchID를 불러올 DB선택
db_mat = client.mat_info   # 연결할 db 선택
coll_mat = db_mat.matchIds   # 연결할 때 마다 collection의 형태임 -- collection이 없으면 새로 만드는 구조

# (2) 정보를 저장할 db 및 collections 확인
db_api = client.api_info




def call_api(mat_list):
    print("조회할 matchid 개수는: ", len(mat_list), " =================================================")
    info_list = []


    # 2. API에서 데이터 불러오기
    for i in range(len(mat_list)):        # matchID iterate
        mat_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + mat_list[i] + "?api_key=" + api_key
        mat_info = requests.get(mat_url)

        timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + mat_list[i] + "/timeline?api_key=" + api_key
        mat_timeline = requests.get(timeline_url)

        if 'status' in mat_info.json() or 'status' in mat_timeline.json():
            if mat_info.json()['status']['message'] == 'Rate limit exceeded' or mat_timeline.json()['status']['message'] == 'Rate limit exceeded':
                print("리밋 걸림!!!! 2분 쉬어갑니다 ----------------------------------------")
                time.sleep(120)

                # 데이터 다시 불러오기
                mat_info = requests.get(mat_url)
                mat_timeline = requests.get(timeline_url)

            else:
                print("조회하는데 오류가 생겼습니다. 다음을 진행합니다.")
                continue

        total_json = {"mat_info": mat_info.json(),
                          "mat_timeline": mat_timeline.json()}

        print(i, "번째 데이터를 조회 후 합쳤습니다.")
        info_list.append(total_json)
    return info_list    # 한 티어에 대한 경기 정보를 모두 담은 list




def exe_collApiinfo():

    # 모든 티어의 matchID 불러와 저장
    total_match = coll_mat.find()

    # 도큐먼트 속 모든 keys값을 가져옴: 티어별 matchid
    key_names = []   # match 정보가 있는 key값 이름들
    tier_mat = []    # 각 티어의 정보를 담은 딕셔너리를 원소값으로 갖는 리스트

    for x in total_match:
        key_names.append(list(x.keys())[1])
        tier_mat.append(x)
    print("MongoDB mat_info DB에 있는 matchId 콜렉션 속 도큐먼트 key 값: ", key_names)



    for i in range(1):   # tier iterate   # len(tier_mat)
        lowCase_tier = str(key_names[1])[:-4]
        print("lowCase_tier: ", lowCase_tier)        # tier에 해당하는 소문자

        # api_info에 저장할 collection 이름
        sav_col = lowCase_tier + "_total"
        use_col = db_api.sav_col
        print("사용할 collection은 ",sav_col,"입니다.")
        use_col.drop()  # 콜렉션 비우기

        # 조회할 때 사용할 티어별 모든 matchID 리스트에 저장하기
        mat_list = tier_mat[1][str(key_names[1])]

        # api 전체 데이터 불러오기
        info_list = call_api(mat_list)

        print(lowCase_tier,"에서 모은 경기 정보의 개수는 ", len(info_list), "입니다.")

        # 각 collection에 insert 한꺼번에 하기
        use_col.insert_many(info_list)
        print(sav_col, "collection에 데이터를 저장했습니다 ")

total_match = coll_mat.find()

# 도큐먼트 속 모든 keys값을 가져옴: 티어별 matchid
# key_names = []
# tier_mat = []
# for x in total_match:
#     key_names.append(list(x.keys())[1])
#     tier_mat.append(x)

# print(tier_mat[0])
# print(len(tier_mat))
# for i in range(len(key_names)):
    # print(key_names[i])
    # print(total_match[i][str(key_names[i])])


exe_collApiinfo()

