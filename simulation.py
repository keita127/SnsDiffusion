import numpy as np
import random as rnd
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from agent import Agent

class Simulation:

    global strategy_map
    global color_map
    strategy_map = []
    color_map = []

    def __init__(self, population, average_degree):
        self.agents = self.__generate_agents(population, average_degree)
        self.initial_cooperators = self.__choose_initial_cooperators() 

    def __generate_agents(self, population,edges):
        # エージェントをリストに詰め、隣人エージェントのIDをセットする

        global rearange_edges
        global network
        global pos
        network = nx.barabasi_albert_graph(population, edges)
        pos = nx.spring_layout(network)

        agents = [Agent() for id in range(population)]
        for index, focal in enumerate(agents):
            neighbors_id = list(network[index])
            for agent_id in neighbors_id:
                focal.neighbors_id.append(agent_id)

        return agents

    def __choose_initial_cooperators(self):
        #最初のゲームでC戦略を取るエージェントをランダムに選ぶ

        population = len(self.agents)
        initial_cooperators = rnd.sample(range(population), k = int(population/2))

        return initial_cooperators

    def __initialize_strategy(self):
        # 全エージェントの戦略を初期化

        for index, focal in enumerate(self.agents):
            if index in self.initial_cooperators:
                focal.strategy = "C"
                strategy_map.append(focal.strategy)
                
            else:
                focal.strategy = "D"
                strategy_map.append(focal.strategy)

    def __count_payoff(self, Dg, Dr):
        # 利得表に基づいて全エージェントが獲得する利得を計算

        R = 1       # Reward
        S = -Dr     # Sucker
        T = 1+Dg    # Temptation
        P = 0       # Punishment

        for focal in self.agents:
            focal.point = 0.0
            for nb_id in focal.neighbors_id:
                neighbor = self.agents[nb_id]
                if focal.strategy == "C" and neighbor.strategy == "C":    
                    focal.point += R 
                elif focal.strategy == "C" and neighbor.strategy == "D":   
                    focal.point += S
                elif focal.strategy == "D" and neighbor.strategy == "C":   
                    focal.point += T
                elif focal.strategy == "D" and neighbor.strategy == "D":  
                    focal.point += P

    def __update_strategy(self):
        # 全エージェントに戦略を更新させる

        for focal in self.agents:
            focal.decide_next_strategy(self.agents)

        for focal in self.agents:
            focal_strategy = focal.update_strategy()
            strategy_map.append(focal_strategy)
    
    def __change_agents_color(self):
        # 戦略によりエージェントの色を変える

        red = 0
        blue = 0
        
        color_map.clear()
        for focal in self.agents:
            focal_color = focal.change_agents_color()
            color_map.append(focal_color)
            if(focal_color == 'red'):
                red += 1
            else:
                blue += 1
        
        print("red=" + str(red) + " blue=" + str(blue))
    
    def __play_game(self, Dg, Dr):

        self.__count_payoff(Dg, Dr)
        self.__update_strategy()
        self.__change_agents_color()

    def plot_agents(self, Dg, Dr):
        # エージェントの分布図の描画
        
        self.__choose_initial_cooperators()
        self.__initialize_strategy()
        self.__change_agents_color()
        
        for i in range(10):
            fig = plt.figure(figsize=(40,35), dpi=30)
            nx.draw_networkx(network, pos, node_color=color_map, with_labels=False, node_shape='.', node_size=2000)
            plt.axis("off")
            plt.title("t=" + str(i), fontsize=50)
            fig.savefig("fig_" + str(i) + ".png",dpi=30)
            # plt.show()
            self.__play_game(Dg, Dr)
            

