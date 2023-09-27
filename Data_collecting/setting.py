from db_functions import *
# product api 키 저장
api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"

# lowCase_tier
lowCase = ["chall","grand","mast",
              "dia","em","pla",
              "gold","sil","bro","iron"]

# API_Tier: hash
api_tier = {"dia":"DIAMOND","em":"EMERALD","pla":"PLATINUM",
              "gold":"GOLD","sil":"SILVER","bro":"BRONZE","iron":"IRON"}

# 조회할 회원수
tier_cnt = {'chall':10,'grand':20,'mast':70,
                'dia':125,'em':425,'pla':750,
                'gold':950,'sil':900,'bro':900,'iron':400}

# 불러올 matchID의 개수
tier_cnt = {'chall':197,'grand':200,'mast':200,
                'dia':500,'em':500,'pla':500,
                'gold':1000,'sil':1000,'bro':1000,'iron':500}

raw_coll = {'chall':db_raw.chall_total,'grand':db_raw.grand_total,'mast':db_raw.mast_total,
                'dia':db_raw.dia_total,'em':db_raw.em_total,'pla':db_raw.pla_total,
                'gold':db_raw.gold_total,'sil':db_raw.sil_total,'bro':db_raw.bro_total,'iron':db_raw.iron_total}