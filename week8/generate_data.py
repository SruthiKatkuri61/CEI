from faker import Faker 
import random
import pandas as pd
from datetime import datetime,timedelta

# customers.csv

fake=Faker()
#print(fake.name())
customers=[]
customer_types=["Regular","Premium","VIP"]
start_year=2023
start_date=datetime(start_year,1,1)
end_date=datetime.today()
days=(end_date-start_date).days
no_of_customers=500
for i in range(1,no_of_customers+1):
    customer_id=f"C{i:03d}"
    customer_name=fake.name()
    email=fake.email()
    customer_type=random.choice(customer_types)
    random_days=random.randint(0,days)
    registration_days=start_date+(timedelta(days=random_days))
    customer={
        "customer_id":customer_id,
        "customer_name":customer_name,
        "email":email,
        "customer_type":customer_type,
        "registration_date":registration_days.date()
    }
    customers.append(customer)
customer_df=pd.DataFrame(customers)
customer_df.to_csv("data/customers.csv",index=False)  #default index will be coming when exportong and creating
print("generated")



# products.csv
num_of_products=500
products=[]
category_subcategory={"Electronics":["Laptop","Mobile","Keyboard","Mouse","Printer","Speaker","Webcam","Headphones"],"Clothing":["T-shirt","Shirt","Jeans","Saree","Kurta","Shorts"],"Home":["Chair","Table","Sofa","Pillow","Mattress","Fan"],"Books":["Novel","Dictionary","Notebook","Textbook","Journal","Story Book","Comic"]}
BRANDS = {
    "Electronics": ["Dell", "HP", "Lenovo", "Samsung", "Sony"],
    "Clothing": ["Nike", "Adidas", "Puma", "Levi's"],
    "Home": ["IKEA", "Prestige", "Home Centre"],
    "Books": ["Penguin", "Oxford", "McGraw Hill"]
}
for i in range(1,num_of_products+1):
    product_id=f"P{i:03d}"
    category=random.choice(list(category_subcategory.keys()))
    sub_category=random.choice(category_subcategory[category])
    brand = random.choice(BRANDS[category])
    product_name = f"{brand} {sub_category}"    
    cost_price=random.randint(100,50000)
    product={
        "product_id":product_id,
        "product_name":product_name,
        "category":category,
        "subcategory":sub_category,
        "cost_price":cost_price
    }
    products.append(product)
products_df=pd.DataFrame(products)
products_df.to_csv("data/products.csv",index=False)
print("generated")


#orders.csv

num_of_orders=500
status_order=["Placed","shipped","delivered","cancelled","returned"]
region=["North","south","west","east"]
orders=[]
for i in range(1,num_of_orders+1):
    order_id=f"O{i:03d}"
    customer_id=f"C{random.randint(1,no_of_customers):03d}"
    if random.random()<0.05:
        customer_id=None
    status=random.choice(status_order)
    region_code=random.choice(region)
    random_days=random.randint(0,days)
    random_seconds=random.randint(0,86399)
    order_date=start_date+timedelta(days=random_days,seconds=random_seconds)
    if random.random() < 0.05:
        order_date = order_date.strftime("%d-%m-%Y %H:%M:%S")
    else:
        order_date = order_date.strftime("%Y-%m-%d %H:%M:%S")


    order = {
    "order_id": order_id,
    "customer_id": customer_id,
    "order_date": order_date,
    "status": status,
    "region_code": region_code
    }

    orders.append(order)
orders_df = pd.DataFrame(orders)

orders_df.to_csv("data/orders.csv", index=False)

print("orders.csv generated successfully!")
print(len(orders_df))



#order_items.csv

num_of_items=1000
order_items=[]
for i in range(1,num_of_items+1):
    item_id=f"I{i:03d}"
    order_id=f"O{random.randint(1,num_of_orders):03d}"
    product_id=f"P{random.randint(1,num_of_products):03d}"
    quantity=random.randint(1,5)
    if random.random()<0.03:
        quantity=-quantity
    unit_price=random.randint(200,60000)
    discount_per=random.randint(0,100)
    order_item={
        "item_id":item_id,
        "order_id":order_id,
        "product_id":product_id,
        "quantity":quantity,
        "unit_price":unit_price,
        "discount_percent":discount_per    }
    order_items.append(order_item)
order_items_df=pd.DataFrame(order_items)
order_items_df.to_csv("data/order_items.csv",index=False)
print("genereated")