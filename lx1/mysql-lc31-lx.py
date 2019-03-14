import pymysql
con=pymysql.connect(host="localhost",user="root",password="ac258jwk",database="lc31",charset="utf8")
cursor=con.cursor()
sql="select * from lx;"
rows=cursor.execute(sql)
sql1="insert into lx(data_id) value(3);"
sql2="update lx set temp=12 where data_id=3;"
cursor.execute(sql1)
cursor.execute(sql2)
rows=cursor.execute(sql)
d1=cursor.fetchone()
d2=cursor.fetchone()
d3=cursor.fetchone()
con.commit()
cursor.close()
con.close()
#replace into test_tbl (id,dr) values (1,'2'),(2,'3'),...(x,'y')
