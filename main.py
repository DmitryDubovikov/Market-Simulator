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

    def __str__(self):
        return f"{self.price} {self.type.value} {self.quantity}"


class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def __str__(self):
        buy_orders_str = ", ".join(str(order) for order in self.buy_orders)
        sell_orders_str = ", ".join(str(order) for order in self.sell_orders)
        return f"Buy Orders: [{buy_orders_str}]\nSell Orders: [{sell_orders_str}]"

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

    def match_orders(self):
        self.buy_orders.sort(key=lambda x: (x.price, x.timestamp))
        self.sell_orders.sort(key=lambda x: (-x.price, x.timestamp))

        matched_orders = []
        while (
            self.buy_orders
            and self.sell_orders
            and self.buy_orders[-1].price >= self.sell_orders[-1].price
        ):
            buy_order = self.buy_orders.pop()
            sell_order = self.sell_orders.pop()

            traded_quantity = min(buy_order.quantity, sell_order.quantity)
            trade_price = round((buy_order.price + sell_order.price) / 2, 2)  # fair

            matched_orders.append(
                {
                    "buy_order_id": buy_order.order_id,
                    "sell_order_id": sell_order.order_id,
                    "quantity": traded_quantity,
                    "price": trade_price,
                }
            )

            if buy_order.quantity > traded_quantity:
                buy_order.quantity -= traded_quantity
                self.buy_orders.append(buy_order)
            elif sell_order.quantity > traded_quantity:
                sell_order.quantity -= traded_quantity
                self.sell_orders.append(sell_order)

        return matched_orders


def generate_random_order():
    order_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    order_type = random.choice([OrderType.BUY, OrderType.SELL])
    quantity = random.randint(1, 100)
    # price = round(random.uniform(1, 100), 2)
    price = round(random.uniform(1, 100), 0)
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

    def test_match_orders(self):
        buy_orders = [
            Order(1, OrderType.BUY, 10, 100),
            Order(2, OrderType.BUY, 8, 110),
            Order(3, OrderType.BUY, 12, 95),
        ]

        sell_orders = [
            Order(4, OrderType.SELL, 5, 120),
            Order(5, OrderType.SELL, 15, 105),
        ]

        for order in buy_orders + sell_orders:
            self.order_book.add_order(order)

        matched_trades = self.order_book.match_orders()

        self.assertEqual(len(matched_trades), 1)

        self.assertEqual(matched_trades[0]["buy_order_id"], 2)
        self.assertEqual(matched_trades[0]["sell_order_id"], 5)
        self.assertEqual(matched_trades[0]["quantity"], 8)
        self.assertEqual(matched_trades[0]["price"], 107.5)


def main():
    # order = generate_random_order()
    # print(order)

    order_book = OrderBook()

    for _ in range(10):
        order = generate_random_order()
        order_book.add_order(order)

    print(order_book)
    print("---------------------------")
    print("start trading...")
    print("---------------------------")

    matched_orders = order_book.match_orders()
    print(f"matched orders:\n{matched_orders}")
    print(f"order book:\n{order_book}")

    for _ in range(2):
        print("---------------------------")
        order = generate_random_order()
        print(f"new order:\n{order}")
        order_book.add_order(order)
        matched_orders = order_book.match_orders()
        print(f"matched orders:\n{matched_orders}")
        print(f"order book:\n{order_book}")


if __name__ == "__main__":
    main()
