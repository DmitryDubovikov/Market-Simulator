import time

class Order:
    def __init__(self, order_id, order_type, quantity, price):
        self.order_id = order_id
        self.timestamp = time.time()
        self.type = order_type
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Order(id={self.order_id}, type={self.type}, qty={self.quantity}, price={self.price}, time={self.timestamp})"


def main():
    order = Order(1, 'buy', 5, 100)
    print(order)
    pass


if __name__ == "__main__":
    main()