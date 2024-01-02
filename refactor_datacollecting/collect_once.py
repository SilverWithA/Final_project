import requests
import pandas as pd
import time

api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"
def collect_puuid(collect_cnt, summoner_names):
    """collect_cnt만큼의 유저수, 닉네임 리스트(summnor_names)를 받아 puuid와 닉네임을 담은 playerinfo_df를 반환하는 함수"""
    playerinfo_df = pd.DataFrame(columns=['summonerName', 'puuid'])

    for i in range(collect_cnt):

        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_names[i] + "?api_key=" + api_key
        r = requests.get(puuid_url)
        print(i, "번째 데이터를 가져오고 있습니다.")

        if 'status' in r.json():
            # (1) 조회할 수 없는 회원 일 때 - 'Data not found - summoner not found'
            if r.json()['status']['message'] == 'Data not found - summoner not found':
                print("조회할 수 없는 회원입니다.")
                continue
            # (2) 조회 리밋이 걸렸을 때 - 'Rate limit exceeded' -> 시간 텀(2분)을 뒀다가 다시 조회 시작
            elif r.json()['status']['message'] == 'Rate limit exceeded':

                print("2분 쉬어갑니다.")
                time.sleep(120)
                r = requests.get(puuid_url)
                print(i, "번째 데이터를 다시 가져오고 있습니다.: ", r.json())

            # (1),(2)번의 경우도 아닐 때 해당 닉네임 조회는 넘어감  - continue
            else:
                continue

        # 정보가 행단위로 playerinfo_df에 생성되도록 구성
        meta_summonerName = r.json()["name"]
        meta_puuid = r.json()["puuid"]

        playerinfo_df.loc[i] = [meta_summonerName, meta_puuid]
    return playerinfo_df
challen_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
r = requests.get(challen_url)

callen_count = len(r.json()["entries"])
summonerNames = []
for i in range(callen_count):
    summonerNames.append(r.json()["entries"][i]["summonerName"])

# API에서 puuidID 호출
playerinfo_df = collect_puuid(1, summonerNames)
print("닉네임과 puuid를 수집했습니다")
print(playerinfo_df)

# -----------------------------
matchid_list = []


for i in range(len(playerinfo_df)):  # len(select_df)
    match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + playerinfo_df["puuid"][i] + "/ids?start=0&count=20&api_key=" + api_key
    r = requests.get(match_url)

    matchid_list += r.json()


print("matchID 정보를 수집했습니다")
print(matchid_list)

# --------------------------------------------------------------
tier_list = []
for i in range(1):
    match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid_list[i] + "?api_key=" + api_key  # mat_cnt[i]
    mat_info = requests.get(match_url)

    timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid_list[i] + "/timeline?api_key=" + api_key
    mat_timeline = requests.get(timeline_url)

    total_json = {"mat_info": mat_info.json(),
                  "mat_timeline": mat_timeline.json()}

    tier_list.append(total_json)
print(tier_list)