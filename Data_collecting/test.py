from db_functions import *
from setting import *
import pandas as pd

# 테스트 데이터
table_list = show_tables(engine_gam)
# print(table_list)
chall_aram = select_db(table_list[3][0],conn_name=conn_gam)
chall_lose = select_db(table_list[4][0],conn_name=conn_gam)
chall_win = select_db(table_list[5][0],conn_name=conn_gam)

# print(chall_win.head())
chall_classic = pd.merge(chall_win,chall_lose, how='outer')

# 챔피언 별 세팅 계산하는 함수임
# 1. 룬 계산하기 - 챔피언
def cal_prim_lune():
    all_lune = []
    for i in range(len(chall_classic)):
        prim1_perk = chall_classic['prim1_perk'][i]
        prim2_perk = chall_classic['prim2_perk'][i]
        prim3_perk = chall_classic['prim3_perk'][i]
        prim4_perk = chall_classic['prim4_perk'][i]
        prim_style = chall_classic['prim_style'][i]

        temp = [prim1_perk,prim2_perk,prim3_perk,prim4_perk,prim_style]
        if temp not in all_lune:
            all_lune.append(temp)

    print("해당 챔피언의 모든 주 룬 세팅의 모든 경우의 수: ", all_lune)
    print("그 개수는: ", len(all_lune))

    # 조합의 출현 횟수 count를 위한 hash 만들기
    # {all_lune의 인덱스: all_lune의 조합의 값}
    combin_index = [str(i) for i in range(len(all_lune))]
    primlune_hash = dict(zip(combin_index, all_lune))
    print("primlune_hash: ", primlune_hash)

    primlune_cnt = dict(zip(combin_index, [0]* len(all_lune)))
    print("primlune_cnt: ",primlune_cnt)

    # 주 룬세팅 조합의 개수 cnt해주기
    for i in range(len(chall_classic)):
        prim1_perk = chall_classic['prim1_perk'][i]
        prim2_perk = chall_classic['prim2_perk'][i]
        prim3_perk = chall_classic['prim3_perk'][i]
        prim4_perk = chall_classic['prim4_perk'][i]
        prim_style = chall_classic['prim_style'][i]
        temp2 = [prim1_perk, prim2_perk, prim3_perk, prim4_perk, prim_style]

        for conbin in primlune_hash.values():
            if temp2 == conbin:
                # print("temp2: ",temp2)
                # print("index: ",all_lune.index(temp2))
                primlune_cnt[str(all_lune.index(temp2))] += 1

    primlune_cnt = dict(sorted(primlune_cnt.items(), key=lambda x:x[1], reverse=True))
    print("정렬이 끝난 primlune_cnt: ",primlune_cnt)
    a,b,c,d,e = primlune_hash[str(list(primlune_cnt)[0])]  # 1순위 조합만 추출
    print(a,b,c,d,e)
def cal_sub_lune():
    all_sublune = []
    # 모든 경우의 수 저장
    for i in range(len(chall_classic)):

        temp = [chall_classic['sub1_perk'][i],chall_classic['sub2_perk'][i],chall_classic['sub_style'][i]]

        if temp not in all_sublune:
            all_sublune.append(temp)

    print("all_sublune: ",all_sublune)
    print("모든 경우의 수는: ", len(all_sublune))

    # count를 위한 해시 생성
    # sublune_cnt = {all_sublune의 index:all_sublune의 값}
    all_index = [str(i) for i in range(len(all_sublune))]
    sublune_hash = dict(zip(all_index,all_sublune))

    print("sublune_hash: ",sublune_hash)

    # cnt올려주기 위한 hash 생성
    sublune_cnt = dict(zip(all_index, [0]* len(all_sublune)))
    print("sublune_cnt: ",sublune_cnt)
    for i in range(len(chall_classic)):
        temp2 = [chall_classic['sub1_perk'][i],chall_classic['sub2_perk'][i],chall_classic['sub_style'][i]]

        for combin in sublune_hash.values():
            if temp2 == combin:
                sublune_cnt[str(all_sublune.index(temp2))] += 1

    sublune_cnt = dict(sorted(sublune_cnt.items(), key=lambda x:x[1],reverse=True))
    print("sublune_cnt: ",sublune_cnt)
    final_sublune =sublune_hash[str(list(sublune_cnt)[0])]      # 1순위 조합의 index
    print(final_sublune)

# 1-1. 능력치 파편
def cal_ability():
    abil_combin = []
    # 모든 조합 경우의 수 찾기
    for i in range(len(chall_classic)):  # all table data iterate
        defense = chall_classic['defense'][i]
        flex = chall_classic['flex'][i]
        offense = chall_classic['offense'][i]
        temp1 = [defense,flex,offense]

        if temp1 not in abil_combin:
            abil_combin.append(temp1)

    print("능력치 파편의 모든 경우의 수는: ", len(abil_combin),"가지 입니다.")
    keys = [str(i) for i in range(len(abil_combin))]

    # {index: abil_combin} = {어떤 경우의 수의 abil_combin 인덱스: 경우의 수 리스트}
    abil_hash = dict(zip(keys,abil_combin))
    print("abil_combin의 인덱스: 경우의 수 = abil_hash: ", abil_hash)


    # 어떤 조합의 출현빈도  cnt 를 계산하기 위한 code
    cnt_ability = dict(zip(keys, [0] * len(abil_combin)))

    for i in range(len(chall_classic)):         # all table data iterate
        temp2 = [chall_classic['defense'][i],chall_classic['flex'][i], chall_classic['offense'][i]]
        for combin in abil_combin:
            if temp2 == combin:
                # print("abil_combin에서 temp2의 인덱스: ", abil_combin.index(temp2))
                cnt_ability[str(abil_combin.index(temp2))] += 1

    # {index:count} 오름차순으로 정리
    cnt_ability = dict(sorted(cnt_ability.items(), key=lambda x:x[1], reverse=True))
    # print("해당 챔피언의 모든 능력치 파편의 경우의 수 및 개수: ",cnt_ability)


    # 가장 경우의 수가 많은 능력치 파편을 저장을 위한 리스트에 넣어주기
    index_order = list(cnt_ability)   # cnt 내림 차순으로 인덱스의 순서
    # print(abil_hash[index_order[0]])  # 1순위 조합
    a,b,c =abil_hash[index_order[0]]  # 1순위 조합
    print("최종 값: ",a,b,c)
# 2. 소환사 주문
def cal_spell():
    spell_combin = []

    # 모든 조합 경우의 수 찾기
    for i in range(len(chall_classic)):  # all table data iterate
        spell1 = chall_classic['summoner1Id'][i]
        spell2 = chall_classic['summoner2Id'][i]

        temp = [spell1,spell2]
        if temp not in spell_combin:
            spell_combin.append(temp)

    print("능력치 파편의 모든 경우의 수는: ", len(spell_combin), "가지 입니다.")
    keys = [str(i) for i in range(len(spell_combin))]

    # {index: abil_combin} = {어떤 경우의 수의 abil_combin 인덱스: 경우의 수 리스트}
    spell_hash = dict(zip(keys, spell_combin))
    print("abil_combin의 인덱스: 경우의 수 = abil_hash: ", spell_hash)


    # 경우의 수 별 count 세기
    # 어떤 조합의 출현빈도  cnt 를 계산하기 위한 code
    spell_cnt = dict(zip(keys, [0] * len(spell_combin)))

    for i in range(len(chall_classic)):  # all table data iterate
        spell1 = chall_classic['summoner1Id'][i]
        spell2 = chall_classic['summoner2Id'][i]

        temp2 = [spell1, spell2]

        for combin in spell_combin:
            if temp2 == combin:
                # print("abil_combin에서 temp2의 인덱스: ", abil_combin.index(temp2))
                spell_cnt[str(spell_combin.index(temp2))] += 1

    # {index:count} 오름차순으로 정리
    spell_cnt = dict(sorted(spell_cnt.items(), key=lambda x: x[1], reverse=True))
    print("해당 챔피언의 모든 능력치 파편의 경우의 수 및 개수: ",spell_cnt)

    # 가장 경우의 수가 많은 능력치 파편을 저장을 위한 리스트에 넣어주기
    index_order = list(spell_cnt)  # cnt 내림 차순으로 인덱스의 순서
    print("index_order: ",index_order)
    # print(abil_hash[index_order[0]])  # 1순위 조합
    a, b = spell_hash[str(index_order[0])]  # 1순위 조합
    c, d = spell_hash[str(index_order[1])]  # 1순위 조합
    print("최종 값: ", a, b)
    print("최종 값: ", c, d)
# 3. 스킬 빌드
def cal_skilltree():
    all_skill = []
    # 모든 skill_slot의 경우의 수 구하기
    for i in range(len(chall_classic)):
        skill_slot = chall_classic['skill_slot'][i]
        if  skill_slot not in all_skill:
            all_skill.append(skill_slot)
    print("해당 챔피언의 모든 스킬트리의 경우의 수: ",all_skill)

    # 경우의 수의 count를 담아줄 hash = {각 경우: count 수}
    skill_hash = dict(zip(all_skill,[0] * len(all_skill)))

    # cnt 올려주는 연산 작업
    for i in range(len(chall_classic)):
        skill_hash[str(chall_classic['skill_slot'][i])] += 1


    # cnt가 높은 순으로 내림차순
    skill_hash = dict(sorted(skill_hash.items(), key=lambda x: x[1], reverse=True))
    print("skill_hash: ",skill_hash)   # 내림차순 결과

    a = list(skill_hash)[0] # 키값만 list로 만들기
    b = list(skill_hash)[1]
    fin = [list(a),list(b)]
    print("mast_skill 추가 전: ",fin)

    mast_skill = ['1','2','3']

    for skill_str in fin:
        for mast in mast_skill:
            if mast not in skill_str:
                skill_str.append(mast)

    print("mast_skill 추가: ",fin)
# 4. 시작 아이템 빌드
def cal_item_build():
    all_itembuild = []

    for i in range(len(chall_classic)):
        temp = [chall_classic['first_pur1'][i],chall_classic['first_pur2'][i],
                chall_classic['first_pur3'][i],chall_classic['first_pur4'][i],
                chall_classic['first_pur5'][i],chall_classic['first_pur6'][i],
                chall_classic['first_pur7'][i],chall_classic['first_pur8'][i]]

        if temp not in all_itembuild:
            all_itembuild.append(temp)

    print("해당 챔피언의 모든 주 룬 세팅의 모든 경우의 수: ", all_itembuild)
    print("그 개수는: ", len(all_itembuild))

    # 조합의 출현 횟수 count를 위한 hash 만들기
    # {all_itembuild 인덱스: all_itembuild 조합의 값}
    combin_index = [str(i) for i in range(len(all_itembuild))]
    item_hash = dict(zip(combin_index, all_itembuild))
    print("item_hash: ", item_hash)

    item_cnt = dict(zip(combin_index, [0] * len(all_itembuild)))
    print("item_cnt: ", item_cnt)

    # # 주 룬세팅 조합의 개수 cnt해주기
    for i in range(len(chall_classic)):
        temp2 = [chall_classic['first_pur1'][i], chall_classic['first_pur2'][i],
                chall_classic['first_pur3'][i], chall_classic['first_pur4'][i],
                chall_classic['first_pur5'][i], chall_classic['first_pur6'][i],
                chall_classic['first_pur7'][i], chall_classic['first_pur8'][i]]

        for conbin in item_hash.values():
            if temp2 == conbin:
                # print("temp2: ",temp2)
                # print("index: ",all_lune.index(temp2))
                item_cnt[str(all_itembuild.index(temp2))] += 1

    item_cnt = dict(sorted(item_cnt.items(), key=lambda x: x[1], reverse=True))
    print("정렬이 끝난 item_cnt: ", item_cnt)

    print(item_hash[str(list(item_cnt)[0])]) # 1순위 조합만 추출
    print(item_hash[str(list(item_cnt)[1])])  # 2순위 조합만 추출

    fin_itembuild = [item_hash[str(list(item_cnt)[0])],
                     item_hash[str(list(item_cnt)[1])]]
# 5. 신발
def cal_shoes():
    all_shoes =[]

    # 모든 경우의 수 찾기
    for i in range(len(chall_classic)):
        if chall_classic['shoes'][i] not in all_shoes:
            if chall_classic['shoes'][i] == None:
                continue
            all_shoes.append(chall_classic['shoes'][i])
    print("챔피언의 모든 신발의 경우의 수는: ", all_shoes)

    shoes_hash = dict(zip(all_shoes,[0]*len(all_shoes)))

    # 신발 등장 횟수 count
    for i in range(len(chall_classic)):
        if chall_classic['shoes'][i] == None:
            continue
        shoes_hash[str(chall_classic['shoes'][i])] += 1

    # 내림차순 정렬하기
    shoes_hash = dict(sorted(shoes_hash.items(), key=lambda x: x[1], reverse=True))
    print("shoes_hash: ", shoes_hash)
    a = list(shoes_hash)[0]  # shoes_hash값만 list로 만들어 1순위, 2순위만 추출
    b = list(shoes_hash)[1]
    print("최종 값: ",a,b)
# 6. 코어 빌드
def cal_corebuild():
    all_core = []

    for i in range(len(chall_classic)):
        temp = [chall_classic['core1'][i], chall_classic['core2'][i],
                chall_classic['core3'][i], chall_classic['core4'][i],
                chall_classic['core5'][i], chall_classic['core6'][i]]

        if temp == [None] * 6:
            continue

        if temp not in all_core:
            all_core.append(temp)

    print("해당 챔피언의 모든 주 코어의 모든 경우의 수: ", all_core)
    print("그 개수는: ", len(all_core))

    # 조합의 출현 횟수 count를 위한 hash 만들기
    # {all_itembuild 인덱스: all_itembuild 조합의 값}
    combin_index = [str(i) for i in range(len(all_core))]
    core_hash = dict(zip(combin_index, all_core))
    print("core_hash: ", core_hash)

    core_cnt = dict(zip(combin_index, [0] * len(all_core)))
    print("core_cnt: ", core_cnt)

    # # 주 룬세팅 조합의 개수 cnt해주기
    for i in range(len(chall_classic)):
        temp2 = [chall_classic['core1'][i], chall_classic['core2'][i],
                chall_classic['core3'][i], chall_classic['core4'][i],
                chall_classic['core5'][i], chall_classic['core6'][i]]

        for conbin in core_hash.values():
            if temp2 == conbin:
                # print("temp2: ",temp2)
                # print("index: ",all_lune.index(temp2))
                core_cnt[str(all_core.index(temp2))] += 1

    core_cnt = dict(sorted(core_cnt.items(), key=lambda x: x[1], reverse=True))
    print("정렬이 끝난 core_cnt: ", core_cnt)

    print(core_hash[str(list(core_cnt)[0])])  # 1순위 조합만 추출
    print(core_hash[str(list(core_cnt)[1])])  # 2순위 조합만 추출

    fin_core = [core_hash[str(list(core_cnt)[0])],core_hash[str(list(core_cnt)[1])],
                     core_hash[str(list(core_cnt)[2])], core_hash[str(list(core_cnt)[3])]]

    print(fin_core)
cal_corebuild()