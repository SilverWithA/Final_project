from db_functions import *
# product api 키 저장
api_key = ""

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


# 브론즈 티어 협곡에서 등장하는 모든 챔피언에 대한 해시값 매핑임 - 모든 챔피언 매핑값은 아님!!!
# chamID_hash = {'Urgot': '6', 'Briar': '233', 'Akali': '84', 'Ezreal': '81', 'Pantheon': '80', 'Darius': '122', 'Kindred': '203', 'Kaisa': '145', 'Vayne': '67', 'Lux': '99', 'Sett': '875', 'LeeSin': '64', 'Ahri': '103', 'Nilah': '895', 'Vex': '711', 'Nautilus': '111', 'KSante': '897', 'Shen': '98', 'Zac': '154', 'Ashe': '22', 'Heimerdinger': '74', 'Vi': '254', 'Kayn': '141', 'Tristana': '18', 'Zed': '238', 'Tryndamere': '23', 'Draven': '119', 'Swain': '50', 'MissFortune': '21', 'Sona': '37', 'Gangplank': '41', 'Yone': '777', 'MasterYi': '11', 'Rumble': '68', 'Rammus': '33', 'Seraphine': '147', 'Lucian': '236', 'Yuumi': '350', 'Aatrox': '266', 'JarvanIV': '59', 'Jinx': '222', 'Leona': '89', 'Aphelios': '523', 'Kayle': '10', 'Nunu': '20', 'Naafiri': '950', 'Nasus': '75', 'Shaco': '35', 'Irelia': '39', 'Samira': '360', 'Renekton': '58', 'Garen': '86', 'Morgana': '25', 'Anivia': '34', 'Poppy': '78', 'Singed': '27', 'Illaoi': '420', 'Trundle': '48', 'Khazix': '121', 'Ekko': '245', 'Quinn': '133', 'Sylas': '517', 'Amumu': '32', 'Yasuo': '157', 'Warwick': '19', 'Hecarim': '120', 'Azir': '268', 'Blitzcrank': '53', 'Nocturne': '56', 'MonkeyKing': '62', 'Caitlyn': '51', 'Volibear': '106', 'Graves': '104', 'TahmKench': '223', 'Belveth': '200', 'Viego': '234', 'XinZhao': '5', 'Varus': '110', 'Rakan': '497', 'Thresh': '412', 'Nidalee': '76', 'Xerath': '101', 'Diana': '131', 'Cassiopeia': '69', 'Soraka': '16', 'Jhin': '202', 'Xayah': '498', 'Leblanc': '7', 'Karthus': '30', 'Janna': '40', 'Fiora': '114', 'AurelionSol': '136', 'DrMundo': '36', 'Ryze': '13', 'Nami': '267', 'Bard': '432', 'Sion': '14', 'Gwen': '887', 'Syndra': '134', 'Teemo': '17', 'Yorick': '83', 'Senna': '235', 'Udyr': '77', 'Karma': '43', 'Maokai': '57', 'Mordekaiser': '82', 'Malphite': '54', 'Twitch': '29', 'Olaf': '2', 'Rengar': '107', 'Pyke': '555', 'Lillia': '876', 'Sivir': '15', 'Ornn': '516', 'Neeko': '518', 'Zoe': '142', 'Evelynn': '28', 'Orianna': '61', 'Chogath': '31', 'Jax': '24', 'Galio': '3', 'Zeri': '221', 'Zyra': '143', 'Sejuani': '113', 'Lissandra': '127', 'Brand': '63', 'Alistar': '12', 'Camille': '164', 'Annie': '1', 'Kassadin': '38', 'Katarina': '55', 'Lulu': '117', 'Veigar': '45', 'Braum': '201', 'Gragas': '79', 'Talon': '91', 'Malzahar': '90', 'Rell': '526', 'Jayce': '126', 'Viktor': '112', 'Ziggs': '115', 'Taliyah': '163', 'Kled': '240', 'Ivern': '427', 'Elise': '60', 'Akshan': '166', 'Riven': '92', 'Qiyana': '246', 'Kennen': '85', 'Skarner': '72', 'Shyvana': '102', 'Fizz': '105', 'Milio': '902', 'Vladimir': '8', 'RekSai': '421', 'FiddleSticks': '9', 'TwistedFate': '4', 'Velkoz': '161', 'Zilean': '26', 'KogMaw': '96', 'Gnar': '150', 'Kalista': '429', 'Renata': '888', 'Taric': '44', 'Corki': '42'}
# 모으기위한 연산 스캐치임
# for j in range(len(tier)):
#     for i in range(len(tier_table)):
#         pass
# print("chamID_hash에 ",len(chamID_hash),"개의 챔피언 ID정보가 모였습니다.")

teamposit_list = ['TOP','JUNGLE','MIDDLE','BOTTOM','UTILITY']

columns_list = ["matchID","win", "gameMode", "summonerName","puuid","teamPosition",
                                   "championName","championId","assists","kills", "deaths",
                                   "defense","flex","offense",
                                   "prim1_perk", "prim2_perk", "prim3_perk", "prim4_perk","prim_style",
                                   "sub1_perk", "sub2_perk", "sub_style",
                                   "summoner1Id","summoner2Id",
                                   "first_pur1","first_pur2","first_pur3","first_pur4",
                                   "first_pur5","first_pur6","first_pur7","first_pur8",
                                   "skill_slot","bans",
                                   "core1","core2","core3","core4","core5","core6","shoes"]

cham_col_list = ['tier','championName', 'championId', 'teamPosition',

                         'match_cnt','win_cnt','ban_cnt','pick_cnt',
                         'win_rate', 'ban_rate', 'pick_rate','av_kda',

                         'most_priperk1', 'most_priperk2', 'most_priperk3', 'most_priperk4', 'most_pristyle',
                         'most_subperk1', 'most_subperk2', 'most_substyle',
                         'abil_def', 'abil_fle', 'abil_off',

                         'spell1_1', 'spell1_2', 'spell1_cnt', 'spell1_rate', 'spell1_win',
                         'spell2_1', 'spell2_2', 'spell2_cnt', 'spell2_rate', 'spell2_win',

                         'skill_build1', 'skill_build2', 'skill_build3',
                         'skill_cnt', 'skill_rate', 'skill_win',

                         'item_set1_1', 'item_set1_2', 'item_set1_3', 'item_set1_4',
                         'item_set1_5', 'item_set1_6', 'item_set1_7', 'item_set1_8',
                         'item_set1_cnt', 'item_set1_rate', 'item_set1_win',

                         'item_set2_1', 'item_set2_2', 'item_set2_3', 'item_set2_4',
                         'item_set2_5', 'item_set2_6', 'item_set2_7','item_set2_8',
                         'item_set2_cnt', 'item_set2_rate', 'item_set2_win',

                         'shoes1', 'shoes1_cnt', 'shoes1_rate', 'shoes1_win',
                         'shoes2', 'shoes2_cnt', 'shoes2_rate', 'shoes2_win',

                         'core1_1', 'core1_2', 'core1_3', 'core1_4', 'core1_5', 'core1_6',
                         'core1_cnt', 'core1_rate', 'core1_win',

                         'core2_1', 'core2_2', 'core2_3', 'core2_4', 'core2_5', 'core2_6',
                         'core2_cnt', 'core2_rate', 'core2_win',

                         'core3_1', 'core3_2', 'core3_3', 'core3_4', 'core3_5', 'core3_6',
                         'core3_cnt', 'core3_rate', 'core3_win']
