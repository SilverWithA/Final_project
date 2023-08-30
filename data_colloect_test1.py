import requests
import pandas as pd
import time


api_key = "RGAPI-96d4602c-940f-4bd3-b2dd-f6f6f7726996"
print("api 키가 저장되었습니다.")

# 티어별 사용자 정보 가져오기
def collect_tiers(queue,tier,division,pages):
    summoner_df = pd.DataFrame()


    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for page in range(1,pages+1):


        print(f"{page}번째 페이지의 플레이 정보를 불러옵니다.")
        leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + queue + "/" + tier+ "/" + division + "?page=" + str(page) + "&api_key=" + api_key
        r = requests.get(leagueV4_url)

        # 각 페이지의 닉네임만 담은 page_df
        page_df = pd.DataFrame(r.json())["summonerName"]


        # 닉네임만 담은 summoner_df
        summoner_df = pd.concat([summoner_df, page_df], axis=0,ignore_index=True)
    print(summoner_df.head())
    print("summoner_df의 정보의 길이: ", len(summoner_df))




    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------

    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    playerinfo_df = pd.DataFrame(columns=['summonerName','puuid'])
    for i in range(len(summoner_df)-380):

        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_df[0][i] + "?api_key=" + api_key
        r = requests.get(puuid_url)
        print(i,"번째 데이터: ", r.json())



        if 'status' in  r.json():


            # 조회할 수 없는 회원일때
            if r.json()['status']['message'] == 'Data not found - summoner not found':
                print("조회할 수 없는 회원입니다.")
                continue

            # 조회 리밋이 걸렸을 때 -> 시간 텀(2분)을 뒀다가 다시 조회 시작
            elif r.json()['status']['message'] == 'Rate limit exceeded':
                print("2분 쉬어갑니다.")
                time.sleep(120)
                r = requests.get(puuid_url)
                print(i,"번째 데이터: ", r.json())
            else:
                continue


        # 정보가 행단위로 playerinfo_df에 생성되도록 구성
        meta_summoner = r.json()["name"]
        meta_puuid = r.json()["puuid"]
        playerinfo_df.loc[i] = [meta_summoner,meta_puuid]

    return playerinfo_df

EMERALD_IIdf = collect_tiers("RANKED_SOLO_5x5", "EMERALD", "II", 2)
print(EMERALD_IIdf.head())
