import sqlite3
import pandas as pd
conn=sqlite3.connect("ecommerce.db")
print("Database created successfully")
customers=pd.read_csv("data/customers.csv")
products=pd.read_csv("data/products.csv")
orders=pd.read_csv("data/orders.csv")
order_items=pd.read_csv("data/order_items.csv")

customers.to_sql("customers",conn,if_exists="replace",index=False)

products.to_sql("products",conn,if_exists="replace",index=False)

orders.to_sql("orders",conn,if_exists="replace",index=False)

order_items.to_sql("order_items",conn,if_exists="replace",index=False)

print("Database created successfully")

cursor=conn.cursor()
cursor.execute(""" select name from sqlite_master where type='table';""")
tables=cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(table[0])