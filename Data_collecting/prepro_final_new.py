import pandas as pd
import pprint
from pymongo import MongoClient

from db_functions import *
from setting import *
from final_cal_function import *

# <raw_info에서 json을 받아서 정제된 dataframe으로 만들어서 MySQL에 넘기는 코드>


# mongoDB에서 matchId 정보가 있는 콜렉션 불러와서 - 전처리
def coll_usrlog(coll_raw,lowCase):
    Aram_table, Rank_loser, Rank_winner = table_maker(3)

    cnt = 0
    columns_list = list(Rank_winner.columns)
    # print("columns_list: ",columns_list)

    for raw_json in coll_raw.find():  # collection 중 하나의 도큐먼트 불러오기
        # print("------------------------------------------")
        cnt += 1
        # pprint.pprint(raw_json['mat_timeline'])       # 해시로 불러와짐
        pass_columns = ["first_pur2", "first_pur3", "first_pur4", "first_pur5", "first_pur6", "first_pur7",
                        "first_pur8",
                        "prim2_perk", "prim3_perk", "prim4_perk", "prim_style",
                        "sub1_perk", "sub2_perk", "sub_style",
                        "core2", "core3", "core4", "core5", "core6", "shoes"]


        # 2. 데이터 전처리 및 분류해서 리스트로 저장 -> 최종 테이블 형식의 df로 반환
        mat_info = raw_json['mat_info']
        print(cnt, "번째 match정보를 가져왔습니다.", mat_info['metadata']['matchId'])
        mat_timeline = raw_json['mat_timeline']  # print(mat_info['info']['participants'][0])
        if mat_timeline['info']['frames'][0]['events'][0]['type'] == "GAME_END":
            print(mat_info['metadata']['matchId'],"는 조기종료 된 게임입니다.")
            continue

        pur_list = cal_first_pur(mat_timeline)
        # print("pur_list: ",pur_list)

        skill_tree = cal_skill_tree(mat_timeline)
        # print("skill_tree: " , skill_tree)

        bans_list = make_ban_list(mat_info)
        # print("ban_list: ",bans_list)

        build_core = search_core_item(core_list, mat_timeline)
        # print("build_core: ",build_core)





        for i in range(len(mat_info["metadata"]['participants'])):   # participants iterate
            # print(cnt, "번째 matchID에서",i,"번째 참가자 정보를 수집합니다.----------------------------------------")
            data_parti = mat_info['info']['participants']
            # print(data_parti)
            usrplay_info = [None] * len(columns_list)
            # print(data_parti[i])
            
            # item컬럼들 안에 shoes에 해당하는 코드가 있는지 확인하기 위해 item_list 저장
            item_list = [data_parti[i]["item0"],data_parti[i]["item1"],data_parti[i]["item2"],data_parti[i]["item3"],data_parti[i]["item4"],data_parti[i]["item5"],data_parti[i]["item6"]]

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

                    elif str(column) in pass_columns:
                        continue

                    elif str(column) == 'gameMode':
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

                    elif str(column) == "first_pur1":
                        for x in range(8):
                            usrplay_info[idx+x] = parti_pur[x]

                    elif str(column) == 'skill_slot':
                        slots = parti_skills(skill_tree=skill_tree, parti_num=i)
                        # print("mast skill 계산 전: ",skill_tree[str(i+1)])
                        # print(i,"번째 참가자의 skill_slots: ",slots)
                        if slots == '':
                            continue
                        usrplay_info[idx] = slots

                    elif str(column) == 'bans':
                        try:
                            usrplay_info[idx] = bans_list.pop()

                        except:
                            continue

                    elif str(column) == 'core1':

                        # 코어가 6개 이하면 None으로 채워 길이를 6개로 맞춤
                        if len(build_core[str(i+1)]) < 6:
                            for x in range(6 - len(build_core[str(i+1)])):
                                build_core[str(i + 1)].append(None)

                        # i = participants number
                        for core_num in range(6): # core iterate
                            usrplay_info[idx + core_num] = build_core[str(i+1)][0+core_num]



                    else:
                        # print("각 참가자의", str(column),"에 대한 정보입니다.")
                        usrplay_info[idx] = data_parti[i][str(column)]



                except Exception as e:  #  Exception as e
                    # print("컬럼 저장 과정에서 문제 발생: ",e)
                    continue


            # item0~ item6까지에 코드 중 shoew_list에 있는 코드가 있다면 shoes 컬럼에 넣기
            # print("items:", usrplay_info[25:32])


            for item in item_list:            # item iterate
                if item in shoes_list:        # 어떤 item 이 신발 코드라면
                    usrplay_info[-1] = item

            # print("usrplay_info: ",usrplay_info)




            # 데이터 저장하기
            try:
                # print(cnt,"번째 경기 정보를 저장합니다.")
                if mat_info["info"]['gameMode'] == 'ARAM':
                    n = len(Aram_table)
                    Aram_table.loc[n] = usrplay_info


                elif data_parti[i]['win'] == 1:
                    n = len(Rank_winner)
                    Rank_winner.loc[n] = usrplay_info


                else:
                    n = len(Rank_loser)
                    Rank_loser.loc[n] = usrplay_info


            except Exception as e:
                print("불러온 usrinfo를 df 저장 실패", e)
                pass

    print(lowCase,"의 최종 테이블 컬럼 개수는 다음과 같음 =======================================")
    print("Aram: ", len(Aram_table))
    print("Rank_winner: ", len(Rank_winner))
    print("Rank_loser: ", len(Rank_loser))

    Rank_winner.to_sql(name=str(lowCase+"_win"), con=conn_gam, if_exists='append',index=False)
    Rank_loser.to_sql(name=str(lowCase+"_lose"), con=conn_gam, if_exists='append', index=False)
    Aram_table.to_sql(name=str(lowCase+"_aram"), con=conn_gam, if_exists='append', index=False)
    print(lowCase,"데이터를 전처리하여 모두 저장하였습니다 =======================================")

def exe_prepro_final():
    # gameinfo 에 있는 모든 table 데이터 초기화
    trun_tables(engine_gam)

    # 임시로 스키마 하나를 불러오기
    # fin_schema = select_db(table_name='chall_win', conn_name=conn_gam)

    # raw_coll와 lowCase는 setting.py에서 설정
    for i in range(len(raw_coll)):  # raw_info의 collections iterate  # len(raw_coll)

        print("전처리 할 티어는 ", lowCase[i], "입니다.===========================================")
        # coll_raw = 사용할 collection 지정 / # lowCase = 수집할 티어의 소문자
        coll_usrlog(coll_raw=raw_coll[str(lowCase[i])], lowCase=lowCase[i])
        # coll_usrlog(coll_raw=raw_coll[str(lowCase[i])], lowCase=lowCase[i],schema = fin_schema)


exe_prepro_final()