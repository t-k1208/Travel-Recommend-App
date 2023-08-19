# https://qiita.com/yokotate/items/cec2dfcdfe88e37b82dd
import psycopg2
import pickle

path = "localhost"
port = "5432"
dbname = "test_travel"
user = "postgres"
password = "zprjyH5j"

conText = "host={} port={} dbname={} user={} password={}"
conText = conText.format(path,port,dbname,user,password)

connection = psycopg2.connect(conText)
cur = connection.cursor()

## テーブルを削除する SQL を準備
#sql = 'DROP TABLE travel_spot'
## SQL を実行し、テーブル削除
#cur.execute(sql)
## コミットし、変更を確定する
#connection.commit()

# テーブルを作成する SQL を準備
sql = "CREATE TABLE travel_spot (id serial, spot VARCHAR(100), PRIMARY KEY (id));" 
# SQL を実行し、テーブル作成
cur.execute(sql)
# コミットし、変更を確定する
connection.commit()

# 登録する観光地のリストをロード
with open("./travel/data/title_list_2.pkl", "rb") as f:
    title_list = pickle.load(f)
# テーブルに保存
for title in title_list:
    sql = "insert into travel_spot(spot) values('{}');".format(title)
    cur.execute(sql)
    connection.commit()