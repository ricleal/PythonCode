from random import randint
from FitnessCalc import FitnessCalc

class Individual():
  
    DefaultGeneLength = len(FitnessCalc.Solution)

    def __init__(self):
        self.genes = bytearray(Individual.DefaultGeneLength)
        for i in range(Individual.DefaultGeneLength):   
            gene = randint(0,1)
            self.genes[i] = gene

    def get_gene(self, index):
        return self.genes[index]
    
    def set_gene(self, index, what_to_set):
        self.genes[index] =  what_to_set
    
    def size(self):
        return len(self.genes)