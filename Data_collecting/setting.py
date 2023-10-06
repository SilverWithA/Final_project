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
tier_cnt = {'chall':180,'grand':180,'mast':180,
                'dia':180,'em':180,'pla':180,
                'gold':180,'sil':180,'bro':180,'iron':180}

# 불러올 matchID의 개수
# tier_cnt = {'chall':197,'grand':200,'mast':200,
#                 'dia':500,'em':500,'pla':500,
#                 'gold':1000,'sil':1000,'bro':1000,'iron':500}

raw_coll = {'chall':db_raw.chall_total,'grand':db_raw.grand_total,'mast':db_raw.mast_total,
                'dia':db_raw.dia_total,'em':db_raw.em_total,'pla':db_raw.pla_total,
                'gold':db_raw.gold_total,'sil':db_raw.sil_total,'bro':db_raw.bro_total,'iron':db_raw.iron_total}


# 코어 아이템 리스트
core_list = [3087, 6632, 3179, 6672, 3115, 2065, 3152, 6631, 3078,
             6653, 3142, 6692, 6630, 4636, 3508, 3190, 6656, 6657,
             6675, 6655, 3003, 3004, 4644, 3084, 3116, 6617, 3095,
             6691, 6620, 3074, 6667, 3153, 3068, 4633, 3001, 6662,
             3124, 3041, 6676, 3085, 6671, 4005, 3071, 3100, 3031, 3181, 4637, 3050, 3504, 6693, 3107, 3161, 4645,
             3109, 3742, 6616, 3222, 6665, 3748, 3091, 6696, 3157, 3011, 4628, 8001, 3814, 6673, 8020, 3046, 6694,
             3102, 3094, 4629, 3119, 3089, 3053, 3083, 3075, 3072, 3036, 3156, 3110, 3033, 6609, 6695, 4638, 3065,
             6333, 3026, 4401, 3193, 3165, 3135, 3143]


# 신발 아이템 리스트
shoes_list = [3006,3009,3020,3047,3111,3117,3158]

teamposit_list = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']
