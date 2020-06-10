import function
import random
import math

n = 100 #sample size

X = [0]*n
E = [0]*n
for i in range(n):
    X[i] = random.uniform(-1,1)
    E[i] = random.gauss(0,1)



def y1(x, e):
    y = 1* x + e
    return y

def y2(x,e):
    y = 1 * x * x + e
    return y


Y1 = list(map(y1,X,E))

Y2 = list(map(y2,X,E))

"""
print("Correlation between Y1 and X: " + str(function.correlation(Y1, X)))

print ("Correlation between Y1 and Y2: " + str(function.correlation(Y1,Y2)))


tester = function.FitnessTester(math.sqrt, 0,1000000,100)

fit = tester.fitness(lambda x: x)

fit.printSelf()
"""

def alex_sqrt(x, acceptable_error, print_iters = False):
    if x==0:
        return 0
    acceptable_error_percent = acceptable_error / x
    acceptable_squared_error = acceptable_error ** 2
    guess = x / 2
    squared_guess = guess ** 2
    squared_error = squared_guess - x
    i=0
    if(print_iters):
        print("i: " + str(i) + ", guess: " + str(guess) + ", SquaredError: "  + str(squared_error))
    while abs(squared_error) > acceptable_squared_error:
        i+1
        guess -= squared_error * acceptable_error_percent
        squared_guess = guess ** 2
        squared_error = squared_guess - x
        if(print_iters):
            print("i: " + str(i) + ", guess: " + str(guess) + ", SquaredError: "  + str(squared_error))

    return guess


def quick_sqrt(x):
    return alex_sqrt(x,1)


"""
result = alex_sqrt(1000,1,True)
print("Result: " + str(result))
"""
tester = function.FitnessTester(math.sqrt,0,10000000,100)

fit = tester.fitness(quick_sqrt)
fit.printSelf()

