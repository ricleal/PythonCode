from Individual import Individual
from FitnessCalc import FitnessCalc

class Population():

    def __init__(self, population_size, initialise):
        self.individuals = []

        #Creates the individuals
        if (initialise):
            for i in range(population_size):
                new_individual = Individual()
                self.individuals.append(new_individual)
  
    def get_fitness(self, individual_passed):
        fitness = 0
        for i in range(Individual.DefaultGeneLength):
            if individual_passed.genes[i] == FitnessCalc.Solution[i]:
                fitness += 1
        return fitness

    def fitness_of_the_fittest(self):
        fitness_of_the_fittest = self.get_fitness(self.get_fittest())
        return fitness_of_the_fittest

    def get_fittest(self):
        fittest = self.individuals[0]
        for i in range(len(self.individuals)):
            if self.get_fitness(fittest) <= self.get_fitness(self.individuals[i]) :
                fittest = self.individuals[i]
        return fittest

    def size(self):
        return len(self.individuals)
    
    def get_individual(self, index):
        return self.individuals[index]
        
    def save_individual(self, index, individual_passed):
        self.individuals[index] = individual_passed
