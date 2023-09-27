import pandas as pd
from setting import *
from db_functions import *
import pprint

# MySQL에서 최종 테이블 불러오기
final_tables =show_tables(engine_gam)
# print(final_tables)

chall_win = select_db(final_tables[5][0],conn_gam)
# print("chall_win 길이: ",len(chall_win))
# pprint.pprint(chall_win.head())
chall_lose = select_db(final_tables[4][0],conn_gam)
# pprint.pprint(chall_lose.tail())
# print("chall_lose 길이: ", len(chall_lose))


# outer join 수행
chall_classic = pd.merge(chall_win,chall_lose,how='outer')
# pprint.pprint(chall_classic)
# pprint.pprint(chall_classic.tail())
# print("chall_classic 길이: ", len(chall_classic))

# chall_classic.to_sql(name='chall_classic', con=conn_cham, if_exists='replace', index=False)
# # pprint.pprint(chall_lose)
# pprint.pprint(chall_lose.columns)

posit_list = []
chamName_list = []
chamID_list = []
chamID_hash = {}
for i in range(len(chall_classic)):
    if chall_classic['championName'][i] not in chamID_hash:
        chamID_hash[str(chall_classic['championName'][i])] = chall_classic['championId'][i]

    posit_list.append(chall_classic['teamPosition'][i])
    chamName_list.append(chall_classic['championName'][i])
    chamID_list.append(chall_classic['championId'][i])


# posit_list = list(set(posit_list))
# print("중복 제거 한 팀포지션: ", list(set(posit_list)))
# print("중복 제거 한 챔피언의 모든 이름: ", len(list(set(chamName_list))))
# print("중복 제거 한 챔피언의 모든 아이디: ", len(list(set(chamID_list))))
# print("챔피언 이름과 아이디를 매핑시킨 해시: ", chamID_hash)


def iterate_posit():
    # 해당 티어에서 치룬 모든 게임: total_cnt
    total_cnt = len(list(set(chall_classic['matchId'])))

    # 저장된 스키마 불러오기
    chall_cham = select_db('chall_cham',conn_cham)

    data_list = []  # 임시 저장을 위한 리스트
    for i in range(len(posit_list)):  # teamposition iterate  # len(posit_list)
        print("조회할 팀포지션은 ",posit_list[i],"입니다 --------------------------------------")
        posit_cham = {}

        for j in range(len(chall_classic)):  # all data iterate for collect chamName per position
            if chall_classic['teamPosition'][j] == posit_list[i]:
                chamName_key = str(chall_classic['championName'][j])
                posit_cham[chamName_key] = 0


        # print("posit_cham: ",posit_cham)
        for cham in posit_cham:  # chamName per position iterate
            win_cnt = 0
            ban_cnt = 0
            pick_cnt = 0
            for j in range(len(chall_classic)):  # all data iterate
                championId = chamID_hash[cham]

                if chall_classic['teamPosition'][j] == posit_list[i] and chall_classic['championName'][j] == cham:
                    championName = chall_classic['championName'][j]
                    championId = chamID_hash[cham]
                    teamPosition = chall_classic['teamPosition'][j]
                    pick_cnt += 1

                    if chall_classic['win'][j] == 1:
                        win_cnt += 1

                if chall_classic['bans'][j] == championId:
                    ban_cnt += 1


            data_list = [championName, championId, teamPosition,
                         total_cnt, win_cnt, ban_cnt, pick_cnt]
            print(data_list)

            n = len(chall_cham)
            chall_cham.loc[n] = data_list


    pprint.pprint(chall_cham)
    # chall_cham.to_sql(name='chall_cham', con=conn_cham, if_exists='replace', index=False)
iterate_posit()

# 사용하지 않는 함수임
def iterate_chamName():
    data_list = []  # 임시 저장을 위한 리스트
    for i in range(len(chamName_list)):  # teamposition iterate  # len(posit_list)
        win_cnt = 0
        ban_cnt = 0
        pick_cnt = 0
        teamPosition = {}
        for j in range(len(chall_classic)):  # all data iterate
            if chall_classic['championName'][j] == chamName_list[i]:
                pick_cnt += 1
                # teamPosition 해시값에 넣어주기 - 챔피언당 하나의 teamPosition만 가지는 게 아닐 수도 있으니까
                if chall_classic['teamPosition'][j] not in teamPosition:
                    teamPosition[str(chall_classic['teamPosition'][j])] = 1
                else:
                    teamPosition[str(chall_classic['teamPosition'][j])] +=1
            if chall_classic['championName'][j] == chamName_list[i] and chall_classic['win'][j] == 1:  # 승리한 판
                win_cnt += 1
            if chall_classic['bans'][j] == chamID_hash[str(chamName_list[i])]:  # bans 개수
                ban_cnt += 1

        data_list = [chamName_list[i],chamID_hash[str(chamName_list[i])],teamPosition,
                     total_cnt,win_cnt,ban_cnt,pick_cnt]


        pprint.pprint(data_list)
