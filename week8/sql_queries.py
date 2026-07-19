import sqlite3
conn=sqlite3.connect("ecommerce.db")
cursor=conn.cursor()
print("1. Total revenue per category (revenue = quantity × unit_price × (1 - discount_percent/100)) ")
query1="""select p.category,round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as total_revenue from products p 
join order_items oi on p.product_id=oi.product_id group by p.category order by total_revenue desc;"""
cursor.execute(query1)
for row in cursor.fetchall():
    print(row)

print("2. Top 10 customers by total order value ")
query2="""select c.customer_id,c.customer_name,round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as total_order_value from customers c
join orders o on c.customer_id=o.customer_id
join order_items oi on o.order_id=oi.order_id
group by c.customer_id,c.customer_name order by total_order_value desc limit 10;"""
cursor.execute(query2)
for row in cursor.fetchall():
    print(f"Customer ID:{row[0]} | Name:{row[1]}|total order value:{row[2]}")

print("3. Month-wise order count for the last 12 months")
query3=""" select strftime('%Y-%m',order_date) as month,count(order_id) as total_orders from orders where order_date>=date('now','-12 months') 
group by strftime('%Y-%m',order_date) order by month;"""
cursor.execute(query3)
for row in cursor.fetchall():
    print(f"Month:{row[0]} | Total Orders:{row[1]}")

print("4. Find customers who placed orders but never had any item delivered ")
query4=""" select distinct c.customer_id,c.customer_name from customers c join orders o on c.customer_id=o.customer_id 
where c.customer_id not in(select customer_id from orders where status='DELIVERED');"""
cursor.execute(query4)
for row in cursor.fetchall():
    print(f"Customer ID: {row[0]} | Name: {row[1]}")

print("5. Products that were ordered but had more returns than purchases")
query5="""select p.product_id,p.product_name,sum(case when oi.quantity>0 then oi.quantity else 0 end)
as total_purchases,abs(sum(case when oi.quantity<0 then oi.quantity else 0 end)) as total_returns 
from products p join order_items oi on p.product_id=oi.product_id group by p.product_id,p.product_name having total_returns>total_purchases
order by total_returns desc;"""
cursor.execute(query5)
rows=cursor.fetchall()
for row in rows:
    print(f"Product ID:{row[0]}|" f"Product :{row[1]}|" f"Purchases:{row[2]}|" f"returns:{row[3]}")

print("6. Calculate the return rate(returned items/total items) per category")
query6="""select p.category,
round((abs(sum(case when oi.quantity<0 then oi.quantity else 0 end))*100.0)/sum(abs(oi.quantity)),2)
as return_rate
from products p join order_items oi
on p.product_id=oi.product_id
group by p.category
order by return_rate desc;"""

cursor.execute(query6)
rows=cursor.fetchall()

for row in rows:
    print(f"Category:{row[0]}|" f"Return Rate:{row[1]}%")


print("7. Running total of revenue per region")

query7="""select region_code,order_date,daily_revenue,
sum(daily_revenue) over(partition by region_code order by order_date) as running_total
from
(select o.region_code,date(o.order_date) as order_date,
round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as daily_revenue
from orders o join order_items oi
on o.order_id=oi.order_id
group by o.region_code,date(o.order_date)
) t
order by region_code,order_date;"""

cursor.execute(query7)
rows=cursor.fetchall()

for row in rows:
    print(f"Region:{row[0]}|" f"Date:{row[1]}|" f"Daily Revenue:{row[2]}|" f"Running Total:{row[3]}")


print("8. Rank products by total revenue within each category")

query8="""select category,product_name,total_revenue,
dense_rank() over(partition by category order by total_revenue desc) as rank_in_category
from
(select p.category,p.product_name,
round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as total_revenue
from products p join order_items oi
on p.product_id=oi.product_id
group by p.category,p.product_name
) t
order by category,rank_in_category;"""

cursor.execute(query8)
rows=cursor.fetchall()

for row in rows:
    print(f"Category:{row[0]}|" f"Product:{row[1]}|" f"Revenue:{row[2]}|" f"Rank:{row[3]}")


print("9. Days between consecutive orders(LAG Analysis)")

query9="""select customer_id,order_date,previous_order_date,days_gap,
case when avg(days_gap) over(partition by customer_id)>30 then 'At Risk'
else 'Safe'
end as customer_status
from
(select customer_id,date(order_date) as order_date,
lag(date(order_date)) over(partition by customer_id order by date(order_date)) as previous_order_date,
julianday(date(order_date))-julianday(lag(date(order_date)) over(partition by customer_id order by date(order_date))) as days_gap
from orders
where customer_id!='UNKNOWN'
) t
order by customer_id,order_date;"""

cursor.execute(query9)
rows=cursor.fetchall()

for row in rows:
    print(f"Customer ID:{row[0]}|" f"Order Date:{row[1]}|" f"Previous Order:{row[2]}|" f"Days Gap:{row[3]}|" f"Status:{row[4]}")


print("10. CTE with Multiple Levels")

query10="""with monthly_revenue as
(select o.customer_id,
strftime('%Y-%m',o.order_date) as month,
round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as revenue
from orders o join order_items oi
on o.order_id=oi.order_id
where o.customer_id!='UNKNOWN'
group by o.customer_id,strftime('%Y-%m',o.order_date)),

customer_category as
(select customer_id,month,revenue,
case
when revenue>10000 then 'High'
when revenue between 5000 and 10000 then 'Medium'
else 'Low'
end as category
from monthly_revenue)

select month,category,count(customer_id) as customer_count
from customer_category
group by month,category
order by month,category;"""

cursor.execute(query10)
rows=cursor.fetchall()

for row in rows:
    print(f"Month:{row[0]}|" f"Category:{row[1]}|" f"Customers:{row[2]}")


print("11. NTILE for Customer Segmentation")

query11="""select customer_id,total_value,quartile,
case
when quartile=1 then 'Platinum'
when quartile=2 then 'Gold'
when quartile=3 then 'Silver'
else 'Bronze'
end as quartile_label
from
(select customer_id,total_value,
ntile(4) over(order by total_value desc) as quartile
from
(select o.customer_id,
round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as total_value
from orders o join order_items oi
on o.order_id=oi.order_id
where o.customer_id!='UNKNOWN'
group by o.customer_id
)t1
)t2;"""

cursor.execute(query11)
rows=cursor.fetchall()

for row in rows:
    print(f"Customer ID:{row[0]}|" f"Total Value:{row[1]}|" f"Quartile:{row[2]}|" f"Label:{row[3]}")



print("12. Year-over-Year Comparison")

query12="""with monthly_revenue as
(select strftime('%Y',o.order_date) as year,
strftime('%m',o.order_date) as month,
round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as revenue
from orders o join order_items oi
on o.order_id=oi.order_id
group by strftime('%Y',o.order_date),strftime('%m',o.order_date))

select m1.year,m1.month,m1.revenue,
coalesce(m2.revenue,0) as prev_year_revenue,
case
when m2.revenue is null or m2.revenue=0 then null
else round(((m1.revenue-m2.revenue)*100.0/m2.revenue),2)
end as yoy_growth_percent
from monthly_revenue m1
left join monthly_revenue m2
on m1.month=m2.month
and cast(m1.year as integer)=cast(m2.year as integer)+1
order by m1.year,m1.month;"""

cursor.execute(query12)
rows=cursor.fetchall()

for row in rows:
    print(f"Year:{row[0]}|" f"Month:{row[1]}|" f"Revenue:{row[2]}|" f"Previous Year Revenue:{row[3]}|" f"YoY Growth:{row[4]}")


print("13. First/Last Value Analysis")

query13="""with customer_orders as
(select o.customer_id,o.order_date,p.category,
first_value(p.category) over(partition by o.customer_id order by o.order_date) as first_category,
first_value(p.category) over(partition by o.customer_id order by o.order_date desc) as last_category
from orders o join order_items oi
on o.order_id=oi.order_id
join products p
on oi.product_id=p.product_id
where o.customer_id!='UNKNOWN')

select distinct customer_id,first_category,last_category,
case
when first_category=last_category then 'No'
else 'Yes'
end as category_shift
from customer_orders
order by customer_id;"""

cursor.execute(query13)
rows=cursor.fetchall()

for row in rows:
    print(f"Customer ID:{row[0]}|" f"First Category:{row[1]}|" f"Last Category:{row[2]}|" f"Category Shift:{row[3]}")


print("14. Cumulative Distribution")

query14="""with customer_revenue as
(select o.customer_id,
round(sum(oi.quantity*oi.unit_price*(1-oi.discount_percent/100.0)),2) as revenue
from orders o join order_items oi
on o.order_id=oi.order_id
where o.customer_id!='UNKNOWN'
group by o.customer_id)

select customer_id,revenue,
sum(revenue) over(order by revenue desc) as cumulative_revenue,
round((sum(revenue) over(order by revenue desc)*100.0)/(sum(revenue) over()),2) as cumulative_percent
from customer_revenue
order by revenue desc;"""

cursor.execute(query14)
rows=cursor.fetchall()

for row in rows:
    print(f"Customer ID:{row[0]}|" f"Revenue:{row[1]}|" f"Cumulative Revenue:{row[2]}|" f"Cumulative Percent:{row[3]}%")



print("15. Complex CTE - Cohort Analysis")

query15="""with cohort_data as
(select c.customer_id,
strftime('%Y-%m',c.registration_date) as cohort_month,
((cast(strftime('%Y',o.order_date) as integer)-cast(strftime('%Y',c.registration_date) as integer))*12+
(cast(strftime('%m',o.order_date) as integer)-cast(strftime('%m',c.registration_date) as integer))) as month_number
from customers c join orders o
on c.customer_id=o.customer_id
where o.customer_id!='UNKNOWN'),

cohort_summary as
(select cohort_month,month_number,
count(distinct customer_id) as customers
from cohort_data
where month_number between 0 and 3
group by cohort_month,month_number),

cohort_size as
(select cohort_month,
count(distinct customer_id) as total_customers
from cohort_data
group by cohort_month)

select cs.cohort_month,cs.month_number,cs.customers,
round(cs.customers*100.0/cs1.total_customers,2) as retention_rate
from cohort_summary cs join cohort_size cs1
on cs.cohort_month=cs1.cohort_month
order by cs.cohort_month,cs.month_number;"""

cursor.execute(query15)
rows=cursor.fetchall()

for row in rows:
    print(f"Cohort:{row[0]}|" f"Month:{row[1]}|" f"Customers:{row[2]}|" f"Retention Rate:{row[3]}%")



print("16. Frequently Bought Together Products")

query16="""select
p1.product_name as product_a,
p2.product_name as product_b,
count(*) as times_bought_together
from order_items oi1
join order_items oi2
on oi1.order_id=oi2.order_id
and oi1.product_id<oi2.product_id
join products p1
on oi1.product_id=p1.product_id
join products p2
on oi2.product_id=p2.product_id
group by p1.product_name,p2.product_name
order by times_bought_together desc;"""

cursor.execute(query16)
rows=cursor.fetchall()

for row in rows:
    print(f"Product A:{row[0]}|" f"Product B:{row[1]}|" f"Times Bought Together:{row[2]}")

conn.close()