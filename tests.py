#mean, covariance, std deviaiton, and correlation tests
import function
import time


l1 = [1,2,3,4,5,6]
l2 = [4,-1,-2,-3,-4,-5]
l3 = list(map(lambda x: 2*x,l1))

"""
print("l1 is: " + str(l1))
print("l2 is: " + str(l2))
print("l3 is: " + str(l3))
"""


print("m1 is: " + str(function.mean(l1)))
print("m2 is: " + str(function.mean(l2)))


print("covariance is: " + str(function.covariance(l1,l2)))
print("correlation is: " + str(function.correlation(l1,l2)))



print("l3 is: " + str(l3))

"""
print("correlation l1 l3 is:" + str(function.correlation(l1,l3)))

start_time = time.time()


for i in range(1000000):
    j = i % 3


end_time = time.time()


print("Elapsed time: " + str(end_time - start_time))

"""
