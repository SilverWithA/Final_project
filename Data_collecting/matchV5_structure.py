import requests
import pandas as pd

from pymongo import MongoClient
import pprint
from db_functions import *

# product키
api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"

# DB 연결 설정
# client = MongoClient('mongodb://localhost:27017/')
# db_mat = client.mat_info
# print("db_mat에 있는 모든 콜렉션: ",db_mat.list_collection_names())
#
# coll_mat = db_mat.matchIds
#
#pro
# mat_hash = {}
# for doc in coll_mat.find():
#     # print(cnt,"번째 콜렉션은")
#     # pprint.pprint(doc)   # 해시로 불러와짐
#     mat_hash[str(list(doc.keys())[1])] = doc.values()    # lowCase_mat
#


# tier_mat = list(mat_hash.keys())

mat_cnt = pd.read_csv("matchID_chall.csv")
# print(mat_cnt)
# print(tier_mat)
ban_list = []
# for coll_name in tier_mat:  # for coll_name in tier_mat
#     mat_cnt = list(mat_hash[str(coll_name)])[1]
for _ in range(1):
    for i in range(len(mat_cnt)):  # len(mat_cnt)
        # print(mat_cnt[i])


        match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + mat_cnt['MatchId'][i] + "?api_key=" + api_key  # mat_cnt[i]
        r = requests.get(match_url)

        print(i,"번째 match정보입니다. --------------------------------------------------------------")
        # print(coll_name,"에서 가져온", i,"번째 정보: ", mat_cnt[i])
        print("meta--------------------------------------")
        print("MatchId: ", r.json()['metadata']['matchId'])
        print("경기 모드: ", r.json()['info']['gameMode'])


        # 팀 bans에 대한 정보
        if r.json()['info']['gameMode'] == "CLASSIC":  # 칼바람의 경우 팀밴이 없음
            if r.json()['info']['teams'][0]['bans']:
                for b in range(5):
                    ban_list.append(r.json()['info']['teams'][0]['bans'][b]['championId'])
                    ban_list.append(r.json()['info']['teams'][1]['bans'][b]['championId'])
                print("중복 제거 전: ", ban_list)
                print("중복 제거 후: ", list(set(ban_list)))
            else:
                print("클래식 게임 모드에서 백픽을 선택하지 않았습니다?")


        for j in range(1):  # parti_num = 10
            print(j,"번째 참가자의 승패여부(T/F) win: ", r.json()['info']['participants'][j]['win'])
            print(j,"번째 참가자의 summonerName: ", r.json()['info']['participants'][j]['summonerName'])
            print(j,"번째 참가자의 puuid: ", r.json()['info']['participants'][j]['puuid'])
            print(j,"번째 참가자의 summonerLevel: ", r.json()['info']['participants'][j]['summonerLevel'])
            print(j,"경기 진행 시간 gameDuration: ", r.json()['info']['gameDuration'])
            print(j,"번째 참가자의 teamPosition: ", r.json()['info']['participants'][j]['teamPosition'])
            print(j,"번째 참가자의 championName: ", r.json()['info']['participants'][j]['championName'])
            print(j,"번째 참가자의 championId: ", r.json()['info']['participants'][j]['championId'])
            print(j,"번째 참가자의 champLevel: ", r.json()['info']['participants'][j]['champLevel'])

            print(j,"번째 참가자의 assists: ", r.json()['info']['participants'][j]['assists'])
            print(j,"번째 참가자의 kill: ", r.json()['info']['participants'][j]['kills'])
            print(j,"번째 참가자의 deaths: ", r.json()['info']['participants'][j]['deaths'])

            print(j,"번째 참가자의 룬특성(defense): ", r.json()['info']['participants'][j]['perks']["statPerks"]["defense"])
            print(j,"번째 참가자의 룬특성(flex): ", r.json()['info']['participants'][j]['perks']["statPerks"]["flex"])
            print(j,"번째 참가자의 룬특성(offense): ", r.json()['info']['participants'][j]['perks']["statPerks"]["offense"])



            print(j,"번째 참가자의 prim1_perk : ", r.json()['info']['participants'][j]['perks']['styles'][0]['selections'][0]['perk'])
            print(j,"번째 참가자의 prim2_perk : ",r.json()['info']['participants'][j]['perks']['styles'][0]['selections'][1]['perk'])
            print(j,"번째 참가자의 prim3_perk : ",r.json()['info']['participants'][j]['perks']['styles'][0]['selections'][2]['perk'])
            print(j,"번째 참가자의 prim4_perk : ",r.json()['info']['participants'][j]['perks']['styles'][0]['selections'][3]['perk'])
            print(j,"번째 참가자의 prim_style: ", r.json()['info']['participants'][j]['perks']['styles'][0]['style'])


            print(j,"번째 참가자의 sub1_perk: ",r.json()['info']['participants'][j]['perks']['styles'][1]['selections'][0]['perk'])
            print(j,"번째 참가자의 sub12_perk: ",r.json()['info']['participants'][j]['perks']['styles'][1]['selections'][1]['perk'])
            print(j,"번째 참가자의 sub_style: ", r.json()['info']['participants'][j]['perks']['styles'][1]['style'])


            print(j,"번째 참가자의 item0: ", r.json()['info']['participants'][j]['item0'])
            print(j,"번째 참가자의 item1: ", r.json()['info']['participants'][j]['item1'])
            print(j,"번째 참가자의 item2: ", r.json()['info']['participants'][j]['item2'])
            print(j,"번째 참가자의 item3: ", r.json()['info']['participants'][j]['item3'])
            print(j,"번째 참가자의 item4: ", r.json()['info']['participants'][j]['item4'])
            print(j,"번째 참가자의 item5: ", r.json()['info']['participants'][j]['item5'])
            print(j,"번째 참가자의 item6: ", r.json()['info']['participants'][j]['item6'])


            print(j,"번째 참가자의 totalDamageDealtToChampions: ", r.json()['info']['participants'][j]['totalDamageDealtToChampions'])
            print(j,"번째 참가자의 totalDamageTaken: ", r.json()['info']['participants'][j]['totalDamageTaken'])

            # CS --------------------------------------------------
            print("CS 지표 관련 데이터 ------------------- ")
            print(j,"번째 참가자의 totalMinionsKilled: ", r.json()['info']['participants'][j]['totalMinionsKilled'])
            print(j,"번째 참가자의 totalEnemyJungleMinionsKilled: ", r.json()['info']['participants'][j]['totalEnemyJungleMinionsKilled'])
            print(j,"번째 참가자의 totalAllyJungleMinionsKilled: ", r.json()['info']['participants'][j]['totalAllyJungleMinionsKilled'])



            print(j,"번째 참가자의  detectorWardsPlaced: ", r.json()['info']['participants'][j]['detectorWardsPlaced'])
            print(j,"번째 참가자의 goldEarned: ", r.json()['info']['participants'][j]['goldEarned'])
            print(j,"번째 참가자의 timeCCingOthers: ", r.json()['info']['participants'][j]['timeCCingOthers'])


            print(j,"소환사 주문 D: ", r.json()['info']['participants'][j]['summoner1Id'])
            print(j,"소환사 주문 F: ", r.json()['info']['participants'][j]['summoner2Id'])



            # # matchID - timeline API -------------------------------------------------------
            timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + mat_cnt['MatchId'][i]+ "/timeline?api_key=" + api_key
            s = requests.get(timeline_url)

            event = s.json()['info']['frames'][1]['events']  # 두번째 event가 아이템 구매에 대한 정보가 있음
            first_pur = {}  # 해시로 저장
            for i in range(len(event)):
                if event[i]['type'] == "ITEM_PURCHASED":  # 이벤트 중 아이템 구매만 선별
                    if str(event[i]['participantId']) not in first_pur:
                        first_pur[str(event[i]['participantId'])] = [event[i]['itemId']]
                    else:
                        first_pur[str(event[i]['participantId'])].append(event[i]['itemId'])
            # print("first_pur: ", first_pur)

            parti_pur = first_pur[str(j+1)]
            for _ in range((8 - len(parti_pur))):
                parti_pur.append(None)
            print(parti_pur)


            # type = SKILL_LEVEL_UP 일때
            frames = s.json()['info']['frames']
            skill_tree = {}
            for i in range(len(frames)):
                if frames[i]['events']:
                    for event_num in range(len(frames[i]['events'])):
                        if frames[i]['events'][event_num]['type'] == "SKILL_LEVEL_UP":

                            if str(frames[i]['events'][event_num]['participantId']) not in skill_tree:
                                skill_tree[str(frames[i]['events'][event_num]['participantId'])] = [frames[i]['events'][event_num]['skillSlot']]
                            else:
                                skill_tree[str(frames[i]['events'][event_num]['participantId'])].append(frames[i]['events'][event_num]['skillSlot'])

            # print("skill_tree: ",skill_tree)

            skills = []
            skill_cnt= [0,0,0]
            for i in range(len(skill_tree[str(j+1)])):

                if skill_tree[str(j+1)][i] == 1:
                    skill_cnt[0] += 1
                elif skill_tree[str(j+1)][i] == 2:
                    skill_cnt[1] += 1
                elif skill_tree[str(j+1)][i] == 4:
                    pass
                else:
                    skill_cnt[2] += 1
                for i in range(3):
                    if skill_cnt[i] == 3:
                        skill_cnt[i] = 0
                        skills.append(i + 1)

            print(skills)
        break
    break











