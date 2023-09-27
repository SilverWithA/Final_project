from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import column
from sqlalchemy import select
from sqlalchemy import table
import pandas as pd



# 1. MySQL에 연결 - sqlalchemy
db_connection_str = 'mysql+pymysql://root:qwer1234@127.0.0.1/conn_test'
engine = create_engine(db_connection_str)
conn = engine.connect()
print("1번 연결 설정이 완료되었습니다.")


# # 2. DB에서 데이터 불러오기 - read_sql사용 --> pandas는 sqlalchemy를 통해 read_sql하는 걸 지원
# df4 = pd.read_sql("SELECT * FROM challusr_info",conn, index_col=None)
# # df4 = pd.read_sql(challusr_info,conn, index_col=None) 도 가능
# print("read_sql를 이용해 DB 테이블을 데이터프레임으로 저장했습니다.")
# print(df4)
# print("DB에서 데이터 불러왔습니다.")
#
#
#
# # 3. DB에 테이블 스키마 만들기
# with engine.begin() as connection:
#     # use connection.execute(), not engine.execute() -use the text() construct to execute textual SQL
#     connection.execute(text("CREATE TABLE TEST_TABLE (summorName VARCHAR(255),puuid VARCHAR(255));"))
#
# print("DB에 테이블 스키마 만들었습니다.")
#
#
# # 4. df를 다시 DB에 저장하기: to_sql
# df4.to_sql(name='create_tb', con=conn, if_exists='append',index=False)
# print("TEST_TABLE라는 이름으로 DB에 저장했습니다.")
#
#
# # 5. 저장 확인하기 -select 사용하기
# create_tb = table("create_tb", column("puuid"))
# with engine.begin() as connection:
#     res = connection.execute(select(create_tb.c.puuid))
#     # res = connection.execute(text('SELECT * FROM create_tb;'))
# print(res.fetchall())
# print("잘 저장되었군요. 실습 끝")
# conn.close()

test_list = ['chall_mat','challusr_info']

# 6. iterator로 sql문 수행하기 - sqlalchemy의 formating 방법
# https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text -- 파라미터라 안되는 것 같음
# https://item4.blog/2016-03-30/Truncate-All-Tables-with-SQLAlchemy/
with engine.begin() as connection:
    for i in range(len(test_list)):
        print(test_list[i])
        connection.execute(text("TRUNCATE TABLE {};".format(test_list[i])))
conn.close()