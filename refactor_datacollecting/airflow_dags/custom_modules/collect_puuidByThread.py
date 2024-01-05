import threading
import requests
import time


api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"
result_data_lock = threading.Lock()
start_time = time.time()


# 2. 티어별 puuid 조회 - challenger -----------------------
puuids = []
def fetch_puuid(summonerName):
    try:
        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summonerName) + "?api_key=" + api_key
        puuid = requests.get(puuid_url).json()["puuid"]

        with result_data_lock:
            puuids.append(puuid)
        return
    except Exception as e:
        return

def collect_puuids(summonerNames):
    puuid_threads = []
    for i in range(len(summonerNames)):

        if i % 50 == 0 and i > 0:
            time.sleep(10)

        thread = threading.Thread(target=fetch_puuid, args=(summonerNames[i],))
        puuid_threads.append(thread)
        thread.start()

    # 모든 스레드가 종료될 때까지 대기
    for thread in puuid_threads:
        thread.join()
    puuid_list = puuids
    return puuid_list