import numpy as np
import bisect
from classes.trader import TraderModel
from classes.news import NewsSpreadModel

class MarketModel:
    def __init__(self, num_traders=700, time_steps=200, stock_price=100):
        # Initialize the model with a given number of traders, time steps, and an initial stock price.
        self.traders = [TraderModel(index=i, stock_price=stock_price) for i in range(num_traders)]
        self.stock_price = stock_price
        self.buy_orders = []  # List to store buy orders
        self.sell_orders = []  # List to store sell orders
        self.stock_price_history = []  # Track the history of stock prices
        self.time_steps = time_steps
        self.news_model = NewsSpreadModel(num_traders=num_traders, time_steps=self.time_steps)

    def get_time_steps(self):
        # Return the number of time steps
        return  self.time_steps

    def update_stock_price(self):
        # Update the stock price based on the highest buy order and the lowest sell order
        if self.buy_orders and self.sell_orders:
            highest_buy = self.buy_orders[-1]
            lowest_sell = self.sell_orders[0]
            self.stock_price = (highest_buy + lowest_sell) / 2
        self.stock_price_history.append(self.stock_price)

    def execute_orders(self):
        # Match and execute buy and sell orders
        while self.buy_orders and self.sell_orders and self.buy_orders[-1] >= self.sell_orders[0]:
            self.buy_orders.pop()  # Remove the executed buy order
            self.sell_orders.pop(0)  # Remove the executed sell order

    def get_current_price(self):
        # Return the current stock price
        if not self.stock_price_history:
            return self.stock_price
        else:
            return self.stock_price_history[-1]

    def simulate_market(self):
        # Simulate the market for the given number of time steps
        self.news_model.spread_news()  # Spread news among traders
        matrix_states = self.news_model.incremented_time_states()

        for day in range(self.time_steps):
            # In the second half of the simulation, influence traders based on news
            if day >= self.time_steps / 2:
                news_magnitude = 1
                for trader in self.traders:
                    trader.receive_news(news_magnitude if matrix_states[day - int(self.time_steps / 2) - 1][trader.index] == 1 else 0,
                                        self.get_current_price())
            self.collect_and_execute_orders()
            self.update_stock_price()  # Update the stock price at each time step

    def collect_and_execute_orders(self):
        # Collect orders from all traders and execute them
        for trader in self.traders:
            order_type, order_price = trader.place_limit_order(self.get_current_price())
            if order_type == 'buy':
                bisect.insort(self.buy_orders, order_price)  # Insert buy order in sorted order
            elif order_type == 'sell':
                bisect.insort(self.sell_orders, order_price)  # Insert sell order in sorted order
        self.execute_orders()

    def get_time_series(self):
        # Generate time series data for stock prices
        return [{'x': index, 'y': price} for index, price in enumerate(self.stock_price_history)]
