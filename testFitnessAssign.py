import math
import function
import random

tester = function.FitnessTester(math.sqrt, 1, 100000, 100)

sqrt = math.sqrt


def x(input):
    return input

def twox(input):
    return input*2

def rand(input):
    return random.random()

def xsquared(input):
    return input**2

def zero(input):
    return 0

#print tester.fitness(sqrt)
#print tester.fitness(x)
#print tester.fitness(twox)
#print tester.fitness(rand)

tester.rankFitness([sqrt, x, twox, rand, xsquared ,zero])
