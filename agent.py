import random as rnd
from matplotlib.pyplot import colorbar
import numpy as np

class Agent:
    def __init__(self):
        self.point = 0.0
        self.strategy = None
        self.next_strategy = None
        self.neighbors_id = []
        self.strategy_map = []
        self.color_map = []

    def decide_next_strategy(self, agents):
        # Pairwise-Fermiモデルで次のゲームでの戦略を決定する

        opponent_id = rnd.choice(self.neighbors_id)
        opponent = agents[opponent_id]

        if opponent.strategy != self.strategy and rnd.random() < 1/(1 + np.exp((self.point - opponent.point)/0.1)):
            self.next_strategy = opponent.strategy
        else:
            self.next_strategy = self.strategy 


    def update_strategy(self):
        self.strategy = self.next_strategy
        return self.strategy
        
    def change_agents_color(self):
        if self.strategy == 'known':
            return "red"
        elif self.strategy == "unknown":
            return "None"
        
        