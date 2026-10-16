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
from time import perf_counter as pc
from numba import njit

# Exc1
def approximate_pi(n):
    inside = 0

    inside_x = []
    inside_y = []
    outside_x = []
    outside_y = []

    for i in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        if x**2 + y**2 <= 1:
            inside += 1
            inside_x.append(x)
            inside_y.append(y)
        else: 
            outside_x.append(x)
            outside_y.append(y)


    pi_approximate = 4 * (inside/n)

    print(f'Antal punkter är: {n}')
    print(f'Antal punkter inuti cirkeln är: {inside}')
    print(f'Approximationen av pi är: {pi_approximate}')

    plt.figure()
    plt.scatter(inside_x, inside_y, color="red", s=1)
    plt.scatter(outside_x, outside_y, color="blue", s=1)
    plt.axis("equal") # frivliig så den blir jämn

    plt.savefig(f"Figure_{n}.png")
    plt.close()


    return pi_approximate

# Exc2, approximation

def sphere_volume(n, d): 
    inside = 0
    for j in range(n):
        distance = 0
        point = [random.uniform(-1, 1) for i in range (d)] #comeprehension
   
        squared_point = map(lambda x: x**2, point) #map and lamda 

        for x in squared_point:
            distance += x

        if distance <= 1:
            inside += 1

    volume_approximate = 2**d * (inside/n)

    print(f'Volymen uppskattas till: {volume_approximate}')
    return volume_approximate


#Exc2, real value
def hypersphere_exact(n, d):
    volume_exact = (m.pi**(d/2))/m.gamma((d/2)+1)
    return volume_exact

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    inside = 0

    for j in range(n):
        distance = 0

        for i in range(d):
            x = random.uniform(-1, 1)
            distance += x**2 
        
        if distance <= 1:
            inside +=1
   
    volume_approximate = 2**d * (inside/n)
    return volume_approximate

#Exc4: parallel code - parallelize actual computations by splitting data
def help_sphere_volume_parallel2(n, d):
    inside = 0 

    for j in range(n):
        distance = 0

        for i in range(d):
            x = random.uniform(-1, 1)
            distance += x**2 
        
        if distance <= 1:
            inside +=1

    return inside 

def sphere_volume_parallel(n, d, np=10):
    n_per_np = n // np
    values = []
    
    with future.ProcessPoolExecutor(max_workers=np) as executor:
        for i in range(np):
            values.append(executor.submit(help_sphere_volume_parallel2, n_per_np, d))
    
    inside = 0
    for result in values:
        inside += result.result()

    volume_approximate = 2**d * (inside/n)
    return volume_approximate  
    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    # Exc2
    n = 100000
    d = 2
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11

    for i in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Sequential Python run {i+1}: {stop-start} seconds")

    #first numba
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f'First numba time is: {stop-start}')

    #second numba
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f'Second numba time is: {stop-start}')

    #third numba
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f'Third numba time is: {stop-start}')

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")

    #parallel
    start = pc()
    sphere_volume_parallel(n, d)
    stop = pc()
    print(f'Parallel time is: {stop-start}')
    

if __name__ == '__main__':
	main()
