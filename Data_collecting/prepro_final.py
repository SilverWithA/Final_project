import pandas as pd
import pprint
from pymongo import MongoClient

from db_functions import *


# 0. 설정
# product api 키 설정
api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"

# mongoDB 연결 설정
client = MongoClient('mongodb://localhost:27017/')
db_api = client.raw_info

coll_names = list(db_api.list_collection_names())
print("db_mat에 있는 모든 콜렉션: ",coll_names)



def table_maker(table_cnt):
    table_frames = []
    for i in range(table_cnt):
        df = pd.DataFrame(columns=["matchId","win", "gameMode", "summonerName","puuid",
                                   "summonerLevel", "gameDuration","teamPosition",
                                   "championName","championId","champLevel",
                                   "assists","kills", "deaths","defense","flex","offense",
                                   "prim1_perk", "prim2_perk", "prim3_perk", "prim4_perk","prim_style",
                                   "sub1_perk", "sub2_perk", "sub_style",
                                   "item0", "item1", "item2", "item3","item4","item5","item6",

                                   "totalDamToCham", "totalDamTaken",
                                   "totalMinionsKilled","totalEnemyJunKilled","totalAllyJunKilled",
                                   "detWardsPlaced","goldEarned",
                                   "timeCCingOthers",
                                   "summoner1Id","summoner2Id",
                                   "first_pur1","first_pur2","first_pur3","first_pur4",
                                   "first_pur5","first_pur6","first_pur7","first_pur8",

                                   "skill_slot","bans"])
        table_frames.append(df)
    return table_frames
Aram_table,Rank_loser,Rank_winner = table_maker(3)

def cal_first_pur(mat_timeline):
    first_pur = {}
    event = mat_timeline['info']['frames'][1]['events']

    for i in range(len(event)):
        if event[i]['type'] == "ITEM_PURCHASED":  # 이벤트 중 아이템 구매만 선별
            if str(event[i]['participantId']) not in first_pur:
                first_pur[str(event[i]['participantId'])] = [event[i]['itemId']]
            else:
                first_pur[str(event[i]['participantId'])].append(event[i]['itemId'])
    return first_pur   # 참가자 넘버와 해시 값임
def cal_skill_tree(mat_timeline):
    frames = mat_timeline['info']['frames']
    skill_tree = {}
    for i in range(len(frames)):
        if frames[i]['events']:
            for event_num in range(len(frames[i]['events'])):
                if frames[i]['events'][event_num]['type'] == "SKILL_LEVEL_UP":

                    if str(frames[i]['events'][event_num]['participantId']) not in skill_tree:
                        skill_tree[str(frames[i]['events'][event_num]['participantId'])] = [frames[i]['events'][event_num]['skillSlot']]
                    else:
                        skill_tree[str(frames[i]['events'][event_num]['participantId'])].append(frames[i]['events'][event_num]['skillSlot'])

    return skill_tree
def parti_skills(skill_tree, parti_num):

    skills = ''
    skill_cnt = [0, 0, 0]
    slot_list = skill_tree[str(parti_num+1)]
    # print("slot_list: ",slot_list)

    for num in range(len(slot_list)):

        if slot_list[num] == 1:
            skill_cnt[0] += 1
        elif slot_list[num] == 2:
            skill_cnt[1] += 1
        elif slot_list[num] == 4:
            pass
        else:
            skill_cnt[2] += 1

        # print(skill_cnt)

        for n in range(3):
            if skill_cnt[n] == 3:
                skill_cnt[n] = 0
                skills += str(n+1)

    return skills

def make_ban_list(mat_info):
    ban_list = []
    if mat_info["info"]['gameMode'] == "CLASSIC":  # 칼바람의 경우 팀밴이 없음
        if mat_info['info']['teams'][0]['bans']: # bans픽이 있으면
            for b in range(5):
                ban_list.append(mat_info['info']['teams'][0]['bans'][b]['championId'])
                ban_list.append(mat_info['info']['teams'][1]['bans'][b]['championId'])

            n1 = len(ban_list)
            print("중복 제거 전: ", ban_list)
            n2 = len(list(set(ban_list)))
            ban_list = list(set(ban_list))


            for _ in range(n1-n2):
                ban_list.append(None)
            print("중복 제거 후: ", list(set(ban_list)))
            return ban_list

        else:
            print("클래식 게임 모드에서 백픽을 선택하지 않았습니다.")

coll_raw = db_api.chall_total
# 1. mongoDB에서 matchId 정보가 있는 콜렉션 불러오기
def coll_usrlog(coll_raw,lowCase):
    cnt = 0
    columns_list = list(Rank_winner.columns)
    ban_list = []

    for raw_json in coll_raw.find():  # collection 중 하나의 도큐먼트 불러오기
        # print("------------------------------------------")
        cnt += 1
        # pprint.pprint(raw_json['mat_timeline'])       # 해시로 불러와짐

        # 2. 데이터 전처리 및 분류해서 리스트로 저장 -> 최종 테이블 형식의 df로 반환
        print(cnt,"번째 match정보를 가져왔습니다.")

        mat_info = raw_json['mat_info']
        mat_timeline = raw_json['mat_timeline']  # print(mat_info['info']['participants'][0])

        pur_list = cal_first_pur(mat_timeline)
        # print("pur_list: ",pur_list)

        skill_tree = cal_skill_tree(mat_timeline)
        # print("skill_tree: " , skill_tree)

        ban_list = make_ban_list(mat_info)
        print("ban_list: ",ban_list)



        for i in range(len(mat_info["metadata"]['participants'])):   # participants iterate
            print(cnt, "번째 matchID에서",i,"번째 참가자 정보를 수집합니다.")
            data_parti = mat_info['info']['participants']
            # print(data_parti)
            usrplay_info = [None] * len(columns_list)
            # print(data_parti[i])

            pass_columns = ["first_pur2","first_pur3","first_pur4","first_pur5","first_pur6","first_pur7","first_pur8",
                            "prim2_perk", "prim3_perk", "prim4_perk", "prim_style",
                            "sub1_perk", "sub2_perk", "sub_style"]
            try:
                parti_pur = pur_list[str(i+1)]
                for _ in range((8 - len(parti_pur))):
                    parti_pur.append(None)
            except:
                pass
                # pprint.pprint(raw_json['mat_timeline'])

            for idx in range(len(columns_list)):  # columns iterate
                try:
                    column = columns_list[idx]
                    # print("저장에 사용할 column은 ", column)
                    if str(column) == 'matchId':
                        usrplay_info[idx] = mat_info['metadata'][str(column)]

                    elif str(column) == 'gameDuration' or str(column) == 'gameMode':
                        usrplay_info[idx] = mat_info["info"][str(column)]

                    elif str(column) in ["defense", "flex", "offense"]:
                        usrplay_info[idx] = data_parti[i]['perks']["statPerks"][str(column)]


                    elif str(column) == 'prim1_perk':
                            usrplay_info[idx+0] = data_parti[i]['perks']['styles'][0]['selections'][0]['perk']
                            usrplay_info[idx+1] = data_parti[i]['perks']['styles'][0]['selections'][1]['perk'] # 'prim2_perk'
                            usrplay_info[idx+2] = data_parti[i]['perks']['styles'][0]['selections'][2]['perk'] # 'prim3_perk'
                            usrplay_info[idx+3] = data_parti[i]['perks']['styles'][0]['selections'][3]['perk'] #  prim4_perk
                            usrplay_info[idx+4] = data_parti[i]['perks']['styles'][0]['style']                 # prim_style
                            usrplay_info[idx+5] = data_parti[i]['perks']['styles'][0]['selections'][0]['perk'] # sub1_perk
                            usrplay_info[idx+6] = data_parti[i]['perks']['styles'][0]['selections'][1]['perk'] # sub2_perk
                            usrplay_info[idx+7] = data_parti[i]['perks']['styles'][1]['style']                 # sub_style



                    elif str(column) == 'totalDamToCham':
                        usrplay_info[idx] = data_parti[i]['totalDamageDealtToChampions']

                    elif str(column) == 'totalDamTaken':
                        usrplay_info[idx] = data_parti[i]['totalDamageTaken']


                    elif str(column) == 'totalMinionsKilled':
                        usrplay_info[idx] = data_parti[i]['totalMinionsKilled']

                    elif str(column) == 'totalEnemyJunKilled':
                        usrplay_info[idx] = data_parti[i]['totalEnemyJungleMinionsKilled']

                    elif str(column) == 'totalAllyJunKilled':
                        usrplay_info[idx] = data_parti[i]['totalAllyJungleMinionsKilled']
                    elif str(column) == 'detWardsPlaced':
                        usrplay_info[idx] = data_parti[i]['detectorWardsPlaced']

                    elif str(column) == "first_pur1":
                        for x in range(8):
                            usrplay_info[idx+x] = parti_pur[x]

                    elif str(column) in pass_columns:
                        continue

                    elif str(column) == 'skill_slot':
                        slots = parti_skills(skill_tree=skill_tree, parti_num=i)
                        # print(i,"번째 참가자의 skill_slots: ",slots)
                        usrplay_info[idx] = slots

                    elif str(column) == 'bans':
                        usrplay_info[idx] = ban_list[i]


                    else:
                        # print("각 참가자의", str(column),"에 대한 정보입니다.")
                        usrplay_info[idx] = data_parti[i][str(column)]



                except:  #  Exception as e
                    continue


            # 데이터 저장하기
            try:
                print(cnt,"번째 경기 정보를 저장합니다.")
                if mat_info["info"]['gameMode'] == 'ARAM':
                    n = len(Aram_table)
                    Aram_table.loc[n] = usrplay_info
                    print("Aram: ", len(Aram_table))

                elif data_parti[i]['win'] == True:
                    n = len(Rank_winner)
                    Rank_winner.loc[n] = usrplay_info
                    print("Rank_winner: ", len(Rank_winner))

                else:
                    n = len(Rank_loser)
                    Rank_loser.loc[n] = usrplay_info
                    print("Rank_loser: ", len(Rank_loser))

            except:
                pass

    Rank_winner.to_sql(name=str(lowCase+"win"), con=conn_gam, if_exists='append',index=False)
    Rank_loser.to_sql(name=str(lowCase+"lose"), con=conn_gam, if_exists='append', index=False)
    Aram_table.to_sql(name=str(lowCase+"aram"), con=conn_gam, if_exists='append', index=False)


coll_raw = db_api.chall_total
coll_usrlog(coll_raw, 'chall')

coll_raw = db_api.grand_total
coll_usrlog(coll_raw, 'grand')

coll_raw = db_api.mast_total
coll_usrlog(coll_raw, 'mast')

coll_raw = db_api.dia_total
coll_usrlog(coll_raw, 'dia')

coll_raw = db_api.em_total
coll_usrlog(coll_raw, 'em')

coll_raw = db_api.pla_total
coll_usrlog(coll_raw, 'pla')

coll_raw = db_api.gold_total
coll_usrlog(coll_raw, 'gold')

coll_raw = db_api.sil_total
coll_usrlog(coll_raw, 'sil')

coll_raw = db_api.bro_total
coll_usrlog(coll_raw, 'bro')

coll_raw = db_api.iron_total
coll_usrlog(coll_raw, 'iron')



