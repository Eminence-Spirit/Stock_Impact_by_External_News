import numpy as np
import copy
import bisect

# Set the frequency of news spreading throughout the day
times_per_day = 2

class NewsSpreadModel:
    def __init__(self, num_traders=500, radius=5, arrival_rate=0.1, time_steps=100):
        # Initialize the model parameters: number of traders, radius of influence, news arrival rate, and time steps
        self.num_traders = num_traders  # Total number of traders in the simulation
        self.radius = radius  # Radius of influence for each trader
        self.arrival_rate = arrival_rate  # Rate at which news arrives and spreads to neighbors
        self.times = [0]  # Initialize times; starts at 0 and adds new times as the process progresses
        # Initialize news states for traders, initially no news (0) for all traders
        self.news_states = [np.random.binomial(1, 0.01, self.num_traders)]
        self.increment_news_states = []  # Placeholder for incremented news states
        self.time_steps = time_steps  # Total number of time steps in the simulation

    def start_news_at_random_location(self):
        # Start the news from a random trader
        # This adds a new state with some traders having news
        self.news_states.append(np.random.binomial(1, 0.25, self.num_traders))

    def _get_neighbors(self, index):
        # Determine the neighbors of a trader based on the specified radius
        # Using modular arithmetic for circular topology (wrapping around)
        return [(index + i) % self.num_traders for i in range(-self.radius, self.radius + 1) if i != 0]

    def spread_news(self):
        # Simulate news spread over time among traders
        t = 0  # Starting time
        while t <= times_per_day * self.time_steps / 2:
            choosen_i = np.random.randint(self.num_traders)  # Randomly choose a trader
            time_increase = np.random.exponential(1 / (self.radius * self.arrival_rate * self.num_traders)) # include nearby neighbours
            t += time_increase  # Increment time based on exponential distribution
            self.times.append(t)  # Record the updated time
            # Copy the last state from news_states to modify
            news_state_to_modify = copy.deepcopy(self.news_states[-1])
            # Spread news to the chosen trader if not already informed
            if news_state_to_modify[choosen_i] == 0:
                neighbors = self._get_neighbors(choosen_i)  # Get neighbors of the chosen trader
                sum_of_neighbors = sum(news_state_to_modify[neighbor] for neighbor in neighbors)
                # Determine if news spreads to the chosen trader based on neighbors' states
                if np.random.uniform() < self.arrival_rate * sum_of_neighbors / (self.arrival_rate * self.radius):
                    news_state_to_modify[choosen_i] = 1  # Update trader's news state
            self.news_states.append(news_state_to_modify)  # Record the updated news state

    def incremented_time_states(self):
        # Record states at incremented time intervals
        self.increment_news_states.append(self.news_states[0])  # Start with the initial state
        for time_increment in range(times_per_day, times_per_day * (int(self.time_steps / 2) + 1), times_per_day):
            # Find the largest time that is within the current time increment
            index_largest_time_within_time_increment = bisect.bisect_right(self.times, time_increment) - 1
            # Append the news state corresponding to that time
            self.increment_news_states.append(self.news_states[index_largest_time_within_time_increment])
            # Note: self.increment_news_states may contain duplicates from self.news_states
            # This is intentional as it reflects the state of news at specific time points.
        return self.increment_news_states
