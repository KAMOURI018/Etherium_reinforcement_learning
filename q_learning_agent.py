import numpy as np
from collections import defaultdict

class QLearningAgent:
    def __init__(self, action_space_size, state_space_size, learning_rate=0.01, discount_factor=0.99, epsilon=0.1):
        self.action_space_size = action_space_size
        self.state_space_size = state_space_size
        self.q_table = defaultdict(lambda: np.zeros(self.action_space_size))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    def choose_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.epsilon:  # Explore
            return np.random.choice(self.action_space_size)
        else:  # Exploit
            return np.argmax(self.q_table[state])

    def update_q_value(self, state, action, reward, next_state):
        # Q-Learning update rule
        old_value = self.q_table[state][action]
        next_max = np.max(self.q_table[next_state])  # Use max Q-value of next state
        td_target = reward + self.discount_factor * next_max
        self.q_table[state][action] = old_value + self.learning_rate * (td_target - old_value)

    def get_state(self, observation):
        # Discretize or transform the observation into a state index
        return hash(tuple(np.round(observation, 2)))  # Simple hashing for Q-table indexing
