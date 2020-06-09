
import function
import math
import time
import copy

N = 3 #number of functions to be created and evaluated each time
NUM_VARS = 4
KEEPERS = 1  #only keep 100 of the functions


#initate function set
funcs = [] #set of functions to be evolved
for i in xrange(N):
	funcs.append(function.Function(NUM_VARS))
	for j in xrange(7): #start with 7 mutations
		funcs[i].mutateFunction()
	funcs[i].update_func()

print "initial functions created"


GENERATIONS = 3
tester = function.FitnessTester(math.sqrt, 1, 10000, 50)
for g in xrange(GENERATIONS):
	print "generation " + str(g) + " begin"
	#fitness assignment
	print "beginning fitness assignment"
	t0 = time.time()
	
	for i in xrange(len(funcs)):
		funcs[i].setFitness(tester.correlOnly(funcs[i].func))

	t_diff = time.time() - t0
	print "fitness assignment completed after " + str(t_diff) + "s"

	#order by fitness
	print "sorting functions"
	t0 = time.time()
	funcs.sort(key=lambda func: -1* func.fitness)
	print "functions sorted after " + str(time.time()-t0) + "s"

	print "best functions are:"
	for i in xrange(len(funcs)):
		print "rank: " + str(i)
		print "fitness: " + str(funcs[i].fitness)
		print "function:" 
		print funcs[i].sfunc


	#keep only the most fit ones
	funcs[:] = funcs[0:KEEPERS]

	#create and mutate copies
	num_copies = N / KEEPERS -1
	copies = [] #list of copies 
	for i in xrange(KEEPERS):
		for j in xrange(num_copies):
			copies.append(copy.deepcopy(funcs[i]))

	for j in xrange(num_copies):
		for m in xrange(4):
			copies[j].mutateFunction()
		copies[j].update_func()
		
	funcs = funcs + copies
	print "length of funcs is now: " + str(len(funcs))




