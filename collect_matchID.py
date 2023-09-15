import pandas as pd
import time
import requests
import pymysql.cursors


conn = pymysql.connect(host="127.0.0.1", user="root", password="qwer1234", db="conn_test", charset="utf8")
cur = conn.cursor()

cur.execute('SHOW TABLES')
result = cur.fetchall()
print(result)
result = [list(result[x]) for x in range(len(result))]
print(result)
table_names = []
for i in range(len(result)):
    table_names.append(result[i][0])
print(table_names)

def collect_matchID(table_names):
    usr_info = pd.DataFrame()
    for table_name in table_names:
        if table_name == "challusr_info":
            cur.execute('SELECT * FROM %s', (table_name))
            res = cur.fetchall()
            res = [list(res[x]) for x in range(len(res))]

            for i in range(len(res)):
                usr_info.loc[i] = res[i]


    print(usr_info)
collect_matchID(table_names)