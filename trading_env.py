import gym
import numpy as np
from gym import spaces

class TradingEnv(gym.Env):
    def __init__(self, df):
        super(TradingEnv, self).__init__()
        
        self.df = df
        self.current_step = 0
        self.initial_balance = 100000  # Initial cash balance
        self.balance = self.initial_balance
        self.position = 0  # Current position: 1 for long, -1 for short, 0 for no position
        self.entry_price = 0
        self.trades = []  # List to track all trades

        # Action space: 0 = Hold, 1 = Buy, 2 = Sell
        self.action_space = spaces.Discrete(3)
        
        # Observation space: use all indicators in `df`
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(len(df.columns),), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        self.balance = self.initial_balance
        self.position = 0
        self.entry_price = 0
        self.trades = []  # Reset trades at the beginning of each episode
        return self.df.iloc[self.current_step].values

    def step(self, action):
        done = False
        current_price = self.df.iloc[self.current_step]['close']
        reward = 0

        # Entry logic
        if action == 1 and self.position == 0:  # Buy
            self.position = 1
            self.entry_price = current_price
            self.trades.append((self.current_step, current_price, 'buy'))
            reward = 10  # Reward for entering a position

        elif action == 2 and self.position == 0:  # Sell
            self.position = -1
            self.entry_price = current_price
            self.trades.append((self.current_step, current_price, 'sell'))
            reward = 10  # Reward for entering a position

        # Holding logic
        elif action == 0 and self.position != 0:  # Hold position
            unrealized_profit = (current_price - self.entry_price) * self.position
            reward = 1 if unrealized_profit > 0 else -1

        # Exit logic
        elif self.position != 0 and action != 0:  # Exit position
            profit = (current_price - self.entry_price) * self.position
            self.balance += profit
            reward = 10 if profit > 0 else -10  # Reward for profitable exit, penalty for loss
            self.trades.append((self.current_step, current_price, 'exit'))
            self.position = 0

        # Inactivity penalty
        if reward == 0 and self.position == 0:
            reward = -1

        # Move to the next step
        self.current_step += 1
        if self.current_step >= len(self.df) - 1:
            done = True

        obs = self.df.iloc[self.current_step].values
        return obs, reward, done, {}

    def render(self):
        profit = self.balance - self.initial_balance
        print(f'Step: {self.current_step}, Profit: {profit}')
