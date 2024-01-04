import threading
import requests
import time

api_key = ""

# 데이터를 저장할 리스트
result_data = []
result_data_lock = threading.Lock()
puuids = []
def fetch_matchID(summonerName):
    try:
        matchID_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + str(matchID) + "?api_key=" + str(api_key)
        response = requests.get(matchID_url)
        data = response.json()

        with result_data_lock:
            result_data.append(data)
        return

    except Exception as e:
        print(f"Error fetching data from {matchID_url}: {str(e)}")


def main():
    start_time = time.time()
    # 병렬로 요청할 API URL 리스트
    matchIDs = ['KR_6874248553'] * 300

    # 스레드를 담을 리스트
    threads = []

    # 각 URL에 대해 스레드 생성 및 실행
    for matchID in matchIDs:
        thread1 = threading.Thread(target=fetch_matchID, args=(matchID,))
        threads.append(thread1)
        thread1.start()

    # 모든 스레드가 종료될 때까지 대기
    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"took {elapsed_time:.2f} seconds.")

    print("matchID 개수: ",len(result_data))
    print("스레드의 개수: ",len(threads))
    return result_data

if __name__ == "__main__":
    matchID_data = main()