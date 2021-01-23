import numpy as np
import random as rnd
import networkx as nx
import pandas as pd
import os
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
        initial_cooperators = rnd.sample(range(population), k = 1)

        return initial_cooperators

    def __initialize_strategy(self):
        # 全エージェントの戦略を初期化

        for index, focal in enumerate(self.agents):
            if index in self.initial_cooperators:
                focal.strategy = "known"
                strategy_map.append(focal.strategy)
                
            else:
                focal.strategy = "unknown"
                strategy_map.append(focal.strategy)

    def __count_payoff(self, I):
        # 利得表に基づいて全エージェントが獲得する利得を計算

        R = 1+I       # Reward
        S = I/2     # Sucker
        T = 1+I/2    # Temptation
        P = 0       # Punishment

        for focal in self.agents:
            focal.point = 0.0
            for nb_id in focal.neighbors_id:
                neighbor = self.agents[nb_id]
                if focal.strategy == "known" and neighbor.strategy == "known":    
                    focal.point += R
                elif focal.strategy == "known" and neighbor.strategy == "unknown":   
                    focal.point += S
                elif focal.strategy == "unknown" and neighbor.strategy == "known":   
                    focal.point += T
                elif focal.strategy == "unknown" and neighbor.strategy == "unknown":  
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

        known = 0
        unknown = 0
        color_map.clear()

        for focal in self.agents:
            focal_color = focal.change_agents_color()
            color_map.append(focal_color)
            if(focal_color == 'red'):
                known += 1
            else:
                unknown += 1
        print("known=" + str(known) + " unknown=" + str(unknown))
    
    def __play_game(self, I):

        self.__count_payoff(I)
        self.__update_strategy()
        self.__change_agents_color()

    def plot_agents(self, I, population):
        # エージェントの分布図の描画
        
        os.makedirs("images/images_" + str(I), exist_ok=True)

        self.__choose_initial_cooperators()
        self.__initialize_strategy()
        self.__change_agents_color()

        break_map = ["None"] * population

        def for_sort(i):
            if( i < 10 ) :
                return ("0" + str(i))
            else :
                return str(i)

        for i in range(100):
            counter = 0
            fig = plt.figure(figsize=(40,35), dpi=30)
            nx.draw_networkx(network, pos, node_color=color_map, with_labels=False, node_shape='.', node_size=2000)
            plt.axis("off")
            plt.title("I=" + str(I) + " , t=" + str(i), fontsize=50)
            fig.savefig("images/images_" + str(I) + "/fig_" + for_sort(i) + ".png",dpi=30)
            for j in range(population) :
                if(color_map[j] == "red") : counter += 1 
            if(color_map == break_map or counter >= 450) : break
            self.__play_game(I)

