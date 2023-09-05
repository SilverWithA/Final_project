import requests
import pandas as pd
import time
import json

# (1) ERD에 따라 테이블 만들기: table_maker
def table_maker(table_cnt):
    talbe_frames = []
    for i in range(table_cnt):
        df = pd.DataFrame(columns=["matchId","puuid", "summonerName", "summonerLevel","win",
                                           "gameMode", "gameDuration","teamPosition",
                                           "championName","championId","champLevel",
                                           "assists","firstBloodAssist", "firstBloodKill","firstTowerAssist","firstTowerKill",
                                           "kills", "pentaKills", "quadraKills", "tripleKills",
                                           "item0", "item1", "item2", "item3","item4","item5","item6",
                                           "defense","flex","offense",
                                           "prim1_perk", "prim1_var1","prim1_var2","prim1_var3",
                                           "prim2_perk", "prim2_var1","prim2_var2","prim2_var3",
                                           "prim3_perk", "prim3_var1","prim3_var2","prim3_var3",
                                           "prim4_perk", "prim4_var1","prim4_var2","prim4_var3","prim_style",
                                           "sub1_perk", "sub1_var1","sub1_var2","sub1_var3",
                                           "sub2_perk", "sub2_var1","sub2_var2","sub2_var3","sub_style",
                                           "summoner1Id","summoner2Id",
                                           "totalDamageDealtToChampions", "totalDamageTaken",
                                           "totalMinionsKilled", "totalEnemyJungleMinionsKilled",
                                           "visionScore", "visionWardsBoughtInGame","wardsKilled", "wardsPlaced"])
        talbe_frames.append(df)
    return talbe_frames
Aram_table,Rank_loser,Rank_winner = table_maker(3)



# (2) MatchID 불러오기 -------------------------------------------------------
matchID_chall = pd.read_csv("matchID_em1.csv", encoding="utf-8-sig")
match_list = list(matchID_chall['MatchId'])

matchID_grand = pd.read_csv("matchID_em2.csv", encoding="utf-8-sig")
match_list += list(matchID_grand['MatchId'])

matchID_mast = pd.read_csv("matchID_em3.csv", encoding="utf-8-sig")
match_list += list(matchID_mast['MatchId'])

matchID_mast = pd.read_csv("matchID_em4.csv", encoding="utf-8-sig")
match_list += list(matchID_mast['MatchId'])

print("전체 matchID의 개수: ", len(match_list))
match_list = set(match_list)
match_list = list(match_list)
print("전체 matchID의 개수: ", len(match_list))







api_key = "RGAPI-96d4602c-940f-4bd3-b2dd-f6f6f7726996"
columns_list= list(Aram_table.columns)

# 각 matchID 따른 게임 정보 불러오기
for i in range(5000):
    match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + match_list[i] + "?api_key=" + api_key
    r = requests.get(match_url)
    print(i,"번째 match정보를 불러왔습니다.", match_list[i])
    # print(matchID_chall['MatchId'][i],"에 대한 전체 정보: ", r.json())

    if 'status' in r.json():
        # 리밋걸리면 2분 쉬어가기 -----------------------------------
        if r.json()['status']['message'] == 'Rate limit exceeded':

            print("2분 쉬어갑니다.")
            time.sleep(120)
            r = requests.get(match_url)
            print(i, "번째 데이터를 다시 가져오고 있습니다.: ", match_list[i])

        else:
            continue

    data_parti = r.json()['info']['participants']
    pass_columns = ["prim1_var1","prim1_var2","prim1_var3",
                 "prim2_perk", "prim2_var1","prim2_var2","prim2_var3",
                 "prim3_perk", "prim3_var1","prim3_var2","prim3_var3",
                 "prim4_perk", "prim4_var1","prim4_var2","prim4_var3","prim_style",
                 "sub1_perk", "sub1_var1","sub1_var2","sub1_var3",
                 "sub2_perk", "sub2_var1","sub2_var2","sub2_var3","sub_style"]



    # columns_list에 들어있는 정보 순서대로 불러와 저장하기
    for i in range(len(r.json()["metadata"]['participants'])):
        # print(i,"번째 참가자에 대한 전체 정보: ", data_parti[i])
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

                elif str(column) in  ["defense","flex","offense"]:
                    data = data_parti[i]['perks']["statPerks"][str(column)]

                elif str(column) == 'prim1_perk':
                    # primstlye
                    for j in range(4):
                        prim_perk = data_parti[i]['perks']['styles'][0]['selections'][j]['perk']
                        prim_var1 = data_parti[i]['perks']['styles'][0]['selections'][j]['var1']
                        prim_var2 = data_parti[i]['perks']['styles'][0]['selections'][j]['var2']
                        prim_var3 = data_parti[i]['perks']['styles'][0]['selections'][j]['var3']
                        prim_st = data_parti[i]['perks']['styles'][0]['style']

                        usrplay_info[idx+(4*j)+0] = prim_perk
                        usrplay_info[idx+(4*j)+1] = prim_var1
                        usrplay_info[idx+(4*j)+2] = prim_var2
                        usrplay_info[idx+(4*j)+3] = prim_var3

                        usrplay_info[idx+16] = prim_st



                    # substlye
                    for j in range(2):
                        sub_perk = data_parti[i]['perks']['styles'][1]['selections'][j]['perk']
                        sub_var1 = data_parti[i]['perks']['styles'][1]['selections'][j]['var1']
                        sub_var2 = data_parti[i]['perks']['styles'][1]['selections'][j]['var2']
                        sub_var3 = data_parti[i]['perks']['styles'][1]['selections'][j]['var3']
                        sub_st = data_parti[i]['perks']['styles'][1]['style']

                        usrplay_info[idx + (4*j)+17] = sub_perk
                        usrplay_info[idx + (4*j)+18] = sub_var1
                        usrplay_info[idx + (4*j)+19] = sub_var2
                        usrplay_info[idx + (4*j)+20] = sub_var3
                        usrplay_info[idx + 25] = sub_st

                elif str(column) in pass_columns:
                    continue

                else:
                    data = data_parti[i][str(column)]


                if idx != 30:
                    usrplay_info[idx] = data

            except:
                continue

        # print("쌓은 참가자의 정보: ", usrplay_info)
        # print("쌓아야할 컬럼의 길이: ", len(usrplay_info))
        # print("쌓인 정보의 길이: ", len(columns_list))

    # usrplay_info를 알맞는 table에 쌓아주기
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




Rank_winner.to_csv("Rank_winner_em1.csv", index=False, encoding="utf-8-sig")
Rank_loser.to_csv("Rank_loser_em1.csv", index=False, encoding="utf-8-sig")
Aram_table.to_csv("Aram_table_em1.csv", index=False, encoding="utf-8-sig")
print(" 16400개의 정보 중 5000개의 정보를 저장했습니다.")




