#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
100% Python genetic algorithm !
"""

import random
import string
import time

population_size = 512*8
# just 10% (the best) of the organisms from the current generation to carry over to the next, unaltered. 
elitism_rate = 0.10  
mutation_rate = 0.25
target_string = 'Hello Ricardo, how are you today?'

# 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\x0b\x0c\r '
all_possible_chars = string.letters + string.digits \
    + string.punctuation + string.whitespace


def randstr():
	"""
	Returns a random string using all_possible_chars
	of the size of len(target_string)
	"""
	ret =""
	for _ in range(len(target_string)):
		ret += random.choice(all_possible_chars)
	return ret


def fitness(random_string):
	"""
	Calculates the distance between the value and the target string
	It does that by summing all the character-wise distances: integer ordinal
	"""
	ret = 0;
	for r,t in zip(random_string,target_string):
		value = abs( ord(r) - ord(t) )
		ret += value;
	return ret


def mate(population_1, population_2):
	"""
	Population is ordered by fitness.
	Only population_2 will be altered.
	"""
	elitism_size = int(population_size * elitism_rate)
    # The top fittest (elit) are equal and won't be changed.
	for i in xrange(elitism_size):  # Elitism
		population_2[i] = population_1[i]
    
    # Only the non elistist are going to be changed
	for i in range(elitism_size, population_size):
		# Only the top 50% will mate!
	    i1 = random.randint(0, population_size / 2)
	    i2 = random.randint(0, population_size / 2)
	    pos = random.randint(0, len(target_string))
	    # Mating == Random concatenation 
	    population_2[i] = (population_1[i1])[:pos] + (population_1[i2])[pos:]  # Mate
	    # Insures mutation_rate: a random character inserted in the concatenation
	    if random.random() < mutation_rate:  # Mutate
	        pos = random.randint(0, len(target_string) - 1)
	        population_2[i] = (population_2[i])[:pos] \
	            + random.choice(all_possible_chars) + (population_2[i])[pos + 1:]

if __name__ == '__main__':
	start_time = time.time()
	# population is population_size of random strings of the size target_string
	population_1 = [randstr() for i in xrange(population_size)]
	population_2 = [randstr() for i in xrange(population_size)]
	iteration = 0
	while True:
		# sort population by fitness
	    population_1 = sorted(population_1, key=lambda c: fitness(c))
	    
	    print '[%3d]\tBest (%04d)\t%s' % (iteration, fitness(population_1[0]), population_1[0])
	    if fitness(population_1[0]) == 0:  # We're done, best match found
	    	print "Match found after %s iterations!"%iteration
	        break

	    mate(population_1, population_2)
	    # Swap populations
	    (population_1, population_2) = (population_2, population_1)
	    iteration+=1
	end_time = time.time()
	print "Total time: %.2f seconds"%(end_time-start_time)
