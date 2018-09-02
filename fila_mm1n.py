# -*- coding: utf-8 -*-
# Fila M(Poisson)/M(Expo)/1/N
import math
import numpy


alfa = 7**5
M = 2**31


def rand_residuo_potencia(root, number_of_iterations):
    vector = []
    for i in xrange(0, number_of_iterations):
        random_variable = float((alfa*root)%(M))
        vector.append(random_variable/M)
        root = random_variable
    return vector
    
        
def rand_transformada(root, number_of_iterations, lambd):
    vector = rand_residuo_potencia(root, number_of_iterations)
    for i in xrange(len(vector)):
        vector[i] = (-math.log(1-vector[i]))/lambd
    return vector
    

def arrival_moments(tc):
    ta = []
    for i in xrange(len(tc)):
        a = 0
        for j in xrange(i+1):
            a = a + tc[j]
        ta.append(a)
    return ta


def generate_tw(tc, ts):
    list_size = len(tc)
    tin = [None]*list_size
    tout = [None]*list_size
    tw = [None]*list_size
    t_arrival = arrival_moments(tc)
    for i in xrange(len(tc)):
        if i == 0:
            print t_arrival[i]
            tin[i] = t_arrival[i]
            tout[i] = t_arrival[i] + ts[i]
            tw[i] = 0
        else:
            if t_arrival[i] >= tout[i-1]:
                tw[i] = 0
                tin[i] = t_arrival[i]
                tout[i] = t_arrival[i] + ts[i]
            else:
                tin[i] = tout[i-1]
                tout[i] = tin[i] + ts[i]
                tw[i] = tout[i] - tin[i]
    return tw
"""
    print tc
    print ts
    print t_arrival
    print tin
    print tout
    print tw
"""


def main():
    tc = rand_transformada(100, 5, 18)
    ts = rand_transformada(999, 5, 10)
    tw = generate_tw(tc, ts)

    e_tc = numpy.mean(ts)
    e_ts = numpy.mean(tc)
    e_tw = numpy.mean(tw)

    print ""
    print "E[tc]: " + str(e_tc) + "/ E[ts]: " + str(e_ts) + "/ E[tw]: " + str(e_tw)
    

if __name__ == "__main__":
    main()