from simulation import Simulation

def main():
    population = 300          # エージェント数
    edges = 5        # 社会ネットワークの平均次数
    Dg = 0.8
    Dr = 0.2
    simulation = Simulation(population, edges)
    
    simulation.plot_agents(Dg, Dr)

if __name__ == '__main__':
    main()