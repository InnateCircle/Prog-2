""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    ns=0
    nc=0
    inside_x = []
    inside_y = []
    outside_x = []
    outside_y = []
    for _ in range(n):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if x**2 + y**2 <= 1:
            nc +=1
            inside_x.append(x), inside_y.append(y)
        else: 
            ns +=1
            outside_x.append(x),outside_y.append(y)
           
    plt.figure()
    plt.scatter(inside_x, inside_y, s=5, c='red',   label='inside')
    plt.scatter(outside_x, outside_y, s=5, c='blue', label='outside')
    plt.axis('equal')
    plt.show()      
    pi = 4*nc/n
    print(n)
    print(pi)
    return pi

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    points = [(random.uniform(-1,1) for _ in range(d)) for _ in range(n)]
    
    inside = list(filter(lambda p : sum(x**2 for x in p) <=1,points))
    nc = len(inside)
    rd = 2**d
    return rd * nc / n

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 
    top = m.pi**(d/2)
    bottom = m.gamma(d/2 + 1)
    
    return top/bottom 

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
      #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    t0 = pc()
    with future.ProcessPoolExecutor() as ex:
           
        P = [ex.submit(sphere_volume,n,d) for _ in range(np)]
        results = [f.result() for f in P]
    t1 =pc()
    
    average = sum(results)/len(results)
    time = t1-t0
    return average, time
#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    t0 = pc()
    base = n//np
    rest = n%np
    parts = [base + 1 if i < rest else base for i in range(np)]
    with future.ProcessPoolExecutor() as ex:
           
        P = [ex.submit(sphere_volume, part ,d) for part in parts]
        results = [f.result() for f in P]
    t1 =pc()
    
    average = sum(results)/len(results)
    time = t1-t0
    return average
    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    
    

if __name__ == '__main__':
	main()
