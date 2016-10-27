# N-Crepes from Artificial Intelligence Subject

# Important data:
#   N       -> Number of crepes

from copy import deepcopy
import random
import sys
import búsqueda_en_haz as BS
import búsqueda_en_haz_con_vuelta_atrás as BSBT
import búsqueda_en_haz_con_discrepancias as BSD
import os

sys.setrecursionlimit(10000)

def neighbours(state):

    result = []
    c = 2

    for a in state:

        k = c

        if(k == len(state)+1):
            break

        copiedState = deepcopy(state)
        crepesToInvest = []

        # Primero obtenemos los k crepes de encima de la pila
        for crepe in state:
            if(k == 0):
                break
            crepesToInvest.append(crepe)
            copiedState.pop(0)
            k = k - 1

        # Los ponemos de nuevo encima de la pila en orden invertido
        for investedCrepe in crepesToInvest:
            copiedState.insert(0, investedCrepe)

        result.append(copiedState)

        c = c + 1

    return result

def heuristic(state):

    h = 0
    plateValue = len(state)+1
    #print(len(state))

    counter = 0
    for crepe in state:
        if(counter+1 == len(state)):
            if(crepe != plateValue-1):
                h = h + 1
            #print("Plato: %s Plato+1: %s Heur: %s" % (crepe, plateValue, h))
        else:
            if(crepe-1 != state[counter+1] and crepe+1 != state[counter+1]):
                h = h + 1
            #print("Plato: %s Plato+1: %s Heur: %s" % (crepe, state[counter+1], h))
        counter = counter + 1

    return h

def N_Crepes(N):

    # ------------------------ START: DATOS A MODIFICAR ----------------------- #
    algoritmo = "BEAM_SEARCH"    # Algorítmo de búsqueda a utilizar:
                                    # BEAM_SEARCH --> Algoritmo búsqueda_en_haz.py
                                    # BEAM_SEARCH_BACK --> Algoritmo búsqueda_en_haz_con_vuelta_atrás.py
                                    # BEAM_SEARCH_DISC --> Algoritmo búsqueda_en_haz_con_discrepancias.py
    max = 100                   # Número de instancias aleatorias
    B = 1                       # Anchura del haz
    memory = 5000               # Tamaño de memoria
    # ------------------------ END: DATOS A MODIFICAR ----------------------- #

    os.system("taskset -p 0xff %d" % os.getpid())

    num_Crepes = N

    estado_final = []

    instancias_resueltas = []
    coste_medio_solucion = []
    num_estados_generados = []
    num_estados_almacenados = []
    tiempo_medio_de_ejecucion = []
    count = 0

    while count < max:
        estado_inicial = []

        random.seed(count)

        for a in range(1, num_Crepes + 1):
            rand_num = random.randrange(1, num_Crepes + 1)
            while rand_num in estado_inicial:
                rand_num = random.randrange(1, num_Crepes + 1)
            estado_inicial.append(rand_num)

        estado_final = deepcopy(estado_inicial)
        estado_final.sort()

        BS.heuristic = heuristic
        BS.neighbours = neighbours

        BSD.heuristic = heuristic
        BSD.neighbours = neighbours

        BSBT.heuristic = heuristic
        BSBT.neighbours = neighbours

        if algoritmo == "BEAM_SEARCH":
            algorithm = BS.busqueda_en_haz(B, estado_inicial, memory, estado_final)
        elif algoritmo == "BEAM_SEARCH_BACK":
            algorithm = BSBT.busqueda_en_haz_backtracking(B, estado_inicial, memory, estado_final)
        elif algoritmo == "BEAM_SEARCH_DISC":
            algorithm = BSD.BULB(estado_inicial, estado_final, B, memory)
        else:
            print("Debe introducir un algoritmo de búsqueda en haz válido (Ejs: BEAM_SEARCH, BEAM_SEARCH_BACK, BEAM_SEARCH_DISC)")

        instancias_resueltas.append(algorithm[0])
        coste_medio_solucion.append(algorithm[1])
        num_estados_generados.append(algorithm[2])
        num_estados_almacenados.append(algorithm[3])
        tiempo_medio_de_ejecucion.append(algorithm[4])
        count = count + 1
        print("Iteración %s" %(count))

    resuelto = str(sum(instancias_resueltas)/len(instancias_resueltas) * 100) + "%"
    coste_medio = sum(coste_medio_solucion)/len(coste_medio_solucion)
    estados_generados = sum(num_estados_generados)/len(num_estados_generados)
    estados_almacenados = sum(num_estados_almacenados)/len(num_estados_almacenados)
    tiempo = sum(tiempo_medio_de_ejecucion)/len(tiempo_medio_de_ejecucion)
    
    print("+----------+--------------------+-----------+-----------------+-------------------+-------------------------+")
    print("|Beam width|Instancias resueltas|Coste medio|Estados generados|Estados almacenados|Tiempo medio de ejecución|")
    print("+----------+--------------------+-----------+-----------------+-------------------+-------------------------+")
    results = "|"
    results = results + str(B)
    guiones = 10 - len(str(B))
    for i in range(guiones):
        results = results + " "
    results = results + "|"

    results = results + str(resuelto)
    guiones = 20 - len(str(resuelto))
    for i in range(guiones):
        results = results + " "
    results = results + "|"

    results = results + str(coste_medio)
    guiones = 11 - len(str(coste_medio))
    for i in range(guiones):
        results = results + " "
    results = results + "|"

    results = results + str(estados_generados)
    guiones = 17 - len(str(estados_generados))
    for i in range(guiones):
        results = results + " "
    results = results + "|"

    results = results + str(estados_almacenados)
    guiones = 19 - len(str(estados_almacenados))
    for i in range(guiones):
        results = results + " "
    results = results + "|"

    results = results + str(tiempo)
    guiones = 25 - len(str(tiempo))
    for i in range(guiones):
        results = results + " "
    results = results + "|"
    print(results)
    print("+----------+--------------------+-----------+-----------------+-------------------+-------------------------+")

# ------------------------ START: DATOS A MODIFICAR ----------------------- #
tam = 30             # Tamaño del problema (Ejs: 30, 40, 50, 60)
# ------------------------ END: DATOS A MODIFICAR ----------------------- #

N_Crepes(tam)

#print(neighbours([3,2,5,1,6,4]))
#print(heuristic([1,2,3,4,5,6,7,8,9]))
#print(heuristic([3,2,5,1,6,4]))
#print(heuristic([3,2,5,1,4,6]))
