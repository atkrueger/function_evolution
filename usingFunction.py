import function
import math
import copy
import time

"""
z = function.Function(2) #creates a default function with 3 input variables

for i in range(4):
	z.addAssignment() #adds random assignment to architecture

for i in range(1):
	z.addCondStatement()

for i in range(3):
	z.mutateFunction()
	z.update_func()
	result = function.meanDiff(math.sqrt, z.func,0,1000,50)
	print "mean difference between sqrt and z is: " + str(result)


z.print_func("z.py")
"""

#next step is to evaluate and evolve towards a particular function
""" steps:
	1. create first generation of functions
	2. evaluate functions and rank them
	3. keep only the top-ranked functions
	4. make multiple copies of the top-ranked functions and mutate them
	5. go back to step 2
"""

N = 10000 #number of functions to be created and evaluated each time
NUM_VARS = 4
KEEPERS = 200  #only keep 100 of the functions

#compares function f to the sqrt function (without calculating sqrt) over range start-stop
def meanDiffSqrt(f, start, stop, tests):
	interval = stop-start / tests
	sum_diff = 0

	try:
		for i in range(tests):
			inp = start + i*interval
			sum_diff += abs(int(inp) - int(f(inp))**2)
			#compares the input to the square of the estimated function
			if sum_diff>1000000:
				return 1000000
		return sum_diff / tests #average difference
	except:
		return 99999


#initate function set
funcs = [] #set of functions to be evolved
for i in range(N):
	funcs.append(function.Function(NUM_VARS))
	for j in range(10): #start with 10 mutations
		funcs[i].mutateFunction()
	funcs[i].update_func()

print("initial functions created")


GENERATIONS = 50
tester = function.FitnessTester(math.sqrt, 1, 10000, 30)
for g in range(GENERATIONS):
	print("generation " + str(g) + " begin")
	#fitness assignment
	print("beginning fitness assignment")
	t0 = time.time()
	for i in range(N):
		#funcs[i].setFitness(meanDiffSqrt(funcs[i].func, 0, 1000, 50))
		fitness = tester.fitness(funcs[i].func)
		funcs[i].setFitness(fitness.correlation) #for now, based solely on correlation

	t_diff = time.time() - t0
	print("fitness assignment completed after " + str(t_diff) + "s")

	#order by fitness
	print("sorting functions")
	t0 = time.time()
	funcs.sort(key=lambda func: -1* func.fitness)
	print("functions sorted after " + str(time.time()-t0) + "s")

	print ("best functions are:")
	for i in range(2):
		print("rank: " + str(i))
		print("fitness: " + str(funcs[i].fitness))
		print("function:")
		print(funcs[i].sfunc)


	#keep only the most fit ones
	funcs[:] = funcs[0:KEEPERS]

	#create and mutate copies
	num_copies = N / KEEPERS -1
	copies = [] #list of copies 
	for i in range(KEEPERS):
		for j in range(num_copies):
			copies.append(copy.deepcopy(funcs[i]))

	for j in range(num_copies):
		for m in range(4):
			copies[j].mutateFunction()
		copies[j].update_func()
		
	funcs = funcs + copies





