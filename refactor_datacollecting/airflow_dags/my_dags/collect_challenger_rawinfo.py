import copy

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime
from custom_modules.collect_summners import collect_summonerNames
from custom_modules.collect_puuidByThread import collect_puuids


def _summoner_task(ti):
    # API 호출
    summonerNames = collect_summonerNames()
    # xcom에 닉네임 저장
    ti.xcom_push(key="summnoerChallenger", value = summonerNames)

def _puuid_task(ti):
    puuids = collect_puuids(ti.xcom_pull(key="summnoerChallenger"))
    ti.xcom_push(key="puuidsChallenger", value=puuids)

with DAG("collect_challenger_Gameinfo", start_date=datetime(2024, 1, 1),
    schedule_interval='@daily', catchup=False) as dag:

    summoner_task = PythonOperator(
        task_id="summoner_task",
        python_callable=_summoner_task
    )

    puuid_task = PythonOperator(
        task_id="puuid_task",
        python_callable=_puuid_task
    )



    summoner_task >> puuid_task

