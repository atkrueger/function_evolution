#code updated to use python 3.8
import random
import math
import time
#import decimal

#decimal.getcontext().prec=30
#precision to 30 digits

#helper functions

def select_random(vector, exclusions=None):
	if exclusions is None:
		return vector[random.randint(0,len(vector)-1)]
	else:
		new_list = []
		for o in vector:
			if o not in exclusions:
				new_list.append(o)
			#else:
			#	print "item " +  str(o) + " excluded"
		
		return new_list[random.randint(0,len(new_list)-1)]


def mean(vector):
	#calculates the mean of the list
	sum = 0.0
	n = len(vector)
	for i in vector:
		sum+=i
	return sum / n

def covariance(vector1, vector2):
	#calculates the covariance of two lists of numbers
	#should throw an error if the lists are not the same length
	mean1 = mean(vector1)
	mean2 = mean(vector2)
	n = len(vector1)
	sum = 0.0
	for i in range(n):
		sum+= (vector1[i] - mean1) * (vector2[i] - mean2)
	return sum / n
	
def variance(vector):
	#returns the standard deviation of a list
	mu = mean(vector)
	n = len(vector)
	sum_sq_diffs=0.0
	try:
		for i in vector:
			sum_sq_diffs+=((i-mu)**2)
		return sum_sq_diffs / n
	except OverflowError:
		return 999999

def stdev(vector):
	return variance(vector)**(0.5)

def correlation(vector1,vector2):
	#returns correlation between vector1 and vector2
	try:
		return covariance(vector1,vector2)/(stdev(vector1)*stdev(vector2))
	except ZeroDivisionError:
		return 0 
		#returns no correlation if the standard deviation of one of them is zero


def meanDeviation(vector1, vector2):
	#calculates mean deviation between the two 
	#sum of absolute value of differences
	sum=0.0
	n = len(vector1)
	for i in range(n):
		sum+= abs(vector1[i] - vector2[i])
	return sum  / n

class FitnessTester(object):

	def __init__(self, goal_func, start, stop, tests):
	#class deisgned to efficiently test the fitness of a function
	# function is more fit the:
	# 1. more closely it is correlated with the goal_func (high absolute value of correl)
	# 2. smaller the mean difference between test_func and goal_func
	# 3. shorter the completion time
	#measures this fitness over range of inputs from start-stop, num tests
		self.interval = (stop - start) / tests
		self.start = start
		self.stop = stop
		self.tests = tests

		self.input = list(map(lambda x: start + (x*self.interval), range(tests)))
		self.goal_output = list(map(goal_func, self.input))


	def fitness(self, test_func):
		
		#calculate test function output and measure duration
		start = time.time()
		test_output = list(map(test_func, self.input))
		duration = time.time() - start

		#measure correlation and mean deviation between test function output and goal function output
		corr = correlation(test_output, self.goal_output)

		mean_dev =meanDeviation(test_output, self.goal_output)

		#now, how to weight the results
		return  Fitness(duration, corr, mean_dev)

class Fitness(object):

	def __init__(self, dur, corr, meandev):
		self.duration = dur
		self.correlation = corr
		self.mean_deviation = meandev


	def printSelf(self):
		print("Corr: " + str(self.correlation) + ", MeanDev: " + str(self.mean_deviation) + ", Duration: " + str(self.duration) + "s")


class Function(object):

	def __init__(self, num_vars):

		#initiate head of default skeleton function
		self.skeleton_head = "def dummy(input):" #name and parameters
		self.skeleton_head+="\n\ttry:"
		self.skeleton_head+="\n\t\tx = [1.0]*" + str(num_vars) #variables to be manipulated
		self.skeleton_tail = "\n\t\treturn x[0]"
		self.skeleton_tail+="\n\texcept ZeroDivisionError:"
		self.skeleton_tail+="\n\t\treturn -77777\n"
			#must end in \n  to be run by executable

		self.stack = [] #the list of expressions in between the head and the tail

		self.num_vars = num_vars #stored for later
		self.update_func() #creates sfunc and func

	def genStackString(self): #returns string from stack
		stackString = ""

		loop_num = 0 #for assigning loop_ids
		for i in range(len(self.stack)):

			#1. assign tab structure
			if(i==0):
				self.stack[i].tabs=2 #first tab has two tabs
			else:
				self.stack[i].tabs = self.stack[i-1].tabs #default

				if isinstance(self.stack[i-1], condStatement):
					self.stack[i].tabs = self.stack[i-1].tabs+1 #tab right if following if or while
				elif isinstance(self.stack[i-1],passStatement):
					self.stack[i].tabs = self.stack[i-1].tabs-1 # tab left if using pass to close conditional

			#2 add unique loop_id to each while statement
			if isinstance(self.stack[i],condStatement) and self.stack[i].type =="while":
				self.stack[i].loop_id = loop_num
				loop_num +=1

			#3. generate string and add to stack
			self.stack[i].genString()
			stackString+= self.stack[i].string
		
		return stackString


	def update_sfunc(self):  #updates string representation of function
		self.sfunc = self.skeleton_head + self.genStackString() + self.skeleton_tail
		#print self.sfunc

	def update_func(self): #converts sfunc to an actual python function
		self.update_sfunc()
		#print self.sfunc
		try:
			exec(self.sfunc) #creates the dummy function 
			self.func = dummy #assigns self.func to that dummy function
		except SystemError as e:
			print ("Following function threw a SystemError:" + str(e))
			print (self.sfunc)
			self.func = lambda x:  88888
		


	def print_func(self, path): #prints function to particular path
		f = open(path, "w")
		f.write(self.sfunc)
		f.close()

	def addAssignment(self): #adds random assignment in random location
		i = random.randint(0,len(self.stack))
		self.stack.insert(i,Assignment(self.num_vars))
		

	def addCondStatement(self): #adds random ifStatement in random location

		#1. insert the leading if statement
		i1 = random.randint(0,len(self.stack))
		self.stack.insert(i1,condStatement(self.num_vars))

		#2 insert the closing pass statement
		i2 = random.randint(i1+1,len(self.stack))
		self.stack.insert(i2, passStatement())

	def removeStackable(self): #removes a random stackable
		#must be careful to remove closing pass statement if removing a cond statement
		if len(self.stack)==0:
			return 0 #nothing to do

		i = random.randint(0, len(self.stack)-1)

		#delete both the condStatement and its following pass statement
		if isinstance(self.stack[i], condStatement):
			for j in range(i, len(self.stack)):
				if isinstance(self.stack[j], passStatement):
					del self.stack[j]
					break
		elif isinstance(self.stack[i], passStatement):
			return 0 #can't delete pass statements, otherwise will have unenclosed loops

		del self.stack[i]
		return 1


	#allows programmer to add a particular statement to the stack
	def addUserStatement(self, statement):
		self.stack.append(Stackable(statement))

	def mutateOrder(self,rate): 
		#rate is the percentage of time order will be mutated
		if(rate>=1):
			def p(x):
				return True
		else:
			def p(x): 
				return random.random() <= x

		def try_swap(index): #tries to swap stack of index and index-1
			if isinstance(self.stack[index-1], condStatement) and isinstance(self.stack[index],passStatement):
				return 0 #no swap
			else:
				holder = self.stack[index-1]
				self.stack[index-1] = self.stack[index]
				self.stack[index] = holder
				return 1 #a swap

		#goes through the stack and flips order
		mutations = 0
		for i in range(len(self.stack)):
			if i !=0:
				if p(rate):
					mutations+=try_swap(i)
		return mutations

	def mutateFunction(self):
		#for now can fix some particular mutation rates
		#but we might want to evolve the mutation rates too in the long run

		#ways to mutate:
		mutations = 0
		#1. Function.mutateOrder(rate)
		if random.random() <= 0.5: #mutate order of stack half the time
			mutations +=self.mutateOrder(0.2) #when mutating order of stack, flip positions 20% of time

		#2. Stackable.mutate(rate)
		for i in range(len(self.stack)):
			if random.random() <= 0.3:
				mutations+=self.stack[i].mutate(0.3)
		
		#3. Function.addAssignment()
		if random.random() <=0.4:
			self.addAssignment()
			mutations+=1

		#4. Function.addCondStatement()
		if random.random() <=0.1:
			self.addCondStatement()
			mutations+=1

		#5. delete stackable
		if random.random() <0.1:
			mutations+=self.removeStackable()

		#check whether any mutations occurred, if not, then re-mutate to assure some difference
		if mutations <1:
			self.mutateFunction()
		
	def setFitness(self, fit):
		self.fitness = fit

	def getFitness(self):
		return self.fitness


class Stackable(object):

	#interior expressions will inherit from this
	#all need to have a genString function and a string attribute
	#all need to have a mutate function

	def __init__(self, statement):
		self.string = statement
		

class Assignment(Stackable):

	#valid assignment is
	#variable (x[0-n]) = [variable or input] [operator] [variable or number or input]
	# ("reveiver")     = "t1"                "operator" "t2"
	#default setup
	VALID_T1_TYPES = ["x", "input"]
	VALID_OPERATORS = ["+", "-", "/", "*"]
	VALID_T2_TYPES = ["x", "input", "constant"]
	VALID_T2_RANGE = [-2,2]


	def __init__(self, num_vars):
		
		#self.tabs = 2 #default value
		#initiate values
		self.num_vars = num_vars
		self.receiver_index = select_random([i for i in range(self.num_vars)])
		self.t1_type = select_random(self.VALID_T1_TYPES)
		self.t1_index = select_random([i for i in range(self.num_vars)])
		self.operator = select_random(self.VALID_OPERATORS)
		self.t2_type = select_random(self.VALID_T2_TYPES)
		self.t2_index = random.randint(0, self.num_vars-1)
		self.t2_constant = random.uniform(self.VALID_T2_RANGE[0],self.VALID_T2_RANGE[1])
		self.tabs=0 # default value
		

	def genString(self):
		tabs = "\n" + "\t" * self.tabs
		r = "x[" + str(self.receiver_index) + "]"
		a = "="

		if(self.t1_type == "x"):
			t1 = "x[" + str(self.t1_index)+"]"
		elif(self.t1_type == "input"):
			t1 = "input"

		o = self.operator

		if(self.t2_type == "x"):
			t2 = "x[" + str(self.t2_index)+"]"
		elif(self.t2_type == "input"):
			t2 = "input"
		elif(self.t2_type =="constant"):
			t2 = str(self.t2_constant)

		self.string = tabs + r + a + t1 + o + t2

	def mutate(self, rate):
		#rate is the mutation rate, equal to a percentage of time each subcomponent should be mutated

		#probability of mutation
		if(rate>=1):
			def p(x):
				return True
		else:
			def p(x): 
				return random.random() <= x

		mutations = 0
		#excluding current values from options to ensure a real mutation
		if p(rate):
			self.receiver_index = select_random([i for i in range(self.num_vars)],[self.receiver_index])
			mutations+=1
		if p(rate):
			self.t1_type = select_random(self.VALID_T1_TYPES, [self.t1_type])
			mutations+=1
		if p(rate):
			self.t1_index = select_random([i for i in range(self.num_vars)],[self.t1_index])
			mutations+=1
		if p(rate):
			self.operator = select_random(self.VALID_OPERATORS, [self.operator])
			mutations+=1
		if p(rate):
			self.t2_type = select_random(self.VALID_T2_TYPES, [self.t2_type])
			mutations+=1
		if p(rate):
			self.t2_index = select_random([i for i in range(self.num_vars)],[self.t2_index])
			mutations+=1
		if p(rate):
			self.t2_constant = random.uniform(self.VALID_T2_RANGE[0],
			self.VALID_T2_RANGE[1])
			mutations+=1

		return mutations


class condStatement(Stackable):
	

	#if statements have the following structure
	#if ([var] [equality operator] [var, input. or const]):
	#and they are closed off by pass statements (while statements are also closed off this way)
	#so when you add an if statement you have to also add a corresponding pass statement

	MAX_LOOPS = 100 #maximum number of loops allowed, to prevent infinite looping
	VALID_OPERATORS = ['>', "<", "<=", ">=","==", "!=" ]
	#only valid t1 type is x[]
	VALID_T2_TYPES = VALID_T2_TYPES = ["x", "input", "constant"]
	VALID_T2_RANGE = [-2,2]
	VALID_TYPES = ["if", "while"]

	def __init__(self, num_vars):
		
		self.num_vars = num_vars 
		#initiate values
		self.t1_index = random.randint(0,self.num_vars-1) #index of variable used in first term
		self.operator = select_random(self.VALID_OPERATORS)
		self.t2_type = select_random(self.VALID_T2_TYPES)
		self.t2_index = random.randint(0,self.num_vars-1)
		self.t2_constant = random.uniform(self.VALID_T2_RANGE[0], self.VALID_T2_RANGE[1])
		self.type = select_random(self.VALID_TYPES)
		self.tabs = 0 # default value
		self.loop_id = 0 # default value
		#self.mutate(1) #select random values for all subcomponents
		

	def mutate(self, rate):
		#probability of mutation
		if(rate>=1):
			def p(x):
				return True
		else:
			def p(x): 
				return random.random() <= x

		mutations =0
		if p(rate):
			self.t1_index = select_random([i for i in range(self.num_vars)],[self.t1_index])
			mutations+=1
		if p(rate):
			self.operator = select_random(self.VALID_OPERATORS, [self.operator])
			mutations+=1
		if p(rate):
			self.t2_type = select_random(self.VALID_T2_TYPES, [self.t2_type])
			mutations+=1
		if p(rate):
			self.t2_index = select_random([i for i in range(self.num_vars)],[self.t2_index])
			mutations+=1
		if p(rate):
			self.t2_constant = random.uniform(self.VALID_T2_RANGE[0], self.VALID_T2_RANGE[1])
			mutations+=1
		if p(rate):
			self.type = select_random(self.VALID_TYPES, [self.type])
			mutations+=1

		return mutations

	def genString(self):

		#adding the unique loop counter, if it is a while loop
		#(prevents infinite loops)
		l_head = ""
		if self.type == "while":
			l_head = "\n" + "\t" * self.tabs + "loop" + str(self.loop_id) + "=0"

		t = "\n" + "\t" * self.tabs

		i = self.type + " " 


		t1 = "x[" + str(self.t1_index) + "]"
		o = self.operator

		if(self.t2_type == "x"):
			t2 = "x[" + str(self.t2_index)+ "]"
		elif(self.t2_type =="input"):
			t2 = "input"
		elif(self.t2_type == "constant"):
			t2 = str(self.t2_constant)

		#adding unique loop counter checker, if it is a while loop
		l_tail = ""
		if self.type == "while":
			l_tail += "\n" + "\t" * (self.tabs+1) + "loop" + str(self.loop_id) + "+=1"
			l_tail += "\n" + "\t" * (self.tabs+1) + "if loop" + str(self.loop_id) + ">" + str(self.MAX_LOOPS) + ":"
			l_tail += "\n" + "\t" * (self.tabs+2) + "break"

		self.string = l_head + t + i + t1 + o + t2 + ":" + l_tail

	#next need to create an "addIfStatement" function to the function creator that adds a massing pass

class passStatement(Stackable):
	#used to close off conditional statements such as ifStatements and whileStatements
	#to ensure that all loops close, when you mutate stacks you need to prohibit pass statements from
	#being pushed above ifStatements and whileStatements
	def __init__(self):
		self.tabs =2 #default value
		self.genString()

	def genString(self):
		t = "\n" + "\t" * self.tabs
		self.string = t + "pass"

	def mutate(self, rate):
		return 0 #can't mutate a pass functio







