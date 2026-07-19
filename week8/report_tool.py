import sqlite3
conn=sqlite3.connect("ecommerce.db")
cursor=conn.cursor()
report_type=input("Enter report type(daily/weekly/monthly): ").lower()
start_date=input("Enter start date(YYYY-MM-DD): ")
end_date=input("Enter end date(YYYY-MM-DD): ")

query1="""select count(*) from orders
where date(order_date) between ? and ?;"""
cursor.execute(query1,(start_date,end_date))
total_orders=cursor.fetchone()[0]
print("Total Orders:",total_orders)


query2="""select round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2)
from orders o join order_items oi
on o.order_id=oi.order_id
where date(o.order_date) between ? and ?;"""
cursor.execute(query2,(start_date,end_date))
total_revenue=cursor.fetchone()[0]
print("Total Revenue:",total_revenue)

query3="""select count(distinct customer_id)
from orders
where customer_id!='UNKNOWN'
and date(order_date) between ? and ?;"""
cursor.execute(query3,(start_date,end_date))
unique_customers=cursor.fetchone()[0]
print("Unique Customers:",unique_customers)


query4="""select p.product_name,
round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as revenue
from orders o join order_items oi on o.order_id=oi.order_id
join products p on oi.product_id=p.product_id
where date(o.order_date) between ? and ? group by p.product_name order by revenue desc limit 3;"""
cursor.execute(query4,(start_date,end_date))
rows=cursor.fetchall()
print("Top 3 Products:")
for row in rows:
    print(f"Product:{row[0]}|" f"Revenue:{row[1]}")



query5="""select round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2)
from orders o join order_items oi on o.order_id=oi.order_id
where date(o.order_date) between date(?,'-'||(julianday(?)-julianday(?)+1)||' days') and date(?,'-1 day');"""
cursor.execute(query5,(start_date,end_date,start_date,start_date))
previous_revenue=cursor.fetchone()[0]
if previous_revenue is None:
    previous_revenue=0
print("Previous Period Revenue:",previous_revenue)
if previous_revenue==0:
    print("Revenue Change: N/A")
else:
    revenue_change=round(((total_revenue-previous_revenue)/previous_revenue)*100,2)
    print("Revenue Change:",revenue_change,"%")