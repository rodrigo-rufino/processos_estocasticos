# -*- coding: utf-8 -*-
# Fila M(Poisson)/M(Expo)/1/N
import math
import numpy
import matplotlib.pyplot as plt


alfa = 7**5
M = 2**31-1


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
    ta = [None]*len(tc)
    for i in xrange(len(tc)):
        if i == 0:
            ta[i] = tc[i]
        else:
            ta[i] = tc[i] + ta[i-1]
    return ta


def generate_tw(tc, ts):
    list_size = len(tc)
    tin = [None]*list_size
    tout = [None]*list_size
    tw = [None]*list_size
    t_arrival = arrival_moments(tc)
    for i in xrange(len(tc)):
        if i == 0:
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


def main():
    taxa_chegada = 20
    taxa_atendimento = 40
    n = 1000000

    print "Calculando tc..."
    tc = rand_transformada(1000, n, taxa_chegada)
    print "calculando ts..."
    ts = rand_transformada(10, n, taxa_atendimento)
    print "Calculando tw..."
    tw = generate_tw(tc, ts)

    e_ts = numpy.mean(tc)
    e_tw = numpy.mean(tw)

    print "\nNumero de elementos = " + str(n)
    print "Taxa de chegada = " + str(taxa_chegada) + "\nTaxa de Saída = " + str(taxa_atendimento)
    print "E[ts]: " + str(e_ts) + "/ E[tw]: " + str(e_tw)

    plt.hist(tw, bins=10)
    plt.xlabel('E[tw]')
    plt.show()

    plt.hist(ts, bins=10)
    plt.xlabel('E[ts]')
    plt.show()


    print "E[tq]: " + str(e_tw + e_ts)


    print "Teste do algoritmo de gerar TW "
    print "Tempos de Chegada: [1,3,2,4,5]; Tempos de Atendimento: [3,2,5,6,3]; Tempo na fila: [0, 0, 0, 6, 3]"
    print "Valor gerado: ", generate_tw([1,3,2,4,5], [3,2,5,6,3])



if __name__ == "__main__":
    main()