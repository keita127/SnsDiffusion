from simulation import Simulation

def main():
    population = 300
    edges = 5
    Dg = 0.8
    Dr = 0.2
    simulation = Simulation(population, edges, Dg, Dr)
    
    simulation.play_game()

if __name__ == '__main__':
    main()