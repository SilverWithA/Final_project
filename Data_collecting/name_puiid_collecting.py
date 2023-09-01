import requests
import pandas as pd
import time


api_key =
print("api 키가 저장되었습니다.")

# 티어별 사용자 정보 가져오기: 아이언~에메랄드
def collect_tiers(queue,tier,division,pages,user_cnt):
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
    for i in range(user_cnt):
    # for i in range(len(summoner_df)):

        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_df[0][i] + "?api_key=" + api_key
        r = requests.get(puuid_url)
        print(i,"번째 데이터를 가져오고 있습니다.", r.json())


        # 조회가 정상적으로 이뤄지지 않앗을때
        if 'status' in r.json():
            # (1) 조회할 수 없는 회원 일때 - 'Data not found - summoner not found'
            if r.json()['status']['message'] == 'Data not found - summoner not found':
                print("조회할 수 없는 회원입니다.")
                continue
            # (2) 조회 리밋이 걸렸을 때 - 'Rate limit exceeded' -> 시간 텀(2분)을 뒀다가 다시 조회 시작
            elif r.json()['status']['message'] == 'Rate limit exceeded':

                print("2분 쉬어갑니다.")
                time.sleep(120)
                r = requests.get(puuid_url)
                print(i,"번째 데이터를 다시 가져오고 있습니다.: ", r.json())

            # (1),(2)번의 경우도 아닐 때 해당 닉네임 조회는 넘어감  - continue
            else:
                continue


        # 정보가 행단위로 playerinfo_df에 생성되도록 구성
        meta_summonerName = r.json()["name"]
        meta_puuid = r.json()["puuid"]

        playerinfo_df.loc[i] = [meta_summonerName, meta_puuid]

    return playerinfo_df



# -------------------------데이터 저장하기--------------------------------
# 다이아 ----------------------------------
# DIAMOND_Idf = collect_tiers("RANKED_SOLO_5x5", "DIAMOND", "I", 1,65)
# print(DIAMOND_Idf.head())
# DIAMOND_Idf.to_csv("name_puuid_dia1.csv", index = False, encoding="utf-8-sig")
# time.sleep(120)
# #
# DIAMOND_IIdf = collect_tiers("RANKED_SOLO_5x5", "DIAMOND", "II", 1,60)
# DIAMOND_IIdf.to_csv("name_puuid_dia2.csv", index = False, encoding="utf-8-sig")
# time.sleep(120)
#
# DIAMOND_IIIdf = collect_tiers("RANKED_SOLO_5x5", "DIAMOND", "III", 1,60)
# # print(DIAMOND_IIIdf.head())
# DIAMOND_IIIdf.to_csv("name_puuid_dia3.csv", index = False, encoding="utf-8-sig")
# time.sleep(120)
#
# DIAMOND_IVdf = collect_tiers("RANKED_SOLO_5x5", "DIAMOND", "IV", 1,65)
# # print(DIAMOND_IVdf.head())
# DIAMOND_IVdf.to_csv("name_puuid_dia4.csv", index = False, encoding="utf-8-sig")
# #
# # 에메랄드 --------------------------------------------------

# EMERALD_Idf = collect_tiers("RANKED_SOLO_5x5", "EMERALD", "I", 2,215)
# EMERALD_Idf.to_csv("name_puuid_em1.csv", index = False, encoding="utf-8-sig")
# print("2분 쉬고 다른 디비젼으로 넘어감니다.")
# time.sleep(120)
#
# EMERALD_IIdf = collect_tiers("RANKED_SOLO_5x5", "EMERALD", "II", 2,210)
# EMERALD_IIdf.to_csv("name_puuid_em2.csv", index = False, encoding="utf-8-sig")
# print("2분 쉬고 다른 디비젼으로 넘어감니다.")
# time.sleep(120)
#
#
# EMERALD_IIIdf = collect_tiers("RANKED_SOLO_5x5", "EMERALD", "III", 2,210)
# EMERALD_IIIdf.to_csv("name_puuid_em3.csv", index = False, encoding="utf-8-sig")
# print("2분 쉬고 다른 디비젼으로 넘어감니다.")
# time.sleep(120)
#
#
#
# EMERALD_IVdf = collect_tiers("RANKED_SOLO_5x5", "EMERALD", "IV", 2,215)
# EMERALD_IVdf.to_csv("name_puuid_em4.csv", index = False, encoding="utf-8-sig")

# 플래티넘 ---------------------------------
# PLATINUM_Idf = collect_tiers("RANKED_SOLO_5x5", "PLATINUM", "I", 2,375)
# PLATINUM_Idf.to_csv("name_puuid_pla1.csv", index = False, encoding="utf-8-sig")
# print("PLATINUM_Idf")
#
#
# PLATINUM_IIdf = collect_tiers("RANKED_SOLO_5x5", "PLATINUM", "II", 2,375)
# PLATINUM_IIdf.to_csv("name_puuid_pla2.csv", index = False, encoding="utf-8-sig")
# print("PLATINUM_IIdf")
#
#
#
# PLATINUM_IIIdf = collect_tiers("RANKED_SOLO_5x5", "PLATINUM", "III", 2,375)
# PLATINUM_IIIdf.to_csv("name_puuid_pla3.csv", index = False, encoding="utf-8-sig")
# print("PLATINUM_IIIdf")
#
#
# PLATINUM_IVdf = collect_tiers("RANKED_SOLO_5x5", "PLATINUM", "IV", 2,375)
# PLATINUM_IVdf.to_csv("name_puuid_pla4.csv", index = False, encoding="utf-8-sig")



# 골드 ------------------------------------
# GOLD_Idf = collect_tiers("RANKED_SOLO_5x5", "GOLD", "I", 3,475)
# GOLD_Idf.to_csv("name_puuid_gold1.csv", index = False, encoding="utf-8-sig")
# print("GOLD_Idf")
#
#
# GOLD_IIdf = collect_tiers("RANKED_SOLO_5x5", "GOLD", "II", 3,475)
# GOLD_IIdf.to_csv("name_puuid_gold2.csv", index = False, encoding="utf-8-sig")
# print("GOLD_IIdf")
#
#
#
# GOLD_IIIdf = collect_tiers("RANKED_SOLO_5x5", "GOLD", "III", 3,475)
# GOLD_IIIdf.to_csv("name_puuid_gold3.csv", index = False, encoding="utf-8-sig")
# print("GOLD_IIIdf")
#
#
# GOLD_IVdf = collect_tiers("RANKED_SOLO_5x5", "GOLD", "IV", 3,475)
# GOLD_IVdf.to_csv("name_puuid_gold4.csv", index = False, encoding="utf-8-sig")

# 실버 ------------------------------------
# SILVER_Idf = collect_tiers("RANKED_SOLO_5x5", "SILVER", "I", 3,450)
# SILVER_Idf.to_csv("name_puuid_sil1.csv", index = False, encoding="utf-8-sig")
# print("SILVER_Idf 저장이 끝났습니다.")
#
#
# SILVER_IIdf = collect_tiers("RANKED_SOLO_5x5", "SILVER", "II", 3,450)
# SILVER_IIdf.to_csv("name_puuid_sil2.csv", index = False, encoding="utf-8-sig")
# print("SILVER_IIdf 저장이 끝났습니다.")
#
#
#
# SILVER_IIIdf = collect_tiers("RANKED_SOLO_5x5", "SILVER", "III", 3,450)
# SILVER_IIIdf.to_csv("name_puuid_sil3.csv", index = False, encoding="utf-8-sig")
# print("SILVER_IIIdf 저장이 끝났습니다.")
#
#
# SILVER_IVdf = collect_tiers("RANKED_SOLO_5x5", "SILVER", "IV", 3,450)
# SILVER_IVdf.to_csv("name_puuid_sil4.csv", index = False, encoding="utf-8-sig")

# 브론즈 ----------------------------------
# BRONZE_Idf = collect_tiers("RANKED_SOLO_5x5", "BRONZE", "I", 3,450)
# BRONZE_Idf.to_csv("name_puuid_bro1.csv", index = False, encoding="utf-8-sig")
# print("BRONZE_Idf 저장이 끝났습니다.")
#
#
# BRONZE_IIdf = collect_tiers("RANKED_SOLO_5x5", "BRONZE", "II", 3,450)
# BRONZE_IIdf.to_csv("name_puuid_bro2.csv", index = False, encoding="utf-8-sig")
# print("BRONZE_IIdf 저장이 끝났습니다.")
#
#
#
# BRONZE_IIIdf = collect_tiers("RANKED_SOLO_5x5", "BRONZE", "III", 3,450)
# BRONZE_IIIdf.to_csv("name_puuid_bro3.csv", index = False, encoding="utf-8-sig")
# print("BRONZE_IIIdf 저장이 끝났습니다.")
#
#
# BRONZE_IVdf = collect_tiers("RANKED_SOLO_5x5", "BRONZE", "IV", 3,450)
# BRONZE_IVdf.to_csv("name_puuid_bro4.csv", index = False, encoding="utf-8-sig")
# 아이언 ----------------------------------
# IRON_Idf = collect_tiers("RANKED_SOLO_5x5", "IRON", "I", 1,200)
# IRON_Idf.to_csv("name_puuid_iron1.csv", index = False, encoding="utf-8-sig")
# print("IRON_Idf 저장이 끝났습니다.")


IRON_IIdf = collect_tiers("RANKED_SOLO_5x5", "IRON", "II", 1,200)
IRON_IIdf.to_csv("name_puuid_iron2.csv", index = False, encoding="utf-8-sig")
print("IRON_IIdf 저장이 끝났습니다.")



IRON_IIIdf = collect_tiers("RANKED_SOLO_5x5", "IRON", "III", 1,200)
IRON_IIIdf.to_csv("name_puuid_iron3.csv", index = False, encoding="utf-8-sig")
print("IRON_IIIdf 저장이 끝났습니다.")


IRON_IVdf = collect_tiers("RANKED_SOLO_5x5", "IRON", "IV", 1,200)
IRON_IVdf.to_csv("name_puuid_iron4.csv", index = False, encoding="utf-8-sig")