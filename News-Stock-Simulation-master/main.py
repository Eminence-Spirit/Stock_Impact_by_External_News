import numpy as np
import matplotlib.pyplot as plt
from classes.market import MarketModel

def simulate_and_plot(news_magnitude_range, num_simulations, num_traders=1000, time_steps=115):
    plt.figure(figsize=(12, 8))

    for news_magnitude in np.linspace(news_magnitude_range[0], news_magnitude_range[1], num_simulations):
        market = MarketModel(num_traders=num_traders, time_steps=time_steps)
        market.simulate_market(news_magnitude=news_magnitude)
        plt.plot(market.stock_price_history, label=f"News Magnitude: {news_magnitude:.2f}")

    plt.title("Stock Price History for Different News Magnitudes")
    plt.xlabel("Time Steps")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.grid(True)
    plt.savefig("stock_price_simulation.png")
    plt.show()

if __name__ == "__main__":
    simulate_and_plot(news_magnitude_range=(-1, 1), num_simulations=20)
