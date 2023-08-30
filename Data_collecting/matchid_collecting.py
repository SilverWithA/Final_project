import pandas as pd
import time
import requests


# 테스트 데이터 불러오기
playerinfo_df = pd.read_csv("name_puuid_test1.csv", encoding="utf-8-sig")


# api키 저장하기
api_key = "RGAPI-96d4602c-940f-4bd3-b2dd-f6f6f7726996"
print("api 키가 저장되었습니다.")

# MatchID 가져오기
for i in range(10):
    match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + playerinfo_df["puuid"][i] + "/ids?start=0&count=20&api_key=" + api_key
    r = requests.get(match_url)

    # 리스트 형식으로 가져와짐
    print(r.json())


    # 하나의 리스트 matid list에 넣고 관리하고 싶음
    # MatchId와 puuid는 N:M 관계
    # 어떻게 관리해야하지??