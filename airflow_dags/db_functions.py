import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy import text





# [0]. DB 연결 설정
# MySQL ----------------------------------------------------------------
# 1. usrinfo
db_conn_Usr= 'mysql+pymysql://root:qwer1234@127.0.0.1/usrinfo'
engine_Usr = create_engine(db_conn_Usr)
conn_Usr = engine_Usr.connect()

# 2. GameInfo DB 연결 설정
GameInfo_str= 'mysql+pymysql://root:qwer1234@127.0.0.1/gameinfo'
engine_gam = create_engine(GameInfo_str)
conn_gam = engine_gam.connect()

# 3. chaminfo DB 연결 설정
ChamInfo_str= 'mysql+pymysql://root:qwer1234@127.0.0.1/chaminfo'
engine_cham = create_engine(ChamInfo_str)
conn_cham = engine_cham.connect()

# MongoDB ----------------------------------------------------------------
client = MongoClient('mongodb://localhost:27017/')

# mat_info DB 연결 설정
db_mat = client.mat_info
coll_mat = db_mat.matchIds

# raw_info DB 연결 설정
db_raw = client.raw_info



# [1] 함수 정의하기
# 1. DB에 았는 모든 테이블 조회 -> 테이블 이름 convert로 반환
# show tables
def show_tables(engine_name):
    """연결하고자하는 DB의 engine 변수를 engine_name에 설정(ex.engine_mat,engine_gam) """
    with engine_name.begin() as connection:
        res = connection.execute(text("SHOW TABLES;"))
    # print("DB에 존재하는 모든 table를 조회합니다.")
    tables = res.fetchall()

    # 인덱싱을 위해 2중 list로 변환
    convert = [list(tables[x]) for x in range(len(tables))]
    # print(convert[0][0])   # 인덱싱
    return convert

# 2. 이미 DB에 있는 정보 삭제하여 테이블 비우기: truncate
def trun_tables(engine_name):
    """연결하고자하는 DB의 engine 변수를 engine_name에 설정"""

    # DB에 존재하는 table이름들을 usr_talbes 변수에 저장
    db_talbes = show_tables(engine_name)

    db_tables = show_tables(engine_name)
    with engine_name.begin() as connection:
        for i in range(len(db_tables)):
            # 스키마는 유지하되 테이블 용량은 삭제하기 위해 truncate 구문 사용
            connection.execute(text("TRUNCATE TABLE {};".format(str(db_tables[i][0]))))
    print(engine_name, "에 존재하는 모든 테이블의 데이터를 삭제 완료하였습니다.")

# 3. DB에 저장된 정보를 dataFrame으로 불러오기
def select_db(table_name,conn_name):
    """conn_name에는 연결하고자하는 db의 conn변수를 입력(ex conn_mat)
    table_name은 해당 db에 있는 table이름을 지정해주면 된다"""

    select_df = pd.read_sql(table_name,conn_name, index_col=None)
    return select_df
