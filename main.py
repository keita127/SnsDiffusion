from simulation import Simulation
import animation

def main():
    population = 500          # エージェント数
    edges = 5        # 社会ネットワークの平均次数
    simulation = Simulation(population, edges)
    
    for i in range(11):
        I = i * 0.1
        I = round(I, 1)
        print("I=" + str(I))
        simulation.plot_agents(I, population)

    animation.make_gif()

if __name__ == '__main__':
    main()