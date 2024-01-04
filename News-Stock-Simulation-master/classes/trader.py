import numpy as np

# multiplier is basically goodness or badness of news, if it can be quantified.
MULTIPLIER = 15

class TraderModel:
    def __init__(self, index, stock_price):
        self.index = index  # Unique identifier for each trader
        self.kt = 0  # knowledge of news, initially no news is known
        self.st = np.random.beta(a=2, b=1)  # sensitivity to news, follows a beta distribution
        self.pvos = np.random.normal(stock_price, 10)  # perceived value of stock, initialized near the actual stock price
        self.lop = 0.005  # p0, limit order probability, a small chance to place a limit order

    def update_perceived_value(self, current_price, news_magnitude=0):
        # note mean of beta(2,1) is 2/3
        # Adjusts perceived value based on news and current price
        self.pvos += self.st * self.kt * news_magnitude * MULTIPLIER
        # inspired from Ornstein-Uhlenbeck Process, include mean reversion 
        # tendencies for pvos 
        # This mean reversion brings the perceived value closer to current price over time
        self.pvos += np.random.normal((current_price - self.pvos) * 0.09, 10)

    def decide_order(self):
        # Random Bernoulli trial with self.lop probability
        # Determines if a limit order will be placed
        return np.random.rand() < self.lop

    def place_limit_order(self, current_price):
        # This method determines the price of the limit order
        # It is called only if decide_order returns True
        if self.decide_order():
            # Update perceived value based on the current market price
            self.update_perceived_value(current_price=current_price)
            # Determine the price at which to place the order
            order_price = np.random.normal(self.pvos, 20)
            # Decide whether to buy or sell based on the order price relative to perceived value
            order_type = 'sell' if order_price > self.pvos else 'buy'
            return order_type, order_price
        else:
            # If no order is decided, return 'pass' action
            return 'pass', None  

    def receive_news(self, news_magnitude, current_price):
        # Updates the trader's knowledge based on news magnitude
        if news_magnitude != 0:
            # If there is significant news, set knowledge to 1 (aware of news)
            self.kt = 1
            # Update perceived value based on the news
            self.update_perceived_value(news_magnitude=news_magnitude, current_price=current_price)
        else:
            # If no news, reset knowledge to 0
            self.kt = 0

