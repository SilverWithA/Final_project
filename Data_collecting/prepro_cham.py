import pandas as pd
from setting import *
from db_functions import *
from cal_chamfunction import *
import pprint

final_tables = show_tables(engine_gam)

# iterate_perTier안에 들어가는 전처리 함수
def collect_classic(lowCase,table,save_name):
    """iterate_perTier()안에 들어가는 전처리 함수"""
    posit_list = []
    chamID_hash = {}


    # 해당 티어에서 치룬 모든 게임 수: total_cnt
    total_cnt = len(list(set(table['matchID'])))

    # 저장을 위해 chaminfo에 저장된 테이블 스키마 df로 불러오기
    cham_df = select_db(str(save_name),conn_cham)


    # chamID_hash = {챔피언 이름: 챔피언 ID} 매핑해주는 해시 for ban픽 챔피언 서치
    for i in range(len(table)):
        if table['championName'][i] not in chamID_hash:
            chamID_hash[str(table['championName'][i])] = table['championId'][i]


        # 게임에 등장한 모든 teamposition을 담은 posit_list
        if table['teamPosition'][i] not in posit_list:
            posit_list.append(table['teamPosition'][i])


    for i in range(len(teamposit_list)):  # teamposition iterate  # len(posit_list)
        print("조회할 팀포지션은 ",teamposit_list[i],"입니다 --------------------------------------")
        # 포지션 별 챔피언 이름을 중복없이 저장하기 위해 해시 이용: posit_cham
        posit_cham = {}

        for j in range(len(table)):  # all data iterate for collect chamName per position
            if table['teamPosition'][j] == teamposit_list[i]:
                chamName_key = str(table['championName'][j])
                posit_cham[chamName_key] = 0


        # print("posit_cham: ",posit_cham)
        for cham in posit_cham:  # chamName per position iterate
            win_cnt = 0
            ban_cnt = 0
            pick_cnt = 0
            championId = chamID_hash[cham]

            ka_cnt = 0
            kda_list = []

            spell1_1,spell1_2,spell2_1,spell2_2 = cal_spell(table)



            for j in range(len(table)):  # all data iterate
                if table['bans'][j] == championId:
                    ban_cnt += 1

                if table['teamPosition'][j] == teamposit_list[i] and table['championName'][j] == cham:

                    championName = table['championName'][j]
                    teamPosition = table['teamPosition'][j]
                    ka_cnt += table['kills'][j]
                    ka_cnt += table['assists'][j]
                    kda_list.append(round(ka_cnt / table['kills'][j]),2)
                    pick_cnt += 1

                    if table['win'][j] == 1:
                        win_cnt += 1



            # 모든 데이터에서 탐색이 끝나고 챔피언 별 승률, 픽율, 밴률 계산하기
            print("total_cnt,win_cnt,ban_cnt,pick_cnt: ",total_cnt,win_cnt,ban_cnt,pick_cnt)
            win_rate = round(win_cnt/pick_cnt,2)
            ban_rate = round(ban_cnt/total_cnt, 2)
            pick_rate = round(pick_cnt/total_cnt, 2)
            av_kda = round(sum(kda_list)/pick_cnt,2)

            pri_perk1,pri_perk2,pri_perk3,pri_perk4,pri_style = cal_prim_lune(table,str(cham))
            sub_perk1, sub_perk2, sub_style = cal_sub_lune(table,str(cham))
            deffence, flex, offence = cal_ability(table,str(cham))

            (spell1_1,spell1_2,spell1_cnt, spell1_rate,spell1_win,
             spell2_1, spell2_2,spell2_cnt, spell2_rate,spell2_win) = cal_spell(table,str(cham))

            data_list = [lowCase,championName, championId, teamPosition,
                         total_cnt, win_cnt,ban_cnt,pick_cnt,
                         win_rate, ban_rate, pick_rate,av_kda,

                         pri_perk1,pri_perk2,pri_perk3,pri_perk4,pri_style,
                         sub_perk1,sub_perk2,sub_style,
                         deffence, flex, offence,
                         spell1_1, spell1_2, spell1_cnt, spell1_rate, spell1_win,
                         spell2_1, spell2_2, spell2_cnt, spell2_rate, spell2_win]
            print(data_list)

            n = len(cham_df)
            cham_df.loc[n] = data_list
    cham_df.to_sql(name=str(save_name), con=conn_cham, if_exists='append', index=False)
def collect_aram(lowCase,table,save_name):
    chamID_hash = {}


    # 해당 티어에서 치룬 모든 게임 수: total_cnt
    total_cnt = len(list(set(table['matchID'])))

    # 저장을 위해 chaminfo에 저장된 테이블 스키마 df로 불러오기
    cham_df = select_db(str(save_name),conn_cham)

    # 챔피언 이름 모으기
    cham_list = list(set(table['championName']))

    # chamID_hash = {챔피언 이름: 챔피언 ID} 매핑해주는 해시 for ban픽 챔피언 서치
    for i in range(len(table)):
        if table['championName'][i] not in chamID_hash:
            chamID_hash[str(table['championName'][i])] = table['championId'][i]

    for cham in cham_list:          # appear champions iterate
        win_cnt = 0
        ban_cnt = 0
        pick_cnt = 0
        championId = chamID_hash[cham]

        for i in range(len(table)): # all table data iterate


            if table['championName'][i] == cham:
                pick_cnt += 1

                if table['win'][i] == 1:
                    win_cnt += 1

            if table['bans'][i] == championId:
                ban_cnt += 1

                # 모든 데이터에서 탐색이 끝나고 챔피언 별 승률, 픽율, 밴률 계산하기
        print("total_cnt,win_cnt,ban_cnt,pick_cnt: ", total_cnt, win_cnt, ban_cnt, pick_cnt)
        win_rate = round(win_cnt / pick_cnt, 2)
        ban_rate = round(ban_cnt / total_cnt, 2)
        pick_rate = round(pick_cnt / total_cnt, 2)

        data_list = [lowCase, cham, championId,"ARAM",
                     total_cnt, win_rate, ban_rate,pick_rate]  # core, shoes, first_pur, prim_perk, prim_stlye etc
        print(data_list)

        n = len(cham_df)
        cham_df.loc[n] = data_list

    cham_df.to_sql(name=str(save_name), con=conn_cham, if_exists='append', index=False)
def iterate_perTier(lowCase):  #  collect_classic()보다 먼저 실행되는 함수


    # DB속 테이블 불러와 변수에 저장하기
    for j in range(len(final_tables)): # iterate all gameinfo tables
        tableName = final_tables[j][0]

        if tableName[:len(lowCase)] == lowCase:
            # print(tableName[:len(lowCase[i])],"==",lowCase[i])

            if tableName[-1:] == 'm':       # 칼바람 정보 테이블
                aram_table = select_db(tableName, conn_gam)
                print(tableName,"정보를 불러와 aram_table 변수에 할당했습니다.")
            if tableName[-1:] == 'n':        # 승자 정보 테이블
                win_table = select_db(tableName,conn_gam)
                print(tableName, "정보를 불러와 win_table 변수에 할당했습니다.")
            if tableName[-1:] == 'e':       # 패자 정보 테이블
                lose_table = select_db(tableName, conn_gam)
                print(tableName, "정보를 불러와 lose_table 변수에 할당했습니다.")


    # outer join 수행
    classic_table = pd.merge(win_table,lose_table,how='outer')
    # print(classic_table.head())
    # print(aram_table.head())
    # print(lowCase, "티어의 win_table 길이: ", len(win_table))
    # print(lowCase, "티어의 lose_table 길이: ", len(lose_table))
    # print(lowCase, "티어의 classic_table 길이: ", len(classic_table))

    print(lowCase,"티어의 classic 게임에 대한 챔피언 정보를 저장합니다.")
    collect_classic(lowCase=lowCase, table= classic_table,save_name = str(lowCase)+"_cham")
    print(lowCase, "티어의 classic 게임에 대한 챔피언 정보를 저장합니다.")
    collect_aram(lowCase=lowCase, table=aram_table, save_name = str(lowCase)+"_archam")
def exe_prepro_cham():

    # 데이터 불러오기# 1. MySQL에서 최종 테이블 불러오기
    final_tables = show_tables(engine_gam)
    # print(final_tables)

    # chaminfo DB의 모든 테이블 데이터 날리고 스키마만 남기기
    trun_tables(engine_name=engine_cham)

    # 티어별 데이터 dataframe으로 불러와 저장하기
    for t in range(len(lowCase)):  # iterate all tiers
        # 티어별 gameinfo테이블을 불러오기 위한 함수
        iterate_perTier(lowCase=lowCase[t])
        print(lowCase[t],"티어의 모든 champion 정보를 저장했습니다.============================================================")

exe_prepro_cham()