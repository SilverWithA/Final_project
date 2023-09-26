from db_functions import *
from sqlalchemy import create_engine
from sqlalchemy import text


tiers = ["chall","grand","mast",
              "dia","em","pla",
              "gold","sil","bro","iron"]

def create_usrinfo():
    """usrinfo DB에 table 스키마 만들기"""

    for i in range(len(tiers)):

        table_name = tiers[i] + "_usrinfo"
        print(table_name)
        with engine_Usr.begin() as connection:
            connection.execute(text('CREATE TABLE {}('
                                    'summnorName varchar(18) NOT NULL,'
                                    'puuid varchar(255) NOT NULL;'))

def create_matinfo():
    for i in range(len(tiers)):
        table_name = tiers[i]+"_mat"
        print(table_name)
        with engine_mat.begin() as connection:
            connection.execute(text('CREATE TABLE {}('
                                    'matchID varchar(255) NOT NULL);'.format(table_name)))
def create_gameinfo():
    for i in range(len(tiers)):
        for j in range(3):
            if j == 0:
                table_name= tiers[i] + "_Aram"
            elif j == 1:
                table_name = tiers[i] + "_win"
            else:
                table_name = tiers[i] + "_lose"

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
                                        'bans varchar(255));'.format(table_name)))



# create_usrinfo()
# create_matinfo()
create_gameinfo()
conn_Usr.close()