import pandas as pd
import time
import requests

# from pymongo import MongoClient
# from sqlalchemy import create_engine
# from sqlalchemy import text
# from db_functions import *


# json 파일 불러오기
# client = MongoClient('mongodb://localhost:27017/')
# use_db = client.api_info
# use_collect = use_db.match_info
api_key= "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"
# 2. 최종 테이블 스키마 정의
def table_maker(table_cnt):
    talbe_frames = []
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
                                   "bans","timeCCingOthers",
                                   "summoner1Id","summoner2Id",
                                   "first_pur1","first_pur2","first_pur3","first_pur4",
                                   "first_pur5","first_pur6","first_pur7","first_pur8",

                                   "slot_log","skill_tree"
                                   ])
        talbe_frames.append(df)
    return talbe_frames

Aram_table,Rank_loser,Rank_winner = table_maker(3)


match_table = pd.read_csv("matchID_mast.csv")
print(match_table.head())


# # 5. 각 티어별 match_table에서 matchId불러와서  API 불러오기
def coll_gameinfo(match_table):
    """matchID를 넣으면 최종 game_info를 APi를 통해 조회하고 DB에 저장하는 함수"""
    # API에서 조회한 데이터를 분류하여 알맞은 컬럼 위치에 넣어주는 작업
    columns_list = list(Rank_winner.columns)

    print("총 조회할 matchID의 개수: ", len(match_table))

    for i in range(1):  # len(match_table)
        match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + match_table['MatchId'][i] + "?api_key=" + api_key
        r = requests.get(match_url)
        print(i, "번째 match정보를 불러왔습니다.", match_table['MatchId'][i])
        print(r.json())


        # 리밋 걸리면 2분 쉬어가기 -------------------------------------
        if 'status' in r.json():
            print(r.json())
            if r.json()['status']['message'] == 'Rate limit exceeded':
                print("2분 쉬어갑니다.")
                time.sleep(120)

                # 데이터 다시 조회하기
                r = requests.get(match_url)
                print(i, "번째 데이터를 다시 가져오고 있습니다.: ", match_table['MatchId'][i])

                # 리밋타이밍에 쉬어갔던 데이터가 조회 불가능한 matchID 일때 필터링
                if 'status' in r.json():
                    continue

            elif r.json()['status']['message'] == 'Forbidden':
                print("api키를 다시 확인해주세요. api키가 막힌 것 같음!!!!!")
                break

            else:
                continue

        data_parti = r.json()['info']['participants']

        # columns_list에 들어있는 정보 순서대로 불러와 저장하기
        for i in range(len(r.json()["metadata"]['participants'])):
            # print(i,"번째 참가자에 대한 정보---------------------- ")

            # 불러온 정보를 저장해 df에 저장하기 전에 잠깐 담아줄 빈 list 생성
            usrplay_info = [None] * len(columns_list)

            # 해당 게임에 참가한 참가자 수에 따라 정보 모아서 컬럼 순서(idx)대로 리스트에 쌓기
            for idx in range(len(columns_list)):
                try:
                    column = columns_list[idx]

                    if str(column) == 'matchId':
                        data = r.json()['metadata'][columns_list[idx]]

                    elif str(column) == 'gameDuration' or str(column) == 'gameMode':
                        data = r.json()["info"][str(column)]

                    elif str(column) in ["defense", "flex", "offense"]:
                        data = data_parti[i]['perks']["statPerks"][str(column)]



                    elif str(column) =='prim1_perk':
                        usrplay_info[idx] = data_parti[i]['perks']['styles'][0]['selections'][0]['perk']

                    elif str(column) =='prim2_perk':
                        usrplay_info[idx] = data_parti[i]['perks']['styles'][0]['selections'][1]['perk']

                    elif str(column) =='prim3_perk':
                        usrplay_info[idx] = data_parti[i]['perks']['styles'][0]['selections'][2]['perk']

                    elif str(column) =='prim4_perk':
                        usrplay_info[idx] = data_parti[i]['perks']['styles'][0]['selections'][3]['perk']

                    elif str(column) == 'prim_style':
                        usrplay_info[idx] = data_parti[i]['perks']['styles'][0]['style']

                    elif str(column) == 'sub_style':
                        usrplay_info[idx] = data_parti[i]['perks']['styles'][1]['style']

                    elif str(column) == 'sub1_perk':
                        usrplay_info[idx] = data_parti[i]['perks']['styles'][0]['selections'][0]['perk']

                    elif str(column) == 'sub2_perk':
                        usrplay_info[idx] = data_parti[i]['perks']['styles'][0]['selections'][1]['perk']

                    elif str(column) == 'bans':
                        usrplay_info[idx] = r.json()['info']['teams'][0]['bans'][i]['championId']


                    else:
                        data = data_parti[i][str(column)]

                except:
                    continue




            try:
                if r.json()['info']['gameMode'] == 'ARAM':
                    n = len(Aram_table)
                    Aram_table.loc[n] = usrplay_info
                # print(Aram_table)

                elif data_parti[i]['win'] == True:
                    n = len(Rank_winner)
                    Rank_winner.loc[n] = usrplay_info
                    # print(Rank_winner)

                else:
                    n = len(Rank_loser)
                    Rank_loser.loc[n] = usrplay_info
                    # print(Rank_loser)
            except:
                pass

    print("Aram_table", Aram_table)
    print()
    print("Rank_winner", Rank_winner)
    print()
    print("Rank_loser", Rank_loser)

    # Aram_table.to_csv("Aram_table.csv")
    # Rank_winner.to_csv("Rank_winner.csv")
    # Rank_loser.to_csv("Rank_loser.csv")


coll_gameinfo(match_table)