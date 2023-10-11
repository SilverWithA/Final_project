from db_functions import *
from setting import *
import pandas as pd

# 테스트 데이터
table_list = show_tables(engine_gam)
# print(table_list)
aram_df = select_db(table_list[0][0],conn_name=conn_gam)
lose_df = select_db(table_list[1][0],conn_name=conn_gam)
win_df = select_db(table_list[2][0],conn_name=conn_gam)

# chall_classic = pd.merge# print(chall_win.head())
classic_df = pd.merge(lose_df,win_df, how='outer')

cham_list = ['LeeSin','Zyra']
chamID_hash = {}
test_cham_df = pd.DataFrame(columns=columns_list)

for i in range(len(classic_df)):
    if classic_df['championName'][i] not in chamID_hash:
        chamID_hash[str(classic_df['championName'][i])] = classic_df['championId'][i]

    if classic_df['championName'][i] == 'Aphelios':
        n = len(test_cham_df)
        test_cham_df.loc[n] = classic_df.loc[i]

# 1 승률, kda 구하기(메타점수)
def cal_base(cham_df, cham_cnt):
    win_cnt = 0
    kda_list = []
    kda_null = 0

    for j in range(len(cham_df)):
        # 승리한 게임 count
        if cham_df['win'][j] == True:
               win_cnt += 1

        # kda 평균값 계산을 위해 각 참가자의 kda를 kda_list에 값 쌓아주기
        ka_cnt = (int(cham_df['kills'][j]) + int(cham_df['assists'][j]))

        if int(cham_df['deaths'][j]) != 0:
            kda = round(ka_cnt / int(cham_df['deaths'][j]), 2)
            kda_list.append(kda)
        else:
            kda_null += 1


    # print("win_cnt,len(kda_list): ",win_cnt,len(kda_list))
    if (cham_cnt-kda_null) == 0:
        print("cham_cnt: ",cham_cnt)
        print("kda_null: ", kda_null)
        av_kda = None
    else:
        av_kda = round(sum(kda_list)/(cham_cnt-kda_null),2)
    win_rate = round(win_cnt/cham_cnt,4)

    result = [win_cnt,win_rate,av_kda]
    return result
# print(cal_base(test_cham_df,cham_cnt=len(test_cham_df)))

# 2. 룬 계산하기 - 메인룬
def cal_prim_lune(cham_df):
    all_lune = []
    
    # lune세팅의 모든 경우의 수 찾기
    for j in range(len(cham_df)):
        temp = [cham_df['prim1_perk'][j],cham_df['prim2_perk'][j],cham_df['prim3_perk'][j],cham_df['prim4_perk'][j],cham_df['prim_style'][j]]
        if temp not in all_lune and temp != ['0', '0', '0', '0', '0']:
            all_lune.append(temp)

    # print("해당 챔피언의 모든 주 룬 세팅의 모든 경우의 수: ", all_lune)
    # print("그 개수는: ", len(all_lune))

    # 조합의 출현 횟수 count를 위한 hash 만들기
    # {all_lune에서의 인덱스: all_lune의 조합의 값}
    combin_index = [str(i) for i in range(len(all_lune))]
    primlune_hash = dict(zip(combin_index, all_lune))
    # print("primlune_hash: ", primlune_hash)

    primlune_cnt = dict(zip(combin_index, [0]* len(all_lune)))
    # print("primlune_cnt: ",primlune_cnt)

    # 주 룬세팅 조합의 개수 count 연산해주기
    for i in range(len(cham_df)):
        temp2 = [cham_df['prim1_perk'][i], cham_df['prim2_perk'][i], cham_df['prim3_perk'][i],  cham_df['prim4_perk'][i], cham_df['prim_style'][i]]

        for conbin in primlune_hash.values():
            if temp2 == conbin:
                # print("temp2: ",temp2)
                # print("index: ",all_lune.index(temp2))
                primlune_cnt[str(all_lune.index(temp2))] += 1

    primlune_cnt = dict(sorted(primlune_cnt.items(), key=lambda x:x[1], reverse=True))
    # print("정렬이 끝난 primlune_cnt: ",primlune_cnt)
    # a,b,c,d,e = primlune_hash[str(list(primlune_cnt)[0])]  # 1순위 조합만 추출
    result = primlune_hash[str(list(primlune_cnt)[0])]


    return result
# print(cal_prim_lune(test_cham_df))

# 2-(1). 룬 계산하기 - 서브룬
def cal_sub_lune(cham_df):
    all_sublune = []

    # 모든 경우의 수 저장
    for i in range(len(cham_df)):
        temp = [cham_df['sub1_perk'][i],cham_df['sub2_perk'][i],cham_df['sub_style'][i]]

        if temp not in all_sublune and temp != ['0', '0', '0']:
            all_sublune.append(temp)

    # print("all_sublune: ",all_sublune)
    # print("모든 경우의 수는: ", len(all_sublune))

    # count를 위한 해시 생성
    # sublune_cnt = {all_sublune의 index:all_sublune의 값}
    all_index = [str(i) for i in range(len(all_sublune))]
    sublune_hash = dict(zip(all_index,all_sublune))
    # print("sublune_hash: ",sublune_hash)

    # cnt올려주기 위한 hash 생성
    sublune_cnt = dict(zip(all_index, [0]* len(all_sublune)))

    for i in range(len(cham_df)):
        temp2 = [cham_df['sub1_perk'][i],cham_df['sub2_perk'][i],cham_df['sub_style'][i]]

        for combin in sublune_hash.values():
            if temp2 == combin:
                sublune_cnt[str(all_sublune.index(temp2))] += 1

    sublune_cnt = dict(sorted(sublune_cnt.items(), key=lambda x:x[1],reverse=True))
    # print("sublune_cnt: ",sublune_cnt)
    final_sublune =sublune_hash[str(list(sublune_cnt)[0])]      # 1순위 조합의 index
    # print(final_sublune)
    return final_sublune
# print(cal_sub_lune(test_cham_df))

# 3. 능력치 파편
def cal_ability(cham_df):
    abil_combin = []

    # 능력치 파편의 모든 조합 경우의 수 찾기
    for i in range(len(cham_df)):  # all table data iterate
        temp1 = [cham_df['defense'][i],cham_df['flex'][i],cham_df['offense'][i]]

        if temp1 not in abil_combin:
            abil_combin.append(temp1)

    # print("능력치 파편의 모든 경우의 수는: ", len(abil_combin),"가지 입니다.")
    keys = [str(i) for i in range(len(abil_combin))]

    # {index: abil_combin} = {어떤 경우의 수의 abil_combin 인덱스: 경우의 수 리스트}
    abil_hash = dict(zip(keys,abil_combin))
    # print("abil_combin의 인덱스: 경우의 수 = abil_hash: ", abil_hash)


    # 어떤 조합의 출현빈도  cnt 를 계산하기 위한 code
    cnt_ability = dict(zip(keys, [0] * len(abil_combin)))

    for i in range(len(cham_df)):
        temp2 = [cham_df['defense'][i],cham_df['flex'][i], cham_df['offense'][i]]
        for combin in abil_combin:
            if temp2 == combin:
                # print("abil_combin에서 temp2의 인덱스: ", abil_combin.index(temp2))
                cnt_ability[str(abil_combin.index(temp2))] += 1

    # {index:count} 오름차순으로 정리
    cnt_ability = dict(sorted(cnt_ability.items(), key=lambda x:x[1], reverse=True))
    # print("해당 챔피언의 모든 능력치 파편의 경우의 수 및 개수: ",cnt_ability)


    # 가장 경우의 수가 많은 능력치 파편을 저장을 위한 리스트에 넣어주기
    index_order = list(cnt_ability)   # cnt 내림 차순으로 인덱스의 순서

    return abil_hash[index_order[0]]

# print(cal_ability(test_cham_df))
# print(cal_ability(classic_df,'Zyra'))

# 4. 소환사 주문
def cal_spell(cham_df,cham_cnt):
    spell_combin = []

    # 모든 조합 경우의 수 찾기
    for i in range(len(cham_df)):
        temp = [cham_df['summoner1Id'][i],cham_df['summoner2Id'][i]]
        if temp not in spell_combin:
            spell_combin.append(temp)

    # print("능력치 파편의 모든 경우의 수는: ", len(spell_combin), "가지 입니다.")
    # print("spell_combin: ",spell_combin)
    keys = [str(i) for i in range(len(spell_combin))]

    # {index: abil_combin} = {어떤 경우의 수의 abil_combin 인덱스: 경우의 수 리스트}
    spell_hash = dict(zip(keys, spell_combin))
    # print("spell_hash의 인덱스: 경우의 수 = spell_hash: ", spell_hash)


    # 경우의 수 별 count 세기
    # 어떤 조합의 출현빈도  cnt 를 계산하기 위한 code
    spell_cnt = dict(zip(keys, [0] * len(spell_combin)))

    for i in range(len(cham_df)):
        temp2 = [cham_df['summoner1Id'][i], cham_df['summoner2Id'][i]]

        for combin in spell_combin:
            if temp2 == combin:
                # print("abil_combin에서 temp2의 인덱스: ", abil_combin.index(temp2))
                spell_cnt[str(spell_combin.index(temp2))] += 1

    # {index:count} 오름차순으로 정리
    spell_cnt = dict(sorted(spell_cnt.items(), key=lambda x: x[1], reverse=True))
    # print("해당 챔피언의 모든 능력치 파편의 경우의 수 및 개수: ",spell_cnt)

    # 가장 경우의 수가 많은 능력치 파편을 저장을 위한 리스트에 넣어주기
    index_order = list(spell_cnt)  # cnt 내림 차순으로 인덱스의 순서
    # print("index_order: ",index_order)
    # print("1순위 조합: ", spell_hash[index_order[0]])  # 1순위 조합
    # print("2순위 조합: ", spell_hash[index_order[1]])  # 2순위 조합
    if len(index_order) >= 2:
        spell1_1, spell1_2 = spell_hash[str(index_order[0])]  # 1순위 조합
        spell2_1, spell2_2 = spell_hash[str(index_order[1])]  # 2순위 조합
    elif len(index_order) == 1:     # 1순위 조합만 있음
        spell1_1, spell1_2 = spell_hash[str(index_order[0])]  # 1순위 조합
        spell2_1, spell2_2 = [None] * 2
    else:
        return [None] * 10



    spell1_cnt = 0
    spell2_cnt = 0
    spell1_win = 0
    spell2_win = 0

    for i in range(len(cham_df)):
        if cham_df['summoner1Id'][i] == spell1_1 and cham_df['summoner2Id'][i] == spell1_2:
            spell1_cnt +=1
            if cham_df['win'][i] == True:
                spell1_win += 1
        elif cham_df['summoner1Id'][i] == spell2_1 and cham_df['summoner2Id'][i] == spell2_2:
            spell2_cnt += 1
            if cham_df['win'][i] == True:
                spell2_win += 1
    # cham_info에서 선언한 컬럼 순서대로
    # print("cham_cnt, spell1_cnt, spell2_cnt,spell1_win, spell2_win: ",
    #       cham_cnt, spell1_cnt, spell2_cnt,spell1_win, spell2_win )

    # division zero 방지 디버깅
    if spell1_cnt == 0:
        spell1_cnt +=1
    if spell2_cnt == 0:
        spell2_cnt +=1

    result = [spell1_1,spell1_2,spell1_cnt,round(spell1_cnt/cham_cnt,2),round(spell1_win/spell1_cnt,2),
              spell2_1,spell2_2,spell2_cnt,round(spell2_cnt/cham_cnt,2),round(spell2_win/spell2_cnt,2)]
    return result
# print(cal_spell(cham_df=test_cham_df,cham_cnt=len(test_cham_df)))


# 5. 스킬 빌드
def cal_skilltree(cham_df, cham_cnt):
    all_skill = []

    # 모든 skill_slot의 경우의 수 구하기
    for i in range(len(cham_df)):
        skill_slot = cham_df['skill_slot'][i]
        if skill_slot not in all_skill and skill_slot != None:
            all_skill.append(skill_slot)
    # print("해당 챔피언의 모든 스킬트리의 경우의 수: ",all_skill)

    # 경우의 수의 count를 담아줄 hash = {각 경우: count 수}
    skill_hash = dict(zip(all_skill,[0] * len(all_skill)))

    # cnt 올려주는 연산 작업
    for i in range(len(cham_df)):
        if cham_df['skill_slot'][i] != None:
            skill_hash[str(cham_df['skill_slot'][i])] += 1


    # cnt가 높은 순으로 내림차순
    skill_hash = dict(sorted(skill_hash.items(), key=lambda x: x[1], reverse=True))
    # print("skill_hash: ",skill_hash)   # 내림차순 결과

    # 스킬빌드가 아예 없는 경우 디버깅
    if len(list(list(skill_hash))) == 0:
        return [None] * 6

    fin = list(list(skill_hash)[0])  # 스킬 빌드 1순위만

    # 마스터한 스킬이 2가지 뿐이면 남은 한가지를 채워주는 반복문
    # 마스터 스킬이 1가지 뿐이면 1개인채로 유지함
    if len(fin) == 2:
        # print("mast_skill 추가 전: ",fin)
        mast_skill = ['1','2','3']
        for skill in fin:
            for mast in mast_skill:
                if mast not in fin:
                        fin.append(mast)
                        break

    if len(fin) <= 1:
        for _ in range(3-len(fin)):
            fin.append("No skill")
            # print("1이하의 fin에  None 추가후: ",fin)

    skill_build1, skill_build2, skill_build3 = fin


    skill_cnt = 0
    skill_win= 0

    for i in range(len(cham_df)):
        if cham_df['skill_slot'][i] == list(skill_hash)[0] or cham_df['skill_slot'][i] == ''.join(fin):
            skill_cnt += 1
            if cham_df['win'][i] == True:
                skill_win +=1
    result = [skill_build1,skill_build2,skill_build3,
              skill_cnt,round(skill_cnt/cham_cnt,2),round(skill_win/skill_cnt,2)]
    # print(result)
    return result
# print(cal_skilltree(cham_df=test_cham_df,cham_cnt=len(test_cham_df)))

# 6. 시작 아이템 빌드
def cal_item_build(cham_df,cham_cnt):
    all_itembuild = []

    for i in range(len(cham_df)):
        temp = [cham_df['first_pur1'][i],cham_df['first_pur2'][i],
                    cham_df['first_pur3'][i],cham_df['first_pur4'][i],
                    cham_df['first_pur5'][i],cham_df['first_pur6'][i],
                    cham_df['first_pur7'][i],cham_df['first_pur8'][i]]

        if temp not in all_itembuild:
            all_itembuild.append(temp)

    # print("해당 챔피언의 모든 주 시작아이템의 모든 경우의 수: ", all_itembuild)
    # print("그 개수는: ", len(all_itembuild))

    # 조합의 출현 횟수 count를 위한 hash 만들기
    # {all_itembuild 인덱스: all_itembuild 조합의 값}
    combin_index = [str(i) for i in range(len(all_itembuild))]
    item_hash = dict(zip(combin_index, all_itembuild))
    # print("item_hash: ", item_hash)

    item_cnt = dict(zip(combin_index, [0] * len(all_itembuild)))
    # print("item_cnt: ", item_cnt)

    # # 주 룬세팅 조합의 개수 cnt해주기
    for i in range(len(cham_df)):
        temp2 = [cham_df['first_pur1'][i], cham_df['first_pur2'][i],
                    cham_df['first_pur3'][i], cham_df['first_pur4'][i],
                    cham_df['first_pur5'][i], cham_df['first_pur6'][i],
                    cham_df['first_pur7'][i], cham_df['first_pur8'][i]]

        for conbin in item_hash.values():
            if temp2 == conbin:
                    # print("temp2: ",temp2)
                    # print("index: ",all_lune.index(temp2))
                item_cnt[str(all_itembuild.index(temp2))] += 1

    item_cnt = dict(sorted(item_cnt.items(), key=lambda x: x[1], reverse=True))
    # print("정렬이 끝난 item_cnt: ", item_cnt)

    # print(item_hash[str(list(item_cnt)[0])]) # 1순위 조합만 추출
    # print(item_hash[str(list(item_cnt)[1])])  # 2순위 조합만 추출

    if len(list(item_cnt)) >= 2:
        fin_itembuild = [item_hash[str(list(item_cnt)[0])],
                     item_hash[str(list(item_cnt)[1])]]
    elif len(list(item_cnt)) == 1:
        fin_itembuild = [None] * 2
        fin_itembuild[0] = item_hash[str(list(item_cnt)[0])]
        fin_itembuild[1] = [None] * 8
    else:
        return [None] * 22

    item_set1_1,item_set1_2,item_set1_3,item_set1_4,item_set1_5,item_set1_6,item_set1_7,item_set1_8 = fin_itembuild[0]
    item_set2_1, item_set2_2, item_set2_3, item_set2_4, item_set2_5, item_set2_6,item_set2_7,item_set2_8 = fin_itembuild[1]
    item_set1_cnt = 0
    item_set2_cnt = 0
    item_set1_win = 0
    item_set2_win = 0

    for i in range(len(cham_df)):
        temp3 = [cham_df['first_pur1'][i],cham_df['first_pur2'][i],cham_df['first_pur3'][i],
                     cham_df['first_pur4'][i],cham_df['first_pur5'][i],cham_df['first_pur6'][i],
                     cham_df['first_pur7'][i],cham_df['first_pur8'][i]]
        if temp3 == fin_itembuild[0]:
            item_set1_cnt +=1
            if cham_df['win'][i] == True:
                item_set1_win+=1

        elif temp3 == fin_itembuild[1]:
            item_set2_cnt += 1
            if cham_df['win'][i] == True:
                item_set2_win += 1
    # print("item_set1_cnt,item_set2_cnt,item_set1_win,item_set2_win: ", item_set1_cnt,item_set2_cnt,item_set1_win,item_set2_win)

    # division by zero 에러를 막기 위한 더미로 1 cnt 올려주었음
    if item_set1_cnt == 0:
        item_set1_cnt +=1
    if item_set2_cnt == 0:
        item_set2_cnt +=1

    result = [item_set1_1,item_set1_2,item_set1_3,
              item_set1_4,item_set1_5,item_set1_6,item_set1_7,item_set1_8,
              item_set1_cnt,round(item_set1_cnt/cham_cnt,2),round(item_set1_win/item_set1_cnt,2),

              item_set2_1, item_set2_2, item_set2_3,
              item_set2_4, item_set2_5, item_set2_6,item_set2_7,item_set2_8,
              item_set2_cnt, round(item_set2_cnt/cham_cnt, 2), round(item_set2_win/item_set2_cnt, 2)
              ]
    # print(result)
    return  result
# print(cal_item_build(cham_df= test_cham_df,cham_cnt=len(test_cham_df)))
# print(cal_item_build(classic_df,'Zyra'))

# 7. 신발
def cal_shoes(cham_df,cham_cnt):
    all_shoes =[]


    # 모든 경우의 수 찾기
    for i in range(len(cham_df)):

        if cham_df['shoes'][i] not in all_shoes:
            if cham_df['shoes'][i] == None:
                continue
            all_shoes.append(cham_df['shoes'][i])
    # print("챔피언의 모든 신발의 경우의 수는: ", all_shoes)
    shoes_hash = dict(zip(all_shoes,[0]*len(all_shoes)))

    # 신발 등장 횟수 count
    for i in range(len(cham_df)):
        if cham_df['shoes'][i] == None:
            continue
        else:
            shoes_hash[str(cham_df['shoes'][i])] += 1


    # 내림차순 정렬하기
    shoes_hash = dict(sorted(shoes_hash.items(), key=lambda x: x[1], reverse=True))
    # print("shoes_hash: ", shoes_hash)

    if len(list(shoes_hash)) >= 2:
        a = list(shoes_hash)[0]  # shoes_hash값만 list로 만들어 1순위, 2순위만 추출
        b = list(shoes_hash)[1]
        # print("최종 값: ",a,b)
    elif len(list(shoes_hash)) == 1:
        a = list(shoes_hash)[0]
        b= [None]

    else:
        return [None] * 8

    # ----------------------------------------------------------
    shoes1_cnt = 0   # 신발 표본수
    shoes1_win = 0   # 신발별 승률
    shoes2_cnt = 0
    shoes2_win = 0

    for i in range(len(cham_df)):
        if cham_df['shoes'][i] == str(a):
            shoes1_cnt +=1
            if cham_df['win'][i] == True:
                shoes1_win += 1
        elif cham_df['shoes'][i] == str(b):
            shoes2_cnt +=1
            if cham_df['win'][i] == True:
                shoes2_win += 1

    # division by zero 에러를 막기 위한 더미로 1 cnt 올려주었음
    if shoes1_cnt == 0:
        shoes1_cnt +=1
    if shoes2_cnt == 0:
        shoes2_cnt +=1

    result = [a,shoes1_cnt,round(shoes1_cnt/cham_cnt,2),round(shoes1_win/shoes1_cnt,2),
              b,shoes2_cnt,round(shoes2_cnt/cham_cnt,2),round(shoes2_win/shoes2_cnt,2)]
    # print(result)
    return result
# print(cal_shoes(cham_df=test_cham_df,cham_cnt=len(test_cham_df)))
# print(cal_shoes(classic_df,'Zyra'))

# 8. 코어 빌드
def cal_corebuild(cham_df,cham_cnt):
    all_core = []

    # corebuild조합의 모든 경우의 수 구하기
    for i in range(len(cham_df)):
        temp = [cham_df['core1'][i], cham_df['core2'][i],
                    cham_df['core3'][i], cham_df['core4'][i],
                    cham_df['core5'][i], cham_df['core6'][i]]

        if temp == [None] * 6:
            continue

        if temp not in all_core:
            all_core.append(temp)

    # print("해당 챔피언의 모든 주 코어의 모든 경우의 수: ", all_core)
    # print("그 개수는: ", len(all_core))

    # 조합의 출현 횟수 count를 위한 hash 만들기
    # {all_itembuild 인덱스: all_itembuild 조합의 값}
    combin_index = [str(i) for i in range(len(all_core))]
    core_hash = dict(zip(combin_index, all_core))
    # print("core_hash: ", core_hash)

    core_cnt = dict(zip(combin_index, [0] * len(all_core)))
    # print("core_cnt: ", core_cnt)

    # # 주 룬세팅 조합의 개수 cnt해주기
    for i in range(len(cham_df)):
        temp2 = [cham_df['core1'][i], cham_df['core2'][i],
                    cham_df['core3'][i], cham_df['core4'][i],
                    cham_df['core5'][i], cham_df['core6'][i]]

        for conbin in core_hash.values():
            if temp2 == conbin:
                    # print("temp2: ",temp2)
                    # print("index: ",all_lune.index(temp2))
                core_cnt[str(all_core.index(temp2))] += 1

    core_cnt = dict(sorted(core_cnt.items(), key=lambda x: x[1], reverse=True))
    # print("정렬이 끝난 core_cnt: ", core_cnt)
    if len(list(core_cnt)) >= 3:
        core1, core2, core3 = core_hash[str(list(core_cnt)[0])],core_hash[str(list(core_cnt)[1])],core_hash[str(list(core_cnt)[2])]
    elif len(list(core_cnt)) == 2:
        core1,core2 = core_hash[str(list(core_cnt)[0])],core_hash[str(list(core_cnt)[1])]
        core3 = [None] * 6
    elif len(list(core_cnt)) == 1:
        core1 = core_hash[str(list(core_cnt)[0])]
        core2 = [None] * 6
        core3 = [None] * 6
    else:
        return [None] * 27

    core1_cnt = 0
    core1_win = 0
    core2_cnt = 0
    core2_win = 0
    core3_cnt = 0
    core3_win = 0

    # 코어마다 표본수, 점유율, 승률 계산
    for i in range(len(cham_df)):
        temp3 = [cham_df['core1'][i], cham_df['core2'][i],
                        cham_df['core3'][i], cham_df['core4'][i],
                        cham_df['core5'][i], cham_df['core6'][i]]

        if temp3 == core1:
            core1_cnt += 1
            if cham_df['win'][i] == True:
                core1_win += 1
        elif temp3 == core2:
            core2_cnt += 1
            if cham_df['win'][i] == True:
                core2_win += 1
        elif temp3 == core3:
            core3_cnt += 1
            if cham_df['win'][i] == True:
                core3_win += 1

    core1_1, core1_2, core1_3, core1_4, core1_5, core1_6 = core1
    core2_1, core2_2, core2_3, core2_4, core2_5, core2_6 = core2
    core3_1, core3_2, core3_3, core3_4, core3_5, core3_6 = core3


    # division by zero 에러를 막기 위한 더미로 1 cnt 올려주었음
    if core1_cnt == 0:
        core1_cnt +=1
    if core2_cnt == 0:
        core2_cnt +=1
    if core3_cnt == 0:
        core3_cnt +=1

    result = [core1_1, core1_2, core1_3, core1_4, core1_5, core1_6,
              core1_cnt, round(core1_cnt/cham_cnt,2),round(core1_win/core1_cnt,2),

              core2_1, core2_2, core2_3, core2_4, core2_5, core2_6,
              core2_cnt, round(core2_cnt / cham_cnt, 2), round(core2_win / core2_cnt, 2),

              core3_1, core3_2, core3_3, core3_4, core3_5, core3_6,
              core3_cnt, round(core3_cnt / cham_cnt, 2), round(core3_win / core3_cnt, 2)]
    # print(result)
    return result

# print(cal_corebuild(cham_df=cham_df,cham_cnt=len(cham_df))
# print(cal_corebuild(classic_df,'Zyra'))
