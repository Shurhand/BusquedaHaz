# N-Puzzle from Artificial Intelligence Subject

# Important data:
#   N       -> Number of pieces

from copy import deepcopy
import random
import sys
from math import sqrt
import búsqueda_en_haz as BS
import búsqueda_en_haz_con_vuelta_atrás as BSBT
import búsqueda_en_haz_con_discrepancias as BSD
import os

sys.setrecursionlimit(10000)

def neighbours(state):

    result = []
    num_Casillas = len(state)
    M = sqrt(num_Casillas)
    tablero = [] # Tablero dividido en filas
    tablero.append([]) # Le metemos la primera fila vacía
    num_row = 0
    num_col = 0
    zero_row = -1
    zero_col = -1

    # Dividimos el tablero en filas

    for num in state:                   # por cada casilla
        if num_col == M:                # si el último elemento que se metió estaba al final de una fila
            tablero.append([])          # creamos la fila siguiente
            num_row = num_row + 1       # aumentamos el contador de filas
            num_col = 0                 # ponemos el contador de columnas a 0 (la primera)
        tablero[num_row].append(num)    # Metemos la siguiente pieza en la casilla que le corresponde
        if(num == 0):
            zero_row = num_row
            zero_col = num_col
        num_col = num_col + 1           # aumentamos el contador de columnas (para que la siguiente pieza vaya en la casila de su derecha)

    # Detectamos los vecinos del estado actual

    posCasillaVacia = state.index(0)

    if(not zero_row-1< 0):
        #print("Vecino de arriba")
        vecino1 = (zero_col,zero_row-1)               # Vecino de arriba
        state1 = deepcopy(state)
        pieza1 = tablero[vecino1[1]][vecino1[0]]
        posPieza1EnState = state.index(pieza1)
        state1[posPieza1EnState] = 0
        state1[posCasillaVacia] = pieza1
        result.append(state1)
        #print(state1)
    if(not zero_col+1 > M-1):
        #print("Vecino a la derecha")
        vecino2 = (zero_col+1,zero_row)               # Vecino a la derecha
        state2 = deepcopy(state)
        pieza2 = tablero[vecino2[1]][vecino2[0]]
        posPieza2EnState = state.index(pieza2)
        state2[posPieza2EnState] = 0
        state2[posCasillaVacia] = pieza2
        result.append(state2)
        #print(state2)
    if(not zero_row+1 > M-1):
        #print("Vecino de abajo")
        vecino3 = (zero_col,zero_row+1)               # Vecino de abajo
        state3 = deepcopy(state)
        pieza3 = tablero[vecino3[1]][vecino3[0]]
        posPieza3EnState = state.index(pieza3)
        state3[posPieza3EnState] = 0
        state3[posCasillaVacia] = pieza3
        result.append(state3)
        #print(state3)
    if(not zero_col-1< 0):
        #print("Vecino a izquierda")
        vecino4 = (zero_col-1,zero_row)               # Vecino de la izquierda
        state4 = deepcopy(state)
        pieza4 = tablero[vecino4[1]][vecino4[0]]
        posPieza4EnState = state.index(pieza4)
        state4[posPieza4EnState] = 0
        state4[posCasillaVacia] = pieza4
        result.append(state4)
        #print(state4)

    return result

def heuristic(state):

    num_col = 1
    num_row = 1
    M = sqrt(len(state))
    result = 0
    initial_state = deepcopy(state)
    initial_state.sort()

    #print(state)
    #print(initial_state)

    # Debemos sacar la suma de fila+columna de la pieza en el ESTADO ACTUAL y restarle el mismo cálculo en el ESTADO INICIAL (en valor absoluto)

    for num in state: # ESTADO ACTUAL  # por cada casilla

        current_res = 1
        initial_res = 1

        if num_col == M+1:  # si el último elemento que se metió estaba al final de una fila
            num_row = num_row + 1  # aumentamos el contador de filas
            num_col = 1  # ponemos el contador de columnas a 0 (la primera)

        #current_res = num_row + num_col
        #print("CURRENT: El %s está en fila %s columna %s" % (num, num_row, num_col))

        initial_num_col = 1
        initial_num_row = 1
        for initial_num in initial_state: # ESTADO INICIAL
            if initial_num_col == M+1:
                initial_num_row = initial_num_row + 1
                initial_num_col = 1

            if(initial_num == num):
                #initial_res = initial_num_row + initial_num_col
                #print("INITIAL: El %s está en fila %s columna %s" % (initial_num, initial_num_row, initial_num_col))
                break

            initial_num_col = initial_num_col + 1

        result = result + abs(num_row - initial_num_row) + abs(num_col - initial_num_col)

        #if(result > 0):
        #    print("El número %s estaba en la fila %s y columna %s, mientras que en initial_state estaba en fila %s columna %s" % (num, num_row, num_col, initial_num_row, initial_num_col))


        num_col = num_col + 1  # aumentamos el contador de columnas (para que la siguiente pieza vaya en la casila de su derecha)

    #result = zero_row + zero_col
    return result

def N_Puzzle(N):

    # ------------------------ START: DATOS A MODIFICAR ----------------------- #
    algoritmo = "BEAM_SEARCH"    # Algorítmo de búsqueda a utilizar:
                                    # BEAM_SEARCH --> Algoritmo búsqueda_en_haz.py
                                    # BEAM_SEARCH_BACK --> Algoritmo búsqueda_en_haz_con_vuelta_atrás.py
                                    # BEAM_SEARCH_DISC --> Algoritmo búsqueda_en_haz_con_discrepancias.py
    max = 100                   # Número de instancias aleatorias
    B = 5                       # Anchura del haz
    memory = 5000               # Tamaño de memoria
    # ------------------------ END: DATOS A MODIFICAR ----------------------- #

    os.system("taskset -p 0xff %d" % os.getpid())

    num_Piezas = N
    num_Casillas = N + 1

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

        for a in range(num_Casillas):
            rand_num = random.randrange(num_Casillas)
            while rand_num in estado_inicial:
                rand_num = random.randrange(num_Casillas)
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
            algorithm = BS.busqueda_en_haz(B, [2,4,8,7,3,5,1,6,0], memory, estado_final)
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
tam = 8             # Tamaño del problema (Ejs: 8, 15, 24)
# ------------------------ END: DATOS A MODIFICAR ----------------------- #

N_Puzzle(tam)

#print(neighbours([0,1,2,3,4,5,6,7,8]))
#print(heuristic([2,1,0,3,4,8,6,7,5]))
#print(heuristic([0, 3, 6, 1, 4, 8, 2, 5, 7]))
#print(heuristic([0, 2, 1, 3, 4, 5, 6, 7, 8]))
#print(heuristic([0, 3, 2, 1, 4, 5, 6, 7, 8])) # 4
#print(heuristic([7,4,6,2,1,8,0,3,5])) #Debe salir 18
#print(heuristic([5,6,2,1,3,7,8,0,4])) #Debe salir 18

