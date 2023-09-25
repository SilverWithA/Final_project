import pandas as pd
import pymysql.cursors

# db에 넣어줄 test data 생성
df = pd.DataFrame({'A':['가','나','다'],
                              'B':['1','2','3']})
# print(df)

# MySQL과 기본 연결 옵션 설정
conn = pymysql.connect(host="127.0.0.1", user="root", password="qwer1234", db="conn_test", charset="utf8")
cur = conn.cursor()

# # 테이블 만들기
# cur.execute("CREATE TABLE test_table (summonerName varchar(255),puuid varchar(255))")
# # Insert 쿼리 날려서 data 삽입
# for i in range(len(df)):
#     cur.execute('INSERT INTO test_table VALUES(%s, %s)', (str(df['A'][i]), str(df['B'][i])))


# # Insert한 쿼리를 db에 반영:commit
# conn.commit()
# df2 = pd.Data()
cur.execute('SELECT * FROM test_table')
result = cur.fetchall()
print(result)

convert = [list(result[x]) for x in range(len(result))]
print("이중리스트 형식으로 변환: ", convert)
df3 = pd.DataFrame(columns=['summonerName', 'puuid'])

for i in range(len(convert)):
    df3.loc[i] = convert[i]

print(df3)
conn.close()

