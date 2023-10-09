
# for cham in posit_cham:  # chamName per position iterate
#     ban_cnt = 0
#     championId = chamID_hash[str(cham)]
#
#     # 티어에 대한 테이블 전체 스캔을 줄이기위해 cham에 대한 데이터만 미리 cham_df에 저장
#     cham_df = pd.DataFrame(columns=columns_list)
#     for i in range(len(table)):
#         if table['championName'][i] == cham:
#             n = len(cham_df)
#             cham_df.loc[n] = table.loc[i]
#
#         # cham에 대한 밴픽
#         if cham_df['bans'][i] == championId:
#             ban_cnt += 1
#
#     cham_cnt = len(cham_df)
#
#     if cham_cnt == 0:
#         print(lowCase,"티어에서", cham,"이 픽된 해당하는 게임 정보가 없습니다. 다음 챔피언 정보 연산을 위해 넘어갑니다.")
#         continue
#
#     chamName = cham
#     championId = chamID_hash[str(cham)]
#
#     # 1. 승픽밴
#     win_cnt, ban_cnt, pick_cnt,win_rate, ban_rate, pick_rate, av_kda = cal_base()
#
#     # 2. 룬세팅
#     pri_perk1,pri_perk2,pri_perk3,pri_perk4,pri_style = cal_prim_lune(table,str(cham))
#     sub_perk1, sub_perk2, sub_style = cal_sub_lune(table,str(cham))
#
#     # 3. 능력치 파편
#     deffence, flex, offence = cal_ability(table,str(cham))
#
#
#     # 4. 소환사 주문
#     (spell1_1,spell1_2,spell1_cnt, spell1_rate,spell1_win,
#      spell2_1, spell2_2,spell2_cnt, spell2_rate,spell2_win) = cal_spell(table,str(cham))
#
#     # 5. 스킬 빌드
#     skill_build1,skill_build2,skill_build3,skill_cnt,skill_rate,skill_win = cal_skilltree(table,str(cham))
#
#     # 6. 아이템 빌드
#     (item_set1_1, item_set1_2, item_set1_3,item_set1_4, item_set1_5, item_set1_6, item_set1_7, item_set1_8,
#      item_set1_cnt, item_set1_rate, item_set1_win,
#
#      item_set2_1, item_set2_2, item_set2_3,item_set2_4, item_set2_5, item_set2_6, item_set2_7, item_set2_8,
#      item_set2_cnt, item_set2_rate, item_set2_win) = cal_item_build(table,str(cham))
#
#     # 7. 신발 빌드
#     (shoe1,shoes1_cnt,shoes1_rate,shoes1_win,
#      shoe2,shoes2_cnt,shoes2_rate,shoes2_win) = cal_shoes(table, str(cham))
#
#     # 8. 코어 빌드
#     (core1_1, core1_2, core1_3, core1_4, core1_5, core1_6,
#       core1_cnt,core1_rate,core1_win,
#
#       core2_1, core2_2, core2_3, core2_4, core2_5, core2_6,
#       core2_cnt,core2_rate,core2_win,
#
#       core3_1, core3_2, core3_3, core3_4, core3_5, core3_6,
#       core3_cnt,core3_rate,core3_win)=cal_corebuild(table,str(cham))
#
#
#     # df에 저장을 위한 리스트 insert의 value 부분
#     data_list = [lowCase,chamName, championId, teamposit_list[i],cham_cnt,
#
#                  win_cnt,ban_cnt,pick_cnt,
#                  win_rate, ban_rate, pick_rate,av_kda,
#
#                  pri_perk1,pri_perk2,pri_perk3,pri_perk4,pri_style,
#                  sub_perk1,sub_perk2,sub_style,
#                  deffence, flex, offence,
#
#                  spell1_1, spell1_2, spell1_cnt, spell1_rate, spell1_win,
#                  spell2_1, spell2_2, spell2_cnt, spell2_rate, spell2_win,
#
#
#                  skill_build1,skill_build2,skill_build3,skill_cnt,skill_rate,skill_win,
#
#                  item_set1_1, item_set1_2, item_set1_3, item_set1_4, item_set1_5, item_set1_6, item_set1_7,
#                  item_set1_8, item_set1_cnt, item_set1_rate, item_set1_win,
#
#                  item_set2_1, item_set2_2, item_set2_3, item_set2_4, item_set2_5, item_set2_6, item_set2_7,
#                  item_set2_8,item_set2_cnt, item_set2_rate, item_set2_win,
#
#                  shoe1, shoes1_cnt, shoes1_rate, shoes1_win,
#                  shoe2, shoes2_cnt, shoes2_rate, shoes2_win,
#
#                  core1_1, core1_2, core1_3, core1_4, core1_5, core1_6,
#                  core1_cnt, core1_rate, core1_win,
#
#                  core2_1, core2_2, core2_3, core2_4, core2_5, core2_6,
#                  core2_cnt, core2_rate, core2_win,
#
#                  core3_1, core3_2, core3_3, core3_4, core3_5, core3_6,
#                  core3_cnt, core3_rate, core3_win]
#
#     print(data_list)

# cham_df.loc[0] = data_list
# 쿼리를 하나씩 날리는 구문으로 변경해야함 ----------------------------------------------------
# cham_df.to_sql(name=str(save_name), con=conn_cham, if_exists='append', index=False)
