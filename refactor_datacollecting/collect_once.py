import requests
import pandas as pd
import time
from datetime import datetime, timedelta

api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"
current_time = datetime.utcnow()

# 1. 티어별 닉네임 조회
challen_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
r = requests.get(challen_url)

callen_count = len(r.json()["entries"])
summonerNames = []
for i in range(callen_count):
    summonerNames.append(r.json()["entries"][i]["summonerName"])

# print(len(summonerNames))

# summonerNames -> 티어별 닉네임 -----------------------------
# puuuid - matchID까지 조회하기
matchid_list = []
for i in range(1):
    puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerNames[i] + "?api_key=" + api_key
    puuid_r = requests.get(puuid_url)

    user_puuid = puuid_r.json()["puuid"]

    match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + user_puuid + "/ids?start=0&count=20&api_key=" + api_key
    match_r = requests.get(match_url)

    matchid_list += match_r.json()


print("matchID 정보를 수집했습니다")
print(matchid_list)


# 2주 이내 게임 정보가 아니면 gameinfo에서 제외 -> s3에 업로드


tier_list = []
for i in range(1):
    match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid_list[i] + "?api_key=" + api_key  # mat_cnt[i]
    mat_info = requests.get(match_url)
    print(mat_info.json()['info']['gameStartTimestamp'])
    unix_time = int(mat_info.json()['info']['gameStartTimestamp'])/ 1000.0
    two_weeks_ago = current_time - timedelta(weeks=2)

    if two_weeks_ago.timestamp() <= unix_time <= current_time.timestamp():
        # 최근 2주 내의 경기이면 timeline까지 조회
        timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid_list[
            i] + "/timeline?api_key=" + api_key
        mat_timeline = requests.get(timeline_url)

        total_json = {"mat_info": mat_info.json(),
                          "mat_timeline": mat_timeline.json()}

        tier_list.append(total_json)

# 최종 raw data = tier_list


