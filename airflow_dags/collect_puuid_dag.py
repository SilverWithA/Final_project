from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging


import requests
import pandas as pd
import time

from db_functions import *
from setting import *

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
def puuid_Chall(collect_cnt):
    "Challenger의 닉네임과 puuid를 불러와 저장하는 함수"
    # logging.info("challenger의 usrinfo 조회를 시작합니다. -----------------------------")

    # API에서 puuid 불러오기
    challen_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r = requests.get(challen_url)

    callen_count = len(r.json()["entries"])
    # print("챌린저 거주 인구 수: ", callen_count)


    # puuid 조회를 위해 모든 닉네임 summonerNames에 임시로 닉네임 저장
    summonerNames = []
    for i in range(callen_count):
        summonerNames.append(r.json()["entries"][i]["summonerName"])

    # API에서 puuidID 호출
    playerinfo_df = collect_puuid(collect_cnt,summonerNames)

    # MySQL의 저장하기
    playerinfo_df.to_sql(name='chall_usrinfo', con=conn_Usr, if_exists='append',index=False)
    # print("chall_usrinfo Table에 데이터를 저장하였습니다.")


default_args = {
    'owner':'airflow',
    "start_date":datetime(2023,10,12),
    "provide_context": True
}


with DAG(
    # DAG name
    'sum_of_list',
    default_args=default_args,
    # schedule_interval=timedelta(minutes=10),
) as dag:
    collect_cnt = 180
    # Define task
    collect_chall = PythonOperator(
        task_id='collect_chall',
        python_callable=puuid_Chall,
        op_args=[collect_cnt],
        dag=dag
    )

