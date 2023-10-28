import random
import string
import time
import unittest
from enum import Enum


class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"


class Order:
    def __init__(self, order_id, order_type, quantity, price):
        if not isinstance(order_type, OrderType):
            raise ValueError(
                "Invalid value for order_type. Allowed values: OrderType.BUY or OrderType.SELL"
            )
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


class TestOrder(unittest.TestCase):
    def test_order_creation(self):
        order = Order(1, OrderType.BUY, 10, 100)
        self.assertEqual(order.order_id, 1)
        self.assertEqual(order.type, OrderType.BUY)
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.price, 100)

    def test_order_representation(self):
        order = Order(1, OrderType.SELL, 5, 200)
        expected_repr = f"Order(id={order.order_id}, type={order.type}, qty={order.quantity}, price={order.price}, time={order.timestamp})"
        self.assertEqual(repr(order), expected_repr)

    def test_invalid_order_type(self):
        with self.assertRaises(ValueError):
            Order(1, "invalid", 3, 150)


def main():
    order = generate_random_order()
    print(order)
    pass


if __name__ == "__main__":
    main()
