#%%
import psycopg2
import pandas as pd

def execute(query):
    pc.execute(query)
    return pc.fetchall()


#아래 정보를 입력
user = 'postgres' # insert ID Here
password = 'bbanal*123' # insert password
host_product = 'database-1.ct0x8ni2zybc.ap-northeast-2.rds.amazonaws.com' # insert hose endpoint
dbname = 'postgres' # insert dbname
port='5432' # insert port here

product_connection_string = "dbname={dbname} user={user} host={host} password={password} port={port}"\
                            .format(dbname=dbname,
                                    user=user,
                                    host=host_product,
                                    password=password,
                                    port=port)    
try:
    product = psycopg2.connect(product_connection_string)
except:
    print("I am unable to connect to the database")

pc = product.cursor()

#%%

#쿼리 입력
query = """
select * from test_table
"""

query = "select * from test_table"
#일반적인 쿼리 조회 방법
result = execute(query)

#pandas를 통한 조회 방법
aaaa = pd.read_sql(query, product)

print(aaaa)
