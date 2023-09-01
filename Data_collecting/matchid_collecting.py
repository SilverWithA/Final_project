import pandas as pd
import time
import requests




# 데이터 불러오기
# chall_df,grand_df,mast_df
# em1_df, em2_df, em3_df, em4_df
# gold1_df, gold2_df, gold3_df, gold4_df
# sil1_df, sil2_df, sil3_df, sil4_d

sil1_df= pd.DataFrame()
sil2_df= pd.DataFrame()
sil3_df= pd.DataFrame()
sil4_d = pd.DataFrame()



# bro1_df, bro2_df, bro3_df, bro4_df
# iron1_df, iron2_df, iron3_df, iron4_df

name_data = [sil1_df, sil2_df, sil3_df, sil4_d]
load_name = ["name_puuid_sil1.csv","name_puuid_sil2.csv","name_puuid_sil3.csv","name_puuid_sil4.csv"]


for i in range(len(name_data)):
    name_data[i] = pd.read_csv(load_name[i], encoding="utf-8-sig")



# api키 저장하기
api_key =
print("api 키가 저장되었습니다.")

def collect_matchid(df):
    matchid_list = []

    # MatchID 가져오기
    for i in range(len(df)):

        match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + df["puuid"][i] + "/ids?start=0&count=20&api_key=" + api_key
        r = requests.get(match_url)
        print(f"현재 {i}번째 puuid에 대한 정보를 불러왔습니다.", r.json())

        if 'status' in  r.json():
            # (1) 조회할 수 없는 회원 일때 - 'Data not found - summoner not found'
            if r.json()['status']['message'] == 'Rate limit exceeded':

                print("2분 쉬어갑니다.")
                time.sleep(120)
                r = requests.get(match_url)
                print(i,"번째 데이터를 다시 가져오고 있습니다.: ", r.json())

            else:
                continue

        # 리스트 형식으로 가져와짐:r.json()
        matchid_list += r.json()


    print("matchID를 모두 불러와 저장했습니다.")

    print("중복 제거 전 길이: ", len(matchid_list))
    matchid_list = set(matchid_list)
    print("중복 제거 전 길이: ", len(matchid_list))
    matchid_list = list(matchid_list)
    matchid_df= pd.DataFrame({"MatchId":matchid_list})
    print("===============MatchID를 df화 하였습니다============")

    return matchid_df



save_name = ["matchID_sil1.csv","matchID_sil2.csv","matchID_sil3.csv","matchID_sil4.csv"]

for i in range(len(name_data)):
    matchid_df = collect_matchid(name_data[i])
    print("담긴 matchid 개수: ", len(matchid_df))
    matchid_df.to_csv(save_name[i], index=False, encoding="utf-8-sig")
    print(f"{save_name[i]} 파일이 저장되었습니다.")
