import requests
import pandas as pd
import time
import pymysql.cursors


api_key = "RGAPI-96d4602c-940f-4bd3-b2dd-f6f6f7726996"
print("api 키가 저장되었습니다.")

# MySQL 연동을 위한 기본 설정
conn = pymysql.connect(host="127.0.0.1", user="root", password="qwer1234", db="conn_test", charset="utf8")
cur = conn.cursor()

def collect_puuid(collect_cnt, summoner_names):
    """닉네임 리스트(summnor_names)를 받아 puuid와 닉네임을 담은 playerinfo_df를 반환하는 함수"""
    playerinfo_df = pd.DataFrame(columns=['summonerName', 'puuid'])
    for i in range(collect_cnt):

        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_names[i] + "?api_key=" + api_key
        r = requests.get(puuid_url)
        print(i, "번째 데이터를 가져오고 있습니다.", r.json())

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
def puuid_Chall(collect_cnt):
    "Challenger의 닉네임과 puuid를 불러와 저장하는 함수"

    # API에서 챌린저 닉네임 불러오기
    challen_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(challen_url)
    print(r.json())

    callen_count = len(r.json()["entries"])
    print("챌린저 거주 인구 수: ", callen_count)


    # puuid 조회를 위해 모든 닉넨임을 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(callen_count):
        summonerNames.append(r.json()["entries"][i]["summonerName"])

    # print(summonerNames)
    # print("summonerNames의 길이: ", len(summonerNames))

    # puuidID 추출하기:SUMMONER-V4 ---------------------------------------
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt,summonerNames)

    # MySQL의 저장하기
    print("데이터를 DB에 저장합니다.")
    # cur.execute("CREATE TABLE challusr_info (summonerName varchar(255), puuid varchar(255))")

    for i in range(len(playerinfo_df)):
        try:
            cur.execute('INSERT INTO challusr_info (summonerName,puuid) VALUES(%s, %s)',(str(playerinfo_df['summonerName'][i]),str(playerinfo_df['puuid'][i])))
            print(f"{i}번째 데이터가 DB에 저장되었습니다.")

        except Exception as e:
            print(f"{i}번째에서 에러가 발생하였습니다." ,e)
            continue
    conn.commit()
    conn.close()
# puuid_Chall(20)
def puuid_grand(collect_cnt):
    """grandmaster의 닉네임과 puuid를 불러와 저장하는 함수"""

    # API에서 그마 닉네임 불러오기
    grand_url = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(grand_url)

    grand_count = len(r.json()["entries"])
    print("그마 거주 인구 수: ", grand_count)

    # puuid 조회를 위해 모든 닉넨임을 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(grand_count):
        summonerNames.append(r.json()["entries"][i]["summonerName"])


    # puuidID 추출하기:SUMMONER-V4 ---------------------------------------
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt,summonerNames)

    # MySQL의 저장하기
    print("데이터를 DB에 저장합니다.")
    # cur.execute("CREATE TABLE grandUsr_info (summonerName varchar(17), puuid varchar(255))")

    for i in range(len(playerinfo_df)):
        try:
            cur.execute('INSERT INTO grandUsr_info (summonerName,puuid) VALUES(%s, %s)',(str(playerinfo_df['summonerName'][i]),str(playerinfo_df['puuid'][i])))
            print(f"{i}번째 데이터가 DB에 저장되었습니다.")

        except Exception as e:
            print(f"{i}번째에서 에러가 발생하였습니다." ,e)
            continue
    conn.commit()
    conn.close()
# puuid_grand(40)
def puuid_mast(collect_cnt):
    """master 닉네임과 puuid를 불러와 저장하는 함수"""

    # API에서 마스터 닉네임 불러오기
    grand_url = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(grand_url)

    mast_count = len(r.json()["entries"])
    print("마스터 거주 인구 수: ", mast_count)

    # puuid 조회를 위해 모든 닉넨임을 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(mast_count):
        summonerNames.append(r.json()["entries"][i]["summonerName"])

    # puuidID 추출하기:SUMMONER-V4 ---------------------------------------
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)

    # MySQL의 저장하기
    print("데이터를 DB에 저장합니다.")
    cur.execute("CREATE TABLE mastUsr_info (summonerName varchar(17), puuid varchar(255))")

    for i in range(len(playerinfo_df)):
        try:
            cur.execute('INSERT INTO mastUsr_info (summonerName,puuid) VALUES(%s, %s)',
                        (str(playerinfo_df['summonerName'][i]), str(playerinfo_df['puuid'][i])))
            print(f"{i}번째 데이터가 DB에 저장되었습니다.")

        except Exception as e:
            print(f"{i}번째에서 에러가 발생하였습니다.", e)
            continue
    conn.commit()
    conn.close()
# puuid_mast(70)
def puuid_dia(collect_cnt):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt//4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt+mod]
    div_num = ["I","II","III","IV"]


    summoner_df = pd.DataFrame()
    page_df = pd.DataFrame()
    summonerNames = []

    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for i in range(len(div_cnt)):
        print()
        print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
        pages = (div_cnt[i]// 200)+1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")


        for page in range(1,int(pages)+1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "DIAMOND"+ "/" + div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

        print("summoner_df의 정보의 길이: ", len(summonerNames))


    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)

    # MySQL의 저장하기
    print("데이터를 DB에 저장합니다.")
    cur.execute("CREATE TABLE DiaUsr_info (summonerName varchar(17), puuid varchar(255))")

    for i in range(len(playerinfo_df)):
        try:
            cur.execute('INSERT INTO DiaUsr_info (summonerName,puuid) VALUES(%s, %s)',
                        (str(playerinfo_df['summonerName'][i]), str(playerinfo_df['puuid'][i])))
            print(f"{i}번째 데이터가 DB에 저장되었습니다.")

        except Exception as e:
            print(f"{i}번째에서 에러가 발생하였습니다.", e)
            continue
    conn.commit()
    conn.close()
puuid_dia(250)




# --------------여기까지함 이 아래는 안함 mysql 연동 코드 추가해줘야함------------------------------------
def puuid_em(collect_cnt,save_name):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt//4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt+mod]
    div_num = ["I","II","III","IV"]


    summoner_df = pd.DataFrame()
    page_df = pd.DataFrame()
    summonerNames = []

    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for i in range(len(div_cnt)):
        print()
        print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
        pages = (div_cnt[i]// 200)+1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")


        for page in range(1,int(pages)+1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "EMERALD"+ "/" + div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

        print("summoner_df의 정보의 길이: ", len(summonerNames))


    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)
    playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")
def puuid_pla(collect_cnt,save_name):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt//4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt+mod]
    div_num = ["I","II","III","IV"]


    summoner_df = pd.DataFrame()
    page_df = pd.DataFrame()
    summonerNames = []

    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for i in range(len(div_cnt)):
        print()
        print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
        pages = (div_cnt[i]// 200)+1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")


        for page in range(1,int(pages)+1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "PLATINUM"+ "/" + div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

        print("summoner_df의 정보의 길이: ", len(summonerNames))


    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)
    playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")

    def puuid_pla(collect_cnt, save_name):
        """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
        # 각 division별 불러올 데이터 개수 결정
        each_cnt = int(collect_cnt // 4)
        mod = collect_cnt - each_cnt * 4
        div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt + mod]
        div_num = ["I", "II", "III", "IV"]

        summoner_df = pd.DataFrame()
        page_df = pd.DataFrame()
        summonerNames = []

        # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
        for i in range(len(div_cnt)):
            print()
            print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
            pages = (div_cnt[i] // 200) + 1
            cnt = 0
            # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")

            for page in range(1, int(pages) + 1):
                # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
                leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "PLATINUM" + "/" + \
                               div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
                r = requests.get(leagueV4_url)

                # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
                for usr in range(len(r.json())):
                    summonerNames.append(r.json()[usr]["summonerName"])
                    cnt += 1

                    # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                    if cnt == div_cnt[i]:
                        break

            print("summoner_df의 정보의 길이: ", len(summonerNames))

        # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
        # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
        print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
        playerinfo_df = collect_puuid(collect_cnt, summonerNames)
        playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")
def puuid_gold(collect_cnt,save_name):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt//4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt+mod]
    div_num = ["I","II","III","IV"]


    summoner_df = pd.DataFrame()
    page_df = pd.DataFrame()
    summonerNames = []

    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for i in range(len(div_cnt)):
        print()
        print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
        pages = (div_cnt[i]// 200)+1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")


        for page in range(1,int(pages)+1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "GOLD"+ "/" + div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

        print("summoner_df의 정보의 길이: ", len(summonerNames))


    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)
    playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")

    def puuid_pla(collect_cnt, save_name):
        """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
        # 각 division별 불러올 데이터 개수 결정
        each_cnt = int(collect_cnt // 4)
        mod = collect_cnt - each_cnt * 4
        div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt + mod]
        div_num = ["I", "II", "III", "IV"]

        summoner_df = pd.DataFrame()
        page_df = pd.DataFrame()
        summonerNames = []

        # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
        for i in range(len(div_cnt)):
            print()
            print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
            pages = (div_cnt[i] // 200) + 1
            cnt = 0
            # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")

            for page in range(1, int(pages) + 1):
                # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
                leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "PLATINUM" + "/" + \
                               div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
                r = requests.get(leagueV4_url)

                # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
                for usr in range(len(r.json())):
                    summonerNames.append(r.json()[usr]["summonerName"])
                    cnt += 1

                    # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                    if cnt == div_cnt[i]:
                        break

            print("summoner_df의 정보의 길이: ", len(summonerNames))

        # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
        # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
        print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
        playerinfo_df = collect_puuid(collect_cnt, summonerNames)
        playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")
def puuid_sil(collect_cnt,save_name):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt//4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt+mod]
    div_num = ["I","II","III","IV"]


    summoner_df = pd.DataFrame()
    page_df = pd.DataFrame()
    summonerNames = []

    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for i in range(len(div_cnt)):
        print()
        print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
        pages = (div_cnt[i]// 200)+1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")


        for page in range(1,int(pages)+1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "SILVER"+ "/" + div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

        print("summoner_df의 정보의 길이: ", len(summonerNames))


    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)
    playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")

    def puuid_pla(collect_cnt, save_name):
        """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
        # 각 division별 불러올 데이터 개수 결정
        each_cnt = int(collect_cnt // 4)
        mod = collect_cnt - each_cnt * 4
        div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt + mod]
        div_num = ["I", "II", "III", "IV"]

        summoner_df = pd.DataFrame()
        page_df = pd.DataFrame()
        summonerNames = []

        # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
        for i in range(len(div_cnt)):
            print()
            print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
            pages = (div_cnt[i] // 200) + 1
            cnt = 0
            # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")

            for page in range(1, int(pages) + 1):
                # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
                leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "PLATINUM" + "/" + \
                               div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
                r = requests.get(leagueV4_url)

                # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
                for usr in range(len(r.json())):
                    summonerNames.append(r.json()[usr]["summonerName"])
                    cnt += 1

                    # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                    if cnt == div_cnt[i]:
                        break

            print("summoner_df의 정보의 길이: ", len(summonerNames))

        # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
        # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
        print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
        playerinfo_df = collect_puuid(collect_cnt, summonerNames)
        playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")
def puuid_bro(collect_cnt,save_name):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt//4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt+mod]
    div_num = ["I","II","III","IV"]


    summoner_df = pd.DataFrame()
    page_df = pd.DataFrame()
    summonerNames = []

    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for i in range(len(div_cnt)):
        print()
        print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
        pages = (div_cnt[i]// 200)+1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")


        for page in range(1,int(pages)+1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "BRONZE"+ "/" + div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

        print("summoner_df의 정보의 길이: ", len(summonerNames))


    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)
    playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")

    def puuid_pla(collect_cnt, save_name):
        """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
        # 각 division별 불러올 데이터 개수 결정
        each_cnt = int(collect_cnt // 4)
        mod = collect_cnt - each_cnt * 4
        div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt + mod]
        div_num = ["I", "II", "III", "IV"]

        summoner_df = pd.DataFrame()
        page_df = pd.DataFrame()
        summonerNames = []

        # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
        for i in range(len(div_cnt)):
            print()
            print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
            pages = (div_cnt[i] // 200) + 1
            cnt = 0
            # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")

            for page in range(1, int(pages) + 1):
                # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
                leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "PLATINUM" + "/" + \
                               div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
                r = requests.get(leagueV4_url)

                # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
                for usr in range(len(r.json())):
                    summonerNames.append(r.json()[usr]["summonerName"])
                    cnt += 1

                    # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                    if cnt == div_cnt[i]:
                        break

            print("summoner_df의 정보의 길이: ", len(summonerNames))

        # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
        # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
        print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
        playerinfo_df = collect_puuid(collect_cnt, summonerNames)
        playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")
def puuid_iron(collect_cnt,save_name):
    """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
    # 각 division별 불러올 데이터 개수 결정
    each_cnt = int(collect_cnt//4)
    mod = collect_cnt - each_cnt * 4
    div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt+mod]
    div_num = ["I","II","III","IV"]


    summoner_df = pd.DataFrame()
    page_df = pd.DataFrame()
    summonerNames = []

    # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
    for i in range(len(div_cnt)):
        print()
        print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
        pages = (div_cnt[i]// 200)+1
        cnt = 0
        # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")


        for page in range(1,int(pages)+1):
            # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
            leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "IRON"+ "/" + div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
            r = requests.get(leagueV4_url)

            # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
            for usr in range(len(r.json())):
                summonerNames.append(r.json()[usr]["summonerName"])
                cnt += 1

                # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                if cnt == div_cnt[i]:
                    break

        print("summoner_df의 정보의 길이: ", len(summonerNames))


    # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
    # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
    print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
    playerinfo_df = collect_puuid(collect_cnt, summonerNames)
    playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")

    def puuid_pla(collect_cnt, save_name):
        """다이아 이하의 티어별 사용자의 닉네임과 puuid를 수집합니다"""
        # 각 division별 불러올 데이터 개수 결정
        each_cnt = int(collect_cnt // 4)
        mod = collect_cnt - each_cnt * 4
        div_cnt = [each_cnt, each_cnt, each_cnt, each_cnt + mod]
        div_num = ["I", "II", "III", "IV"]

        summoner_df = pd.DataFrame()
        page_df = pd.DataFrame()
        summonerNames = []

        # 티어별 닉네임만 가져오기 API: LEAGUE-V4 --------------------------------------------------------------------------------
        for i in range(len(div_cnt)):
            print()
            print(f"다이아 티어의 divsion {div_num[i]} 정보를 가져옵니다-----------------------")
            pages = (div_cnt[i] // 200) + 1
            cnt = 0
            # print(f"divison{div_num[i]}에서 크롤링해 올 총 페이지의 개수는 {pages}")

            for page in range(1, int(pages) + 1):
                # print(f"divison {div_num[i]}의 {page}번째 페이지의 플레이 정보를 불러옵니다.")
                leagueV4_url = "https://kr.api.riotgames.com/lol/league/v4/entries/" + "RANKED_SOLO_5x5" + "/" + "PLATINUM" + "/" + \
                               div_num[i] + "?page=" + str(page) + "&api_key=" + api_key
                r = requests.get(leagueV4_url)

                # 저장할 닉네임 개수대로 summoner_Names 리스트에 쌓아주기
                for usr in range(len(r.json())):
                    summonerNames.append(r.json()[usr]["summonerName"])
                    cnt += 1

                    # 불러올 정보를 다 불러왔다면 닉네임이 더이상쌓이지 않도록 조정
                    if cnt == div_cnt[i]:
                        break

            print("summoner_df의 정보의 길이: ", len(summonerNames))

        # puuid 따오기: SUMMONER-V4 -------------------------------------------------------------
        # 플레이어의 닉네임(summonerName)과 puuid를 담은 playerinfo_df
        print(f"{collect_cnt}의 닉네임에 대한 puuid를 불러옵니다")
        playerinfo_df = collect_puuid(collect_cnt, summonerNames)
        playerinfo_df.to_csv(save_name, index=False, encoding="utf-8-sig")

