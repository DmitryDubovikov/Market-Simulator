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
        return (
            f"Order(id={self.order_id}, type={self.type}, qty={self.quantity}, "
            f"price={self.price}, time={self.timestamp})"
        )


class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.type == OrderType.BUY:
            self.buy_orders.append(order)
        elif order.type == OrderType.SELL:
            self.sell_orders.append(order)

    def remove_order(self, order):
        if order in self.buy_orders:
            self.buy_orders.remove(order)
        elif order in self.sell_orders:
            self.sell_orders.remove(order)


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
        expected_repr = (
            f"Order(id={order.order_id}, type={order.type}, qty={order.quantity}, "
            f"price={order.price}, time={order.timestamp})"
        )
        self.assertEqual(repr(order), expected_repr)

    def test_invalid_order_type(self):
        with self.assertRaises(ValueError):
            Order(1, "invalid", 3, 150)


class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.order_book = OrderBook()

    def test_add_buy_order(self):
        buy_order = Order(1, OrderType.BUY, 10, 100)
        self.order_book.add_order(buy_order)
        self.assertEqual(len(self.order_book.buy_orders), 1)
        self.assertEqual(len(self.order_book.sell_orders), 0)

    def test_add_sell_order(self):
        sell_order = Order(2, OrderType.SELL, 5, 200)
        self.order_book.add_order(sell_order)
        self.assertEqual(len(self.order_book.buy_orders), 0)
        self.assertEqual(len(self.order_book.sell_orders), 1)

    def test_remove_order(self):
        buy_order = Order(1, OrderType.BUY, 10, 100)
        self.order_book.add_order(buy_order)
        self.order_book.remove_order(buy_order)
        self.assertEqual(len(self.order_book.buy_orders), 0)
        self.assertEqual(len(self.order_book.sell_orders), 0)


def main():
    order = generate_random_order()
    print(order)
    pass


if __name__ == "__main__":
    main()
