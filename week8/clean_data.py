import pandas as pd
import re
customers=pd.read_csv("data/customers.csv")
products=pd.read_csv("data/products.csv")
orders=pd.read_csv("data/orders.csv")
order_items=pd.read_csv("data/order_items.csv")

def validate_emails(customers):
    pattern=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    customers["valid_email"]=customers["email"].str.match(pattern)
    invalid_emails=customers[customers["valid_email"]==False]
    print("Invalid emails found:",len(invalid_emails))
    return customers
customers=validate_emails(customers)
print(customers.head())


def clean_products(products):
    print("\nBefore Cleaning:")
    print(products["product_name"].head())
    products["product_name"]=products["product_name"].str.strip()
    products["product_name"]=products["product_name"].str.title()
    print("After Cleaning:")
    print(products["product_name"].head())
    return products

products=clean_products(products)


def clean_orders(orders):
    print("Missing customer IDs:",orders["customer_id"].isnull().sum())
    orders["customer_id"]=orders["customer_id"].fillna("UNKNOWN")
    orders["order_date"]=pd.to_datetime(orders["order_date"],format="mixed")
    print("\nAfter cleaning :")
    print("Missing customer IDs:",orders["customer_id"].isnull().sum())
    print(orders.head(10))
    return orders

orders=clean_orders(orders)


def check_referential_integrity(customers,products,orders,order_items):
    invalid_customers=orders[(~orders["customer_id"].isin(customers["customer_id"]))&(orders["customer_id"]!="UNKNOWN")]
    invalid_orders=order_items[~order_items["order_id"].isin(orders["order_id"])]
    invalid_products=order_items[~order_items["product_id"].isin(products["product_id"])]
    print("refernetial integrity report")
    print("Invalid Customer_ids:",len(invalid_customers))
    print("Invalid Order IDs:",len(invalid_orders))
    print("Invalid Product IDs:",len(invalid_products))

    return customers,products,orders,order_items

customers,products,orders,order_items=check_referential_integrity(customers,products,orders,order_items)

import os

os.makedirs("cleaned_data", exist_ok=True)

customers.to_csv("cleaned_data/customers_cleaned.csv", index=False)
products.to_csv("cleaned_data/products_cleaned.csv", index=False)
orders.to_csv("cleaned_data/orders_cleaned.csv", index=False)
order_items.to_csv("cleaned_data/order_items_cleaned.csv", index=False)

print("Cleaned datasets saved successfully!")