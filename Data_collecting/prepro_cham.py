import pandas as pd

from setting import *
from db_functions import *
from prepro_cham_function import *

# table_list = show_tables(engine_gam)
# aram_df = select_db(table_list[0][0],conn_name=conn_gam)

def collect_classic(lowCase,table,save_name):
    """iterate_perTier()안에 들어가는 전처리 함수1"""
    chamID_hash = {}

    # 연산이 돌아가기 전 존재하는 데이터이면 연산 x continue 하기 위해 이미 저장된 데이터를 불러온다
    saved_table = select_db(table_name=str(save_name), conn_name=conn_cham)


    # # chamID_hash = {챔피언 이름: 챔피언 ID} 매핑해주는 해시 for ban픽 챔피언 서치
    for i in range(len(table)):
        if table['championName'][i] not in chamID_hash:
            chamID_hash[str(table['championName'][i])] = table['championId'][i]
    print("chamID_hash: ",chamID_hash)

    match_list = []
    match_cnt = 0
    # 밴픽 계산을 위한 match_cnt 계산으로 해당 table의 전체 판수 계산: mat_cnt
    for i in range(len(table)):
        if table['matchID'][i] not in match_list:
            match_list.append(table['matchID'][i])
    match_list = list(set(match_list))
    match_cnt = len(match_list)



    # 어떤 포지션에 해당하는 모든 챔피언을 저장하기 위한 연산 - dictionary로 저장
    # posit_hash = {'포지션명': [어떤 포지션에 해당하는 unique 챔피언 이름들]}
    posit_hash = {}
    for i in range(len(teamposit_list)):
        # print("조회할 팀포지션은 ", teamposit_list[i], "입니다 --------------------------------------")
        posit_cham = []
        for j in range(len(table)):  # all data iterate for collect chamName per position
            if table['teamPosition'][j] == teamposit_list[i]:
                if table['teamPosition'][j] not in posit_cham:
                    posit_cham.append(str(table['championName'][j]))
        # print("중복 제거 전: ", len(posit_cham))     # bro 기준  약 5600
        posit_cham = list(set(posit_cham))           # 챔피언 이름 중복 제거
        # print("중복 제거 후: ", len(posit_cham))     # bro 기준  약 140개
        posit_hash[str(teamposit_list[i])] = posit_cham

    print("posit_hash: ",posit_hash)

    for position in teamposit_list:
        print("조회할 포지션은: " ,lowCase,"의", position,"--------------------------------------------------------------------------------------------------------------------")
        print("총",len(posit_hash[str(position)]) ,"명의 챔피언에 대해 연산을 시작합니다.")
        for chamName in posit_hash[str(position)]:  # chamName per position iterate
            print("조회할 챔피언은: ",chamName)

            # 중복 체크하는 변수 = 1이면 이미 테이블에 저장된 정보/ 0이면 중복x
            is_exist =0

            # 이미 saved_table에 저장된 정보인지 확인하는 loop
            for c in range(len(saved_table)):
                if saved_table['championName'][c] ==  chamName and saved_table['teamPosition'][c] == position:
                    is_exist += 1
                    print("포지션",position,"로 사용된",chamName,"은 ",save_name,"에 이미 저장된 정보입니다.")
                    continue
            if is_exist == 1:
                continue

            ban_cnt = 0
            championId = chamID_hash[str(chamName)]
            cham_df = pd.DataFrame(columns=columns_list)



            # 해당 chamName에 해당하는 rows들을 cham_df에 올려놓고 연산 시작
            for i in range(len(table)):
                # chamName 벤된 count 계산
                if table['bans'][i] == championId:
                    ban_cnt += 1

                # cham_df chamName에 해당하는 모든 데이터 올리기
                if table['championName'][i] == chamName and table['teamPosition'][i] == position and table['gameMode'][i]=='CLASSIC':
                    n = len(cham_df)
                    cham_df.loc[n] = table.loc[i]

            cham_cnt = len(cham_df)     # 챔피언의 등장 횟수
            # print("해당 티어의 전체 치룬 경기 수는 ", match_cnt)
            # print("해당 챔피언의 밴픽 수는: ",  ban_cnt)

            # 챔피언 등장이 없으면 다음 챔피언으로 넘어가기
            if cham_cnt == 0:
                print(lowCase,"티어에서", chamName,"이 픽된 해당하는 게임 정보가 없습니다. 다음 챔피언 정보 연산을 위해 넘어갑니다.")
                continue

            # print("cham_df의 길이는: ", len(cham_df))
            # print(cham_df)


            # 밴율 = 밴된 경기 수 / 전체 경기 수
            ban_rate = round(ban_cnt/match_cnt,4)
            # print("밴율은: ", ban_rate)


            # 픽률 = 픽 경기 수/ 전체 경기 수
            pick_rate = round(cham_cnt/match_cnt,4)
            # print("픽률은: ",pick_rate)

            # 1. 승픽밴
            win_cnt, win_rate, av_kda = cal_base(cham_df=cham_df,cham_cnt=cham_cnt)

            # # 2. 룬세팅(메인,서브)
            pri_perk1,pri_perk2,pri_perk3,pri_perk4,pri_style = cal_prim_lune(cham_df)

            sub_perk1, sub_perk2, sub_style = cal_sub_lune(cham_df)

            # 3. 능력치 파편
            deffence, flex, offence = cal_ability(cham_df)

            # 4. 소환사 주문
            (spell1_1,spell1_2,spell1_cnt, spell1_rate,spell1_win,
             spell2_1, spell2_2,spell2_cnt, spell2_rate,spell2_win) = cal_spell(cham_df,cham_cnt)

            # 5. 스킬 빌드
            (skill_build1,skill_build2,skill_build3,
             skill_cnt,skill_rate,skill_win) = cal_skilltree(cham_df,cham_cnt)

            # 6. 아이템 빌드
            (item_set1_1, item_set1_2, item_set1_3,item_set1_4, item_set1_5, item_set1_6, item_set1_7, item_set1_8,
             item_set1_cnt, item_set1_rate, item_set1_win,

             item_set2_1, item_set2_2, item_set2_3,item_set2_4, item_set2_5, item_set2_6, item_set2_7, item_set2_8,
             item_set2_cnt, item_set2_rate, item_set2_win) = cal_item_build(cham_df,cham_cnt)

            # 7. 신발 빌드
            (shoe1,shoes1_cnt,shoes1_rate,shoes1_win,
             shoe2,shoes2_cnt,shoes2_rate,shoes2_win) = cal_shoes(cham_df,cham_cnt)

            # 8. 코어 빌드
            (core1_1, core1_2, core1_3, core1_4, core1_5, core1_6,
              core1_cnt,core1_rate,core1_win,

              core2_1, core2_2, core2_3, core2_4, core2_5, core2_6,
              core2_cnt,core2_rate,core2_win,

              core3_1, core3_2, core3_3, core3_4, core3_5, core3_6,
              core3_cnt,core3_rate,core3_win)=cal_corebuild(cham_df,cham_cnt)




            # df에 저장을 위한 리스트 insert의 value 부분
            data_list = [lowCase,chamName, championId, position,

                         match_cnt,win_cnt,ban_cnt,cham_cnt,
                         win_rate, ban_rate, pick_rate,av_kda,

                         pri_perk1, pri_perk2, pri_perk3, pri_perk4, pri_style,
                         sub_perk1, sub_perk2, sub_style,
                         deffence, flex, offence,

                         spell1_1, spell1_2, spell1_cnt, spell1_rate, spell1_win,
                         spell2_1, spell2_2, spell2_cnt, spell2_rate, spell2_win,

                         skill_build1, skill_build2, skill_build3,
                         skill_cnt, skill_rate, skill_win,

                         item_set1_1, item_set1_2, item_set1_3, item_set1_4,
                         item_set1_5, item_set1_6, item_set1_7, item_set1_8,
                         item_set1_cnt, item_set1_rate, item_set1_win,

                         item_set2_1, item_set2_2, item_set2_3, item_set2_4,
                         item_set2_5, item_set2_6, item_set2_7,item_set2_8,
                         item_set2_cnt, item_set2_rate, item_set2_win,

                         shoe1, shoes1_cnt, shoes1_rate, shoes1_win,
                         shoe2, shoes2_cnt, shoes2_rate, shoes2_win,

                         core1_1, core1_2, core1_3, core1_4, core1_5, core1_6,
                         core1_cnt, core1_rate, core1_win,

                         core2_1, core2_2, core2_3, core2_4, core2_5, core2_6,
                         core2_cnt, core2_rate, core2_win,

                         core3_1, core3_2, core3_3, core3_4, core3_5, core3_6,
                         core3_cnt, core3_rate, core3_win]

            # print(data_list)

            # table_schema df에 데이터 임시저장
            table_schema = pd.DataFrame(columns=cham_col_list)
            table_schema.loc[0] = data_list

            # 모든 연산이 끝나면 임시저장한 df를 table로 저장
            table_schema.to_sql(name=str(save_name), con=conn_cham, if_exists='append', index=False)
            conn_cham.commit()
            # print("insert 쿼리가 실행되었습니다.")
# collect_classic('bro',table=classic_df,save_name='bro_cham')
def collect_aram(table,save_name):
    """iterate_perTier()안에 들어가는 전처리 함수2"""

    # 연산이 돌아가기 전 존재하는 데이터이면 연산 x continue 하기 위해 이미 저장된 데이터를 불러온다
    saved_table = select_db(table_name=str(save_name), conn_name=conn_cham)
    
    # 티어에서 중복없이 치뤄진 게임의 개수
    match_list = []
    match_cnt = 0
    # 밴픽 계산을 위한 match_cnt 계산으로 해당 table의 전체 판수 계산: mat_cnt
    for i in range(len(table)):
        if table['matchID'][i] not in match_list:
            match_list.append(table['matchID'][i])
    match_list = list(set(match_list))
    match_cnt = len(match_list)
    
    # 중복 없는 챔피언 이름의 경우의 수 담아주기
    aram_cham_list = []
    for i in range(len(table)):
        if table['championName'][i] not in aram_cham_list:
            aram_cham_list.append(table['championName'][i])

    print("조회할 챔피언은", len(aram_cham_list),"명입니다.")

    for chamName in aram_cham_list:     # champion name iterate
        print("조회할 챔피언은: ", chamName)


        # 중복 체크하는 변수 = 1이면 이미 테이블에 저장된 정보/ 0이면 중복x
        is_exist = 0
        # 이미 saved_table에 저장된 정보인지 확인하는 loop
        for c in range(len(saved_table)):
            if saved_table['championName'][c] == chamName:
                is_exist += 1
                print(chamName, "은 ", save_name, "에 이미 저장된 정보입니다.")
                continue
        if is_exist == 1:
            print(chamName,"은 이미 저장 완료된 챔피언입니다.")
            continue


        # cham_df chamName에 해당하는 모든 데이터 올리기
        cham_df = pd.DataFrame(columns=columns_list)
        for i in range(len(table)):
            if table['championName'][i] == chamName:
                n = len(cham_df)
                cham_df.loc[n] = table.loc[i]

        cham_cnt = len(cham_df)  # 챔피언이 전체 게임에서 등장한 횟수

        # 챔피언 등장이 없으면 다음 챔피언으로 넘어가기
        if cham_cnt == 0:
            print(chamName, "이 픽된 해당하는 게임 정보가 없습니다. 다음 챔피언 정보 연산을 위해 넘어갑니다.")
            continue

        pick_rate = round(cham_cnt /match_cnt, 4)
        # print("픽률은: ",pick_rate)

        # 1. 승픽밴
        win_cnt, win_rate, av_kda = cal_base(cham_df=cham_df, cham_cnt=cham_cnt)

        # # 2. 룬세팅(메인,서브)
        pri_perk1, pri_perk2, pri_perk3, pri_perk4, pri_style = cal_prim_lune(cham_df)

        sub_perk1, sub_perk2, sub_style = cal_sub_lune(cham_df)

        # 3. 능력치 파편
        deffence, flex, offence = cal_ability(cham_df)

        # 4. 소환사 주문
        (spell1_1, spell1_2, spell1_cnt, spell1_rate, spell1_win,
        spell2_1, spell2_2, spell2_cnt, spell2_rate, spell2_win) = cal_spell(cham_df, cham_cnt)

        # 5. 스킬 빌드
        (skill_build1, skill_build2, skill_build3,
             skill_cnt, skill_rate, skill_win) = cal_skilltree(cham_df, cham_cnt)

        # 6. 아이템 빌드
        (item_set1_1, item_set1_2, item_set1_3, item_set1_4, item_set1_5, item_set1_6, item_set1_7, item_set1_8,
             item_set1_cnt, item_set1_rate, item_set1_win,

             item_set2_1, item_set2_2, item_set2_3, item_set2_4, item_set2_5, item_set2_6, item_set2_7, item_set2_8,
             item_set2_cnt, item_set2_rate, item_set2_win) = cal_item_build(cham_df, cham_cnt)

            # 7. 신발 빌드
        (shoe1, shoes1_cnt, shoes1_rate, shoes1_win,
             shoe2, shoes2_cnt, shoes2_rate, shoes2_win) = cal_shoes(cham_df, cham_cnt)

            # 8. 코어 빌드
        (core1_1, core1_2, core1_3, core1_4, core1_5, core1_6,
             core1_cnt, core1_rate, core1_win,

             core2_1, core2_2, core2_3, core2_4, core2_5, core2_6,
             core2_cnt, core2_rate, core2_win,

             core3_1, core3_2, core3_3, core3_4, core3_5, core3_6,
             core3_cnt, core3_rate, core3_win) = cal_corebuild(cham_df, cham_cnt)

            # df에 저장을 위한 리스트 insert의 value 부분
        data_list = [None, chamName, None, None,

                         match_cnt, win_cnt, None, cham_cnt,
                         win_rate, None, pick_rate, av_kda,

                         pri_perk1, pri_perk2, pri_perk3, pri_perk4, pri_style,
                         sub_perk1, sub_perk2, sub_style,
                         deffence, flex, offence,

                         spell1_1, spell1_2, spell1_cnt, spell1_rate, spell1_win,
                         spell2_1, spell2_2, spell2_cnt, spell2_rate, spell2_win,

                         skill_build1, skill_build2, skill_build3,
                         skill_cnt, skill_rate, skill_win,

                         item_set1_1, item_set1_2, item_set1_3, item_set1_4,
                         item_set1_5, item_set1_6, item_set1_7, item_set1_8,
                         item_set1_cnt, item_set1_rate, item_set1_win,

                         item_set2_1, item_set2_2, item_set2_3, item_set2_4,
                         item_set2_5, item_set2_6, item_set2_7, item_set2_8,
                         item_set2_cnt, item_set2_rate, item_set2_win,

                         shoe1, shoes1_cnt, shoes1_rate, shoes1_win,
                         shoe2, shoes2_cnt, shoes2_rate, shoes2_win,

                         core1_1, core1_2, core1_3, core1_4, core1_5, core1_6,
                         core1_cnt, core1_rate, core1_win,

                         core2_1, core2_2, core2_3, core2_4, core2_5, core2_6,
                         core2_cnt, core2_rate, core2_win,

                         core3_1, core3_2, core3_3, core3_4, core3_5, core3_6,
                         core3_cnt, core3_rate, core3_win]

        # print(data_list)


        # table_schema df에 데이터 임시저장
        table_schema = pd.DataFrame(columns=cham_col_list)
        table_schema.loc[0] = data_list
        # print(table_schema)

        # 모든 연산이 끝나면 임시저장한 df를 table로 저장
        table_schema.to_sql(name=str(save_name), con=conn_cham, if_exists='append', index=False)
        saved_table = select_db(table_name=str(save_name), conn_name=conn_cham)
        conn_cham.commit()
        # print(saved_table)
        # print("insert 쿼리가 실행되었습니다.")
        # break

def iterate_perTier(lowCase,final_tables):  #  collect_classic()보다 먼저 실행되는 함수
    # DB속 테이블 불러와 변수에 저장하기
    for j in range(len(final_tables)): # iterate all gameinfo tables
        tableName = final_tables[j][0]

        if tableName[:len(lowCase)] == lowCase:
            if tableName[-1:] == 'n':        # 승자 정보 테이블
                win_table = select_db(tableName,conn_gam)
                print(tableName, "정보를 불러와 win_table 변수에 할당했습니다.")
            if tableName[-1:] == 'e':       # 패자 정보 테이블
                lose_table = select_db(tableName, conn_gam)
                print(tableName, "정보를 불러와 lose_table 변수에 할당했습니다.")

    # outer join 수행
    classic_table = pd.merge(win_table,lose_table,how='outer')

    print(lowCase,"티어의 classic 게임에 대한 챔피언 정보를 저장합니다.=============================================================================")
    collect_classic(lowCase=lowCase, table= classic_table,save_name = str(lowCase)+"_cham")


def exe_prepro_cham():
    # 데이터 불러오기
    # 1. MySQL에서 최종 테이블 불러오기
    final_tables = show_tables(engine_gam)

    # chaminfo DB의 모든 테이블 데이터 날리고 스키마만 남기기
    # trun_tables(engine_name=engine_cham)


    # classic 게임: 티어별 데이터 dataframe으로 불러와 저장하기
    for t in range(len(lowCase)):  # iterate all tiers
        # 티어별 gameinfo테이블을 불러오기 위한 함수
        iterate_perTier(lowCase=lowCase[t],final_tables=final_tables)
        print(lowCase[t],"티어의 모든 classic게임의 champion 정보를 저장했습니다.============================================================")

    # Aram 게임: 티어별 데이터 dataframe으로 불러와 저장하기
    merge_df = pd.DataFrame(columns=columns_list)
    for i in range(len(final_tables)):
        tableName = final_tables[i][0]

        if tableName[-1:] == 'm':  # 칼바람 정보 테이블
            aram_table = select_db(tableName, conn_gam)
            # print(tableName,"의 길이: ",len(aram_table))
            merge_df = pd.merge(aram_table, merge_df, how='outer')
            print(tableName, "의 정보를 merge_df와 합쳤습니다.")
    print("merge_df의 데이터 개수는: ", len(merge_df))

    # print(aram 게임에 대한 챔피언 정보를 저장합니다.=============================================================================")
    collect_aram(table=merge_df, save_name="total_archam")

# trun_tables(engine_name=engine_cham)
# exe_prepro_cham()