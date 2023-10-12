import pandas as pd
import pprint
from pymongo import MongoClient

from db_functions import *
from setting import *
from final_cal_function import *

# gameinfo DB의 데이터를 전처리하기 위한 함수
def table_maker(table_cnt):
    table_frames = []
    for i in range(table_cnt):
        df = pd.DataFrame(columns=["matchId","win", "gameMode", "summonerName","puuid","teamPosition",
                                   "championName","championId","assists","kills", "deaths",
                                   "defense","flex","offense",
                                   "prim1_perk", "prim2_perk", "prim3_perk", "prim4_perk","prim_style",
                                   "sub1_perk", "sub2_perk", "sub_style",
                                   "summoner1Id","summoner2Id",
                                   "first_pur1","first_pur2","first_pur3","first_pur4",
                                   "first_pur5","first_pur6","first_pur7","first_pur8",
                                   "skill_slot","bans",
                                   "core1","core2","core3","core4","core5","core6","shoes"])
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
                        skill_tree[str(frames[i]['events'][event_num]['participantId'])] = [str(frames[i]['events'][event_num]['skillSlot'])]
                    else:
                        skill_tree[str(frames[i]['events'][event_num]['participantId'])].append(str(frames[i]['events'][event_num]['skillSlot']))

    return skill_tree
def parti_skills(skill_tree, parti_num):
    """parti_num번째 유저의 mast_skills를 문자열로 반환하는 함수. 최대 3자, 1 or 2 or 3으로만 이루어짐"""

    mast_skills = ''
    skill_cnt = [0, 0, 0]
    slot_list = skill_tree[str(parti_num+1)]
    # print("cal_skill_tree에서 받아온 전체 slot_list: ",slot_list)

    for i in range(len(slot_list)):

        for n in range(len(skill_cnt)):
            if skill_cnt[n] == 3 and str(n+1) not in mast_skills:
                # print("초기화 하기 전 skill_cnt: ",skill_cnt)
                skill_cnt[n] = 0          # count 값 초기화
                # print(n,"번째 스킬을 skill_cnt에서 초기화합니다.",skill_cnt)
                mast_skills += (str(n+1))  # 마스터 스킬에 추가
                # print("mast_skills에 스킬이 추가되었습니다.",mast_skills)

        if len(mast_skills) == 3:
            break

        if slot_list[i] == '1':
            skill_cnt[0] += 1
        elif slot_list[i] == '2':
            skill_cnt[1] += 1
        elif slot_list[i] == '4':
            pass
        elif slot_list[i] == '3':
            skill_cnt[2] += 1
        # print("slot_list를 돌며 스킬 카운트를 계산하였습니다: ",skill_cnt)


    # print("mast_skills: ", mast_skills)
    return mast_skills
#
# cnt =0
# for raw_json in raw_coll['chall'].find():  # collection 중 하나의 도큐먼트 불러오기
#     cnt += 1
#     # 2. 데이터 전처리 및 분류해서 리스트로 저장 -> 최종 테이블 형식의 df로 반환
#     mat_info = raw_json['mat_info']
#     print(cnt, "번째 match정보를 가져왔습니다.", mat_info['metadata']['matchId'])
#
#     mat_timeline = raw_json['mat_timeline']  # print(mat_info['info']['participants'][0])
#     # print(cal_skill_tree(mat_timeline))
#
#     skill_tree = cal_skill_tree(mat_timeline)
#     print("skill_tree: ", skill_tree)
#     parti_skills(skill_tree,1)
#     break

def make_ban_list(mat_info):
    """팀벤 정보를 리스트로 반환하는 함수이다"""
    ban_list = []
    if mat_info["info"]['gameMode'] == "CLASSIC":  # 칼바람의 경우 팀밴이 없음
        if len(mat_info['info']['teams'][0]['bans']) == 0:
            # print("클래식 게임 모드에서 백픽을 선택하지 않았습니다.")
            pass


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
def search_core_item(core_list,mat_timeline):
    frames = mat_timeline['info']['frames']

    build_core = {}
    for i in range(len(frames)):  # events iterate
        if frames[i]['events']:  # events가 존재하면
            for event_num in range(len(frames[i]['events'])):  # events의 내부 iterate

                each_event = frames[i]['events'][event_num]

                # build_core에 참가자ID가 없으면 키값 생성해서 []로 값 저장
                if each_event['type'] == "ITEM_PURCHASED" and each_event['itemId'] in core_list:

                    if str(each_event['participantId']) not in build_core:
                        build_core[str(each_event['participantId'])] = [each_event['itemId']]

                    else:
                        build_core[str(each_event['participantId'])].append(each_event['itemId'])


    return build_core




