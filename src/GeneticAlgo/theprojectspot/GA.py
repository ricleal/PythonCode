from FitnessCalc import FitnessCalc
from Population import Population
from Algorithm import Algorithm
from time import time

start = time()

FitnessCalc.set_solution("1111000000000000000000000000000000000000000000000000000000001111")

my_pop = Population(50, True)

generation_count = 0

while my_pop.fitness_of_the_fittest() != FitnessCalc.get_max_fitness():
    generation_count += 1
    print("Generation : %s Fittest : %s " % (generation_count, my_pop.fitness_of_the_fittest()))
    my_pop = Algorithm.evolve_population(my_pop)
    print("******************************************************")
    
genes_the_fittest = []
for i in range(len(FitnessCalc.Solution)):
    genes_the_fittest.append(my_pop.get_fittest().genes[i])

print("Solution found !\nGeneration : %s Fittest : %s " % (generation_count + 1, my_pop.fitness_of_the_fittest()))
print("Genes of the Fittest : %s " % (genes_the_fittest))


finish = time()
print ("Time elapsed : %s " % (finish - start)) 

