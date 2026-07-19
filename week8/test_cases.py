import pandas as pd

orders=pd.read_csv("data/orders.csv")
order_items=pd.read_csv("data/order_items.csv")

print("Test Case 1: Invalid Order IDs")
invalid_orders=order_items[
    ~order_items["order_id"].isin(orders["order_id"])]
print("Invalid Order IDs:",len(invalid_orders))
print(invalid_orders)



print("\nTest Case 2: Invalid Discount")
invalid_discount=order_items[
    order_items["discount_percent"]>100]
print("Invalid Discounts:",len(invalid_discount))
print(invalid_discount)



print("\nTest Case 3: Quantity Equal to Zero")
zero_quantity=order_items[
    order_items["quantity"]==0]
print("Zero Quantity Records:",len(zero_quantity))
print(zero_quantity)



print("\nTest Case 4: Future Order Dates")
orders["order_date"]=pd.to_datetime(
    orders["order_date"],
    format="mixed")
future_orders=orders[
    orders["order_date"]>pd.Timestamp.today()]
print("Future Orders:",len(future_orders))
print(future_orders)