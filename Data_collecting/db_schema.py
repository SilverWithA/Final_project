from db_functions import *
from sqlalchemy import create_engine
from sqlalchemy import text
from setting import *


def create_usrinfo():
    """usrinfo DB에 table 스키마 만들기"""

    for i in range(len(lowCase)):

        table_name = lowCase[i] + "_usrinfo"
        with engine_Usr.begin() as connection:
            connection.execute(text('CREATE TABLE {}('
                                    'summonerName varchar(18),'
                                    'puuid varchar(255);'.format(table_name)))
def create_gameinfo_old():
    for i in range(len(lowCase)):
        for j in range(3):
            if j == 0:
                table_name= lowCase[i] + "_Aram"
            elif j == 1:
                table_name = lowCase[i] + "_win"
            else:
                table_name = lowCase[i] + "_lose"

            with engine_gam.begin() as connection:
                connection.execute(text('CREATE TABLE {} (matchID varchar(255) NOT NULL,'
                                        'win bool,'
                                        'gameMode varchar(255),'
                                        'summonerName varchar(18) NOT NULL,'
                                        'puuid varchar(255) NOT NULL,'
                                        'summonerLevel int(5),'   # 최대 5000까지
                                        'gameDuration int(5),'    # 최대 3000으로 잡음 : 50분
                                        'teamPosition varchar(255),'
                                        'championName varchar(255),'
                                        'championId varchar(255),'
                                        'champLevel int(4),'
                                        'assists int(4),'
                                        'kills int(3),'           # 최대 45를 넘지 않음
                                        'deaths int(4),'
    
                                        'defense varchar(255),'
                                        'flex varchar(255),'
                                        'offense varchar(255),'
    
                                        'prim1_perk varchar(255),'
                                        'prim2_perk varchar(255),'
                                        'prim3_perk varchar(255),'
                                        'prim4_perk varchar(255),'
                                        'prim_style varchar(255),'
    
                                        'sub1_perk varchar(255),'
                                        'sub2_perk varchar(255),'
                                        'sub_style varchar(255),'
    
                                        'item0 varchar(255),'
                                        'item1 varchar(255),'
                                        'item2 varchar(255),'
                                        'item3 varchar(255),'
                                        'item4 varchar(255),'
                                        'item5 varchar(255),'
                                        'item6 varchar(255),'

                                        'totalDamToCham varchar(255),'  # totalDamageDealtToChampions
                                        'totalDamTaken varchar(255),'  # totalDamageTaken
    
    
                                        # 최대 100개 씩임
                                        'totalMinionsKilled int(4),'  # totalMinionsKilled
                                        'totalEnemyJunKilled int(4),'  # totalEnemyJungleMinionsKilled
                                        'totalAllyJunKilled int(4),'   # totalAllyJungleMinionsKilled
    
                                        'detWardsPlaced int(4),'  # 최대 500  #detectorWardsPlaced
                                        'goldEarned int(6),'  # 최대 40000
    
                                        # 'bans varchar(255),'
                                        'timeCCingOthers int(5),'  # 최대 1000개 
                                        
                                        'summoner1Id varchar(255),'
                                        'summoner2Id varchar(255),'
                                        
                                        'first_pur1 varchar(255),'
                                        'first_pur2 varchar(255),'
                                        'first_pur3 varchar(255),'
                                        'first_pur4 varchar(255),'
                                        'first_pur5 varchar(255),'
                                        'first_pur6 varchar(255),'
                                        'first_pur7 varchar(255),'
                                        'first_pur8 varchar(255),'
                                        
                                        'skill_slot varchar(255),'
                                        'bans varchar(255),'
                                        
                                        'core1 varchar(255),'
                                        'core2 varchar(255),'
                                        'core3 varchar(255),'
                                        'core4 varchar(255),'
                                        'core5 varchar(255),'
                                        'core6 varchar(255),'
                                        
                                        'shoes varchar(255));'.format(table_name)))
def create_gameinfo_new():
    for i in range(len(lowCase)):
        for j in range(3):
            if j == 0:
                table_name = lowCase[i] + "_Aram"
            elif j == 1:
                table_name = lowCase[i] + "_win"
            else:
                table_name = lowCase[i] + "_lose"

            with engine_gam.begin() as connection:
                connection.execute(text('CREATE TABLE {} (matchID varchar(255) NOT NULL,'
                                        'win bool,'
                                        'gameMode varchar(255),'
                                        'summonerName varchar(18) NOT NULL,'
                                        'puuid varchar(255) NOT NULL,'
                                        'teamPosition varchar(255),'
                                        'championName varchar(255),'
                                        'championId varchar(255),'
                                        'assists int(4),'
                                        'kills int(3),'  # 최대 45를 넘지 않음
                                        'deaths int(4),'

                                        'defense varchar(255),'
                                        'flex varchar(255),'
                                        'offense varchar(255),'

                                        'prim1_perk varchar(255),'
                                        'prim2_perk varchar(255),'
                                        'prim3_perk varchar(255),'
                                        'prim4_perk varchar(255),'
                                        'prim_style varchar(255),'

                                        'sub1_perk varchar(255),'
                                        'sub2_perk varchar(255),'
                                        'sub_style varchar(255),'  # totalDamageTaken

                                        'summoner1Id varchar(255),'
                                        'summoner2Id varchar(255),'

                                        'first_pur1 varchar(255),'
                                        'first_pur2 varchar(255),'
                                        'first_pur3 varchar(255),'
                                        'first_pur4 varchar(255),'
                                        'first_pur5 varchar(255),'
                                        'first_pur6 varchar(255),'
                                        'first_pur7 varchar(255),'
                                        'first_pur8 varchar(255),'

                                        'skill_slot varchar(255),'
                                        'bans varchar(255),'

                                        'core1 varchar(255),'
                                        'core2 varchar(255),'
                                        'core3 varchar(255),'
                                        'core4 varchar(255),'
                                        'core5 varchar(255),'
                                        'core6 varchar(255),'

                                        'shoes varchar(255));'.format(table_name)))
def create_chaminfo():
    for i in range(len(lowCase)+1):
        if i == len(lowCase):
            print("aram 정보 스키마를 저장합니다.")
            table_name = "total_archam"
        elif i < len(lowCase):
            table_name = lowCase[i]+"_cham"

        with engine_cham.begin() as connection:
            connection.execute(text('CREATE TABLE {}('
                                        'tier varchar(5),'
                                        'championName varchar(255),'
                                        'championId varchar(10),'
                                        'teamPosition varchar(10),'
                                        
                                        'match_cnt int(10),'        # 전체 게임
                                        'win_cnt int(10),'
                                        'ban_cnt int(10),'
                                        'pick_cnt int(10),'
                                        
                                        'win_rate float(10),'       # 승률
                                        'ban_rate float(10),'       # 벤률
                                        'pick_rate float(10),'      # 픽률
                                        'av_kda float(10),'         # KDA 평균

                                        'most_priperk1 varchar(255),'
                                        'most_priperk2 varchar(255),'
                                        'most_priperk3 varchar(255),'
                                        'most_priperk4 varchar(255),'
                                        'most_pristyle varchar(255),'

                                        'most_subperk1 varchar(255),'
                                        'most_subperk2 varchar(255),'
                                        'most_substyle varchar(255),'

                                        'abil_def varchar(255),'
                                        'abil_fle varchar(255),'
                                        'abil_off varchar(255),'
                                        
                                        'spell1_1 varchar(255),'
                                        'spell1_2 varchar(255),'
                                        'spell1_cnt int(10),'    # spell1_cnt
                                        'spell1_rate float(4),'  # spell1_cnt/cham_cnt
                                        'spell1_win float(4),'   # spell1_win/spell1_cnt
                                        
                                        'spell2_1 varchar(255),'
                                        'spell2_2 varchar(255),'
                                        'spell2_cnt varchar(255),'
                                        'spell2_rate varchar(255),'
                                        'spell2_win varchar(255),'
                                        
                                        'skill_build1 varchar(255),'
                                        'skill_build2 varchar(255),'
                                        'skill_build3 varchar(255),'
                                        'skill_cnt int(10),'
                                        'skill_rate float(4),'
                                        'skill_win float(4),'
                                       
                                        'item_set1_1 varchar(255),'
                                        'item_set1_2 varchar(255),'
                                        'item_set1_3 varchar(255),'
                                        'item_set1_4 varchar(255),'
                                        'item_set1_5 varchar(255),'
                                        'item_set1_6 varchar(255),'
                                        'item_set1_7 varchar(255),'
                                        'item_set1_8 varchar(255),'
                                        'item_set1_cnt int(10),'
                                        'item_set1_rate float(4),'
                                        'item_set1_win float(4),'
                                        ''
                                        'item_set2_1 varchar(255),'
                                        'item_set2_2 varchar(255),'
                                        'item_set2_3 varchar(255),'
                                        'item_set2_4 varchar(255),'
                                        'item_set2_5 varchar(255),'
                                        'item_set2_6 varchar(255),'
                                        'item_set2_7 varchar(255),'
                                        'item_set2_8 varchar(255),'
                                        'item_set2_cnt int(10),'
                                        'item_set2_rate float(4),'
                                        'item_set2_win float(4),'
                                        
                                        'shoes1 varchar(255),'
                                        'shoes1_cnt int(10),'
                                        'shoes1_rate float(4),'
                                        'shoes1_win float(4),'
                                        
                                        'shoes2 varchar(255),'
                                        'shoes2_cnt int(10),'
                                        'shoes2_rate float(4),'
                                        'shoes2_win float(4),'
                                        
                                        'core1_1 varchar(255),'
                                        'core1_2 varchar(255),'
                                        'core1_3 varchar(255),'
                                        'core1_4 varchar(255),'
                                        'core1_5 varchar(255),'
                                        'core1_6 varchar(255),'
                                        'core1_cnt varchar(255),'
                                        'core1_rate float(4),'
                                        'core1_win float(4),'
                                        
                                        'core2_1 varchar(255),'
                                        'core2_2 varchar(255),'
                                        'core2_3 varchar(255),'
                                        'core2_4 varchar(255),'
                                        'core2_5 varchar(255),'
                                        'core2_6 varchar(255),'
                                        'core2_cnt varchar(255),'
                                        'core2_rate float(4),'
                                        'core2_win float(4),'
                                        
                                        'core3_1 varchar(255),'
                                        'core3_2 varchar(255),'
                                        'core3_3 varchar(255),'
                                        'core3_4 varchar(255),'
                                        'core3_5 varchar(255),'
                                        'core3_6 varchar(255),'
                                        'core3_cnt varchar(255),'
                                        'core3_rate float(4),'
                                        'core3_win float(4));'.format(table_name)))



create_usrinfo()
# create_gameinfo()
# create_gameinfo_new()
# create_chaminfo()
print("성공적으로 테이블 스키마가 만들어 졌습니다.")
# conn_gam.close()