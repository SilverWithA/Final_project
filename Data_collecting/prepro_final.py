import pandas as pd
import pprint
from pymongo import MongoClient

from db_functions import *
from setting import *


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
def cal_first_pur(mat_timeline):
    """게임 유저의 첫 아이템 구매 항목을 수집하여 길이 8의 리스트로 반환
    아이템 8개를 사지 않았을 때 None값으로 채운다."""
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
    """한 게임에 대한 전체 유저의 skill_tree를 해시값으로 반환하는 함수"""
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
    """parti_num번째 유저의 mast_skills를 문자열로 반환하는 함수. 최대 3자, 1 or 2 or 3으로만 이루어짐"""

    mast_skills = ''
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
                mast_skills += str(n+1)

    return mast_skills

def make_ban_list(mat_info):
    """팀벤 정보를 리스트로 반환하는 함수이다"""
    ban_list = []
    if mat_info["info"]['gameMode'] == "CLASSIC":  # 칼바람의 경우 팀밴이 없음
        if len(mat_info['info']['teams'][0]['bans']) == 0:
            print("클래식 게임 모드에서 백픽을 선택하지 않았습니다.")

        else:

            for b in range(5):
                ban_list.append(mat_info['info']['teams'][0]['bans'][b]['championId'])
                ban_list.append(mat_info['info']['teams'][1]['bans'][b]['championId'])

            n1 = len(ban_list)
            # print("중복 제거 전: ", ban_list)
            n2 = len(list(set(ban_list)))
            ban_list = list(set(ban_list))

            for _ in range(n1-n2):
                ban_list.append(None)
                # print("중복 제거 후: ", ban_list)

            return ban_list



# make_ban_list 테스트하는 코드임 -------------------------------
# coll_raw = raw_coll['chall']
#
# for raw_json in coll_raw.find():
#     mat_info = raw_json['mat_info']
#     pprint.pprint(mat_info['info']['teams'])
#     print()
#     bansinfo = make_ban_list(mat_info)
#     pprint.pprint(bansinfo)
#     break
# # --------------------------------------------------------------









# mongoDB에서 matchId 정보가 있는 콜렉션 불러와서 - 전처리
def coll_usrlog(coll_raw,lowCase):
    Aram_table, Rank_loser, Rank_winner = table_maker(3)

    cnt = 0
    columns_list = list(Rank_winner.columns)
    ban_list = []

    for raw_json in coll_raw.find():  # collection 중 하나의 도큐먼트 불러오기
        # print("------------------------------------------")
        cnt += 1
        # pprint.pprint(raw_json['mat_timeline'])       # 해시로 불러와짐

        # 2. 데이터 전처리 및 분류해서 리스트로 저장 -> 최종 테이블 형식의 df로 반환


        mat_info = raw_json['mat_info']
        print(cnt, "번째 match정보를 가져왔습니다.", mat_info['metadata']['matchId'])
        mat_timeline = raw_json['mat_timeline']  # print(mat_info['info']['participants'][0])
        if mat_timeline['info']['frames'][0]['events'][0]['type'] == "GAME_END":
            print("조기종료 된 게임입니다.")
            continue

        pur_list = cal_first_pur(mat_timeline)
        # print("pur_list: ",pur_list)

        skill_tree = cal_skill_tree(mat_timeline)
        # print("skill_tree: " , skill_tree)

        bans_list = make_ban_list(mat_info)
        # print("ban_list: ",bans_list)



        for i in range(len(mat_info["metadata"]['participants'])):   # participants iterate
            # print(cnt, "번째 matchID에서",i,"번째 참가자 정보를 수집합니다.")
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
                        try:
                            usrplay_info[idx] = bans_list.pop()
                        except:
                            continue


                    else:
                        # print("각 참가자의", str(column),"에 대한 정보입니다.")
                        usrplay_info[idx] = data_parti[i][str(column)]



                except:  #  Exception as e
                    continue


            # 데이터 저장하기
            try:
                # print(cnt,"번째 경기 정보를 저장합니다.")
                if mat_info["info"]['gameMode'] == 'ARAM':
                    n = len(Aram_table)
                    Aram_table.loc[n] = usrplay_info


                elif data_parti[i]['win'] == True:
                    n = len(Rank_winner)
                    Rank_winner.loc[n] = usrplay_info


                else:
                    n = len(Rank_loser)
                    Rank_loser.loc[n] = usrplay_info


            except:
                pass

    print(lowCase,"의 최종 테이블 컬럼 개수는 다음과 같음 =============")
    print("Aram: ", len(Aram_table))
    print("Rank_winner: ", len(Rank_winner))
    print("Rank_loser: ", len(Rank_loser))

    Rank_winner.to_sql(name=str(lowCase+"_win"), con=conn_gam, if_exists='replace',index=False)
    Rank_loser.to_sql(name=str(lowCase+"_lose"), con=conn_gam, if_exists='replace', index=False)
    Aram_table.to_sql(name=str(lowCase+"_aram"), con=conn_gam, if_exists='replace', index=False)
    print(lowCase,"데이터를 전처리하여 모두 저장하였습니다 =============")

def exe_prepro_final():

    # gameinfo 에 있는 모든 table 데이터 초기화
    trun_tables(engine_gam)

    # raw_coll와 lowCase는 setting.py에서 설정
    for i in range(len(raw_coll)):  # raw_info의 collections iterate  # len(raw_coll)

        print("전처리 할 티어는 ", lowCase[i], "입니다.===========================================")
        # coll_raw = 사용할 collection 지정/ # lowCase = 수집할 티어의 소문자
        coll_usrlog(coll_raw=raw_coll[str(lowCase[i])], lowCase=lowCase[i])


exe_prepro_final()





