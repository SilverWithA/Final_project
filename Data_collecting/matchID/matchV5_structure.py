import requests
import pandas as pd
#
#
#
# api_key = "RGAPI-96d4602c-940f-4bd3-b2dd-f6f6f7726996"
# matchID_chall = pd.read_csv("matchID_chall.csv", encoding="utf-8-sig")
#
# for i in range(5):
#     match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchID_chall['MatchId'][i] + "?api_key=" + api_key
#     r = requests.get(match_url)
#
#
#     print(i,"번째 match정보입니다. --------------------------------------------------------------")
#     print(matchID_chall['MatchId'][i],"에 대한 전체 정보: ", r.json())
#
#
#
#     print("meta--------------------------------------")
#     print("MatchId 입니다: ", r.json()['metadata']['matchId'])
#     print("게임에 참가한 전체 참가자 정보입니다: ", r.json()['metadata']['participants'])
    #
    # print("info--------------------------------------")
    # print("경기 진행 시간: ", r.json()['info']['gameDuration'])
    # print("경기 모드: ", r.json()['info']['gameMode'])
    #
    # print("info/participants[i]--------------------------------------")
    # print("0번째 참가자의 puuid: ", r.json()['info']['participants'][0]['puuid'])
    # print("0번째 참가자의 어시스트: ", r.json()['info']['participants'][0]['assists'])
    # print("0번째 참가자의 어시스트: ", r.json()['info']['participants'][0]['champLevel'])
    # print("0번째 참가자의 챔피언 아이디: ", r.json()['info']['participants'][0]['championId'])
    # print("0번째 참가자의 챔피언 이름: ", r.json()['info']['participants'][0]['championName'])
    #
    # print("0번째 참가자의 퍼블 어시스트(T/F): ", r.json()['info']['participants'][0]['firstBloodAssist'])
    # print("0번째 참가자의 퍼블 여부(T/F): ", r.json()['info']['participants'][0]['firstBloodKill'])
    # print("0번째 참가자의 포블 어시스트(T/F): ", r.json()['info']['participants'][0]['firstTowerAssist'])
    # print("0번째 참가자의 포블(T/F): ", r.json()['info']['participants'][0]['firstTowerKill'])
    #
    # # print("0번째 참가자의 팀포지션??(잘모르겠음)", r.json()['info']['participants'][0]['individualPosition'])
    # print("0번째 참가자의 팀포지션??(잘모르겠음)", r.json()['info']['participants'][0]['teamPosition'])
    #
    # print("0번째 참가자의 item0: ", r.json()['info']['participants'][0]['item0'])
    # print("0번째 참가자의 item1: ", r.json()['info']['participants'][0]['item1'])
    # print("0번째 참가자의 item2: ", r.json()['info']['participants'][0]['item2'])
    # print("0번째 참가자의 item3: ", r.json()['info']['participants'][0]['item3'])
    # print("0번째 참가자의 item4: ", r.json()['info']['participants'][0]['item4'])
    # print("0번째 참가자의 item5: ", r.json()['info']['participants'][0]['item5'])
    # print("0번째 참가자의 item6: ", r.json()['info']['participants'][0]['item6'])
    #
    #
    # print("0번째 참가자의 kill횟수: ", r.json()['info']['participants'][0]['kills'])
    # print("0번째 참가자의 펜타킬: ", r.json()['info']['participants'][0]['pentaKills'])
    #
    #
    # print("info/participants[i]/['perks']--------------------------------------")
    # print("0번째 참가자의 룬특성(적응형, 방어력, 마법저항력): ", r.json()['info']['participants'][0]['perks']["statPerks"]["defense"])
    # print("0번째 참가자의 룬특성(적응형, 방어력, 마법저항력): ", r.json()['info']['participants'][0]['perks']["statPerks"]["flex"])
    # print("0번째 참가자의 룬특성(적응형, 방어력, 마법저항력): ", r.json()['info']['participants'][0]['perks']["statPerks"]["offense"])
    #
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][0]['description'])
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][0]['selections'])
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][0]['style'])
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][1]['style'])

    # description = primaryStyle
    # r.json()['info']['participants'][0]['perks']['styles'][0]['selections'][0]['perk']  - selction 아래 4개의 'perk', 'var1','var2','var3'
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][0]['selections'][0]['perk'])
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][0]['selections'][0]['var1'])
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][0]['selections'][0]['var2'])
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][0]['selections'][0]['var3'])
    #
    # # description = subStyle/ selction 아래 2개의 'perk', 'var1','var2','var3'
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][1]['description'])  # sub
    # print("0번째 참가자의 룬특성(정밀, 지배 등)- : ", r.json()['info']['participants'][0]['perks']['styles'][1]['selections'][0]['perk'])
    #
    # print("0번째 참가자의 쿼드라킬: ", r.json()['info']['participants'][0]['quadraKills'])
    #
    # print("0번째 참가자의 소환사 주문 D: ", r.json()['info']['participants'][0]['summoner1Id'])
    # print("0번째 참가자의 소환사 주문 F: ", r.json()['info']['participants'][0]['summoner2Id'])
    #
    # print("0번째 참가자의 소환사의 레벨(게임 전체): ", r.json()['info']['participants'][0]['summonerLevel'])
    # print("0번째 참가자의 소환사 닉네임: ", r.json()['info']['participants'][0]['summonerName'])
    #
    # print("0번째 참가자의 챔피언에게 가한 총 피해량: ", r.json()['info']['participants'][0]['totalDamageDealtToChampions'])
    # print("0번째 참가자의 맞은 피해량: ", r.json()['info']['participants'][0]['totalDamageTaken'])
    #
    # # CS --------------------------------------------------
    # print("0번째 참가자의 전체 미니언 킬: ", r.json()['info']['participants'][0]['totalMinionsKilled'])
    # print("0번째 참가자의 전체 정글 미니언 킬 총량: ", r.json()['info']['participants'][0]['totalEnemyJungleMinionsKilled'])
    #
    #
    # print("0번째 참가자의 트리플킬: ", r.json()['info']['participants'][0]['tripleKills'])
    # print("0번째 참가자의 시야 점수: ", r.json()['info']['participants'][0]['visionScore'])
    #
    # print("0번째 참가자의 비전와드 구매 횟수: ", r.json()['info']['participants'][0]['visionWardsBoughtInGame'])
    # print("0번째 참가자의 와드 파괴 수 : ", r.json()['info']['participants'][0]['wardsKilled'])
    # print("0번째 참가자의 와드 설치 수: ", r.json()['info']['participants'][0]['wardsPlaced'])
    #
    # print("0번째 참가자의 승패여부(T/F): ", r.json()['info']['participants'][0]['win'])



matchID_chall = pd.read_csv("matchID_chall.csv", encoding="utf-8-sig")
match_list = list(matchID_chall['MatchId'])

matchID_grand = pd.read_csv("matchID_grand.csv", encoding="utf-8-sig")
match_list += list(matchID_grand['MatchId'])

matchID_mast = pd.read_csv("matchID_mast.csv", encoding="utf-8-sig")
match_list += list(matchID_mast['MatchId'])


print("전체 matchID의 개수: ", len(match_list))
match_list = set(match_list)
match_list = list(match_list)
print("전체 matchID의 개수: ", len(match_list))
