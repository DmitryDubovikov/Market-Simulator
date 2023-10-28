import random
import string
import time
from enum import Enum


class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"


class Order:
    def __init__(self, order_id, order_type, quantity, price):
        self.order_id = order_id
        self.timestamp = time.time()
        self.type = order_type
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Order(id={self.order_id}, type={self.type}, qty={self.quantity}, price={self.price}, time={self.timestamp})"


def generate_random_order():
    order_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    order_type = random.choice([OrderType.BUY, OrderType.SELL])
    quantity = random.randint(1, 100)
    price = random.uniform(1, 100)
    return Order(order_id, order_type, quantity, price)


def main():
    order = generate_random_order()
    print(order)
    pass


if __name__ == "__main__":
    main()
