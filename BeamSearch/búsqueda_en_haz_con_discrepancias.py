# BeamSearch w/ Discrepancies from Artificial Intelligence Subject
# Gastar la discrepancias lo antes posible

from copy import deepcopy

import timeit

# Variables globlales que almacenan la heurística y los vecinos de un estado.
global heuristic
global neighbours

# Variable estática que almacena los estados generados.
# Permite almacenar los estados generados de todas las llamadas recursivas.
class Estados_generados():
    num_estados_generados = 0

# Accedemos a variable mediante una instancia.
# Para entenderlo mejor mira la URL que te dejo dónde te explican cómo se usan las variables estáticas en Python.
# URL: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
estados_generados_instance = Estados_generados()

# Variable estática que almacena la memoria usada.
# Permite almacenar todos los estados almacenados que se han ido añadiendo al hashtable en todas las llamadas recursivas.
class Memory_table():
    memory_table = []

# Accedemos a variable mediante una instancia.
# Para entenderlo mejor mira la URL que te dejo dónde te explican cómo se usan las variables estáticas en Python.
# URL: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
memory_table_instance = Memory_table()

# Algoritmo padre.
# Es al que se llama desde N-puzzle y N-crepes.
# Recibe:
    # initial_state: Estado inicial generado de forma aleatoria desde N-puzzle y N-crepes.
    # goal_state: Estado final al que queremos llegar.
    # B: Ancho del Haz que vamos a elegir.
    # memory: Tamaño de la memoria disponible para este problema.
def BULB(initial_state, goal_state, B, memory):

    # Marcador de tiempo inicial.
    start = timeit.default_timer()

    # Initialization:

    # Número de discrepancias del problema.
    discrepancies = 0

    # Variable que aparentamente no se usa.
    # Quizás haya que quitarla xD
    state_level = 0;

    # Tabla dónde almacemos los estados visitados.
    hash_table = [initial_state]

    # Tabla de misma longitud que hash_table que nos dice en qué nivel del árbol está cada estado.
    hash_levels = [0]

    # Nivel máximo de vueltas que puede dar el while de abajo.
    # Sin esta variable, el número de vueltas podría ser casi-infinito.
    limitWhile = 1000000

    # Inicializamos la varible declarada antes como variable estática.
    num_estados_generados = 0

    # Nos indica el tiempo que tarda el algoritmo.
    time = 0

    # print("Parada BULB 1")

    # Bucle dónde se ejecuta el algoritmo.
    while limitWhile != 0:

        # print("^^^^^^^^^^")
        # print("Discrepancia: %s" % (discrepancies))

        # pathlength nos indica la distancia entre el estado inicial al estado final del problema.
        # En otras palabras, es la solución del problema.
        # Llamamos a BULBprobe, que será la propia lógica del algoritmo.
        pathlength = BULBprobe(0, discrepancies, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)

        #print(estados_generados_instance.num_estados_generados)
        #print(len(memory_table_instance.memory_table))

        # No indica si resultado es válido.
        # Si no es infinito significa que tenemos solución.
        if pathlength < float('inf'):
            # Generamos la variable de tiempo de fin del algoritmo.
            stop = timeit.default_timer()
            # Calculamos el tiempo de ejecución del algoritmo.
            time =  stop - start
            # Devolvemos el resultado
            # Originalmente devolvía sólo el pathlength pero es necesario devolver más datos para la ejecución de las pruebas.
            # Devolvemos:
                # 1: Nos indica que hemos encontrado solución. Se puede entrender como boolean haySolucion.
                # pathlength: Resultado propiamente dicho. Es la distancia entre el estado inicial y el final.
                # estados_generados_instance.num_estados_generados: Guardamos el número de estados generados.
                # len(memory_table_instance.memory_table): Guardamos los elementos que han entrado en hash_table.
                    # Ahora me pegunto por qué lo guardo entero y no aumento el contador como hago en la variable anterior.
                # time: Nos indica el tiempo que tarda en ejecutarse el algoritmo.
            return [1, pathlength, estados_generados_instance.num_estados_generados, len(memory_table_instance.memory_table), time]

        # Si el resultado es infinito:
        # Aumentamos el número de discrepancias permitidas.
        discrepancies = discrepancies + 1
        # Disminuimos el número de iteraciones permitidas del while.
        limitWhile = limitWhile - 1
        # Volvemos al while.

# Es la lógica del algoritmo.
# Recibe:
    # depth: Profundidas del árbol en la que estamos
    # discrepancias: Número de discrepancias permitidas.
    # hash_table: Tabla que guarda los estados visitados.
    # hash_levels: Tabla, de mismo tamaño que hash_table, que guarda la profundidas de los estados visitados.
    # goal_state: Estado final al que queremos llegar.
    # memory: Tamaño máximo del hash_table. Memoria disponible para el problema.
    # num_estados_generados: Contador de número de estados generados.
def BULBprobe(depth, discrepancies, B, hash_table, hash_levels, goal_state, memory,num_estados_generados):

    # print("Hash Table: %s" % (hash_table))
    # print("Hash Levels: %s" % (hash_levels))

    # A la izquierda:
        # SLICE: Conjunto de estados a tratar en esta iteración
        # value: Solución del problema.
        # index: Marca a partir de qué elemento vamos a continuar con el algoritmo.
    # A la derecha:
        # nextSlice(): Genera el conjunto de estados a tratar.
        # Recibe:
            # depth: Profundidad en la que nos encontramos.
            # 0: Hace refencia al índice a partir del cual empiezan a contarse los estados de un SLICE.
            # B: Tamaño del haz.
            # hash_table: Tabla que guarda los estados visitados.
            # hash_levels: Tabla, de mismo tamaño que hash_table, que guarda la profundidas de los estados visitados.
            # goal_state: Estado final al que queremos llegar.
            # memory: Tamaño máximo del hash_table. Memoria disponible para el problema.
            # num_estados_generados: Contador de número de estados generados.
    [SLICE, value, index] = nextSlice(depth, 0, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)

    # print("SLICE: %s" % (SLICE))
    # print("value: %s" % (value))
    # print("index: %s" % (index))

    # Si value es mayor o igual que 0 devolvemos su valor.
    # Luego se verá que en algunos casos se devuelve -1 por eso este if.
    if value >= 0:
        return value

    # Aquí vemos si se permiten discrepancias.
    # En este caso, no se permiten discrepancias.
    if discrepancies == 0:

        # Preguntamos si hay estados a tratar.
        # En este caso, al no haber, se devueve infinito y volvemos al BULB()
        if SLICE is []:
            return float('inf')

        # Calculamos el tamaño del camino con una llamada recursiva.
        # Al tratarse de un escalón más, depth se incrementa.
        pathlenght = BULBprobe(depth+1, 0, B, hash_table, hash_levels, goal_state, memory,num_estados_generados)

        # Aquí vamos borrando del hash_table los elementos del SLICE y sus posiciones del hash_levels.
        for s in SLICE:
            if s in hash_table:
                pos_in_hash_table = hash_table.index(s)
                hash_table.remove(s)
                # memory_table_instance.memory_table.remove(s)
                hash_levels.pop(pos_in_hash_table)

        # Devolvemos la distancia entre el estado incial y el final.
        return pathlenght

    # En este caso sí se permiten discrepancias.
    else:

        # Si el SLICE nos está vacío, eliminamos todos sus elementos del hash_table y sus posiciones del hash_levels
        if SLICE is not []:
            for s in SLICE:
                if s in hash_table:
                    pos_in_hash_table = hash_table.index(s)
                    hash_table.remove(s)
                    # memory_table_instance.hash_table2.remove(s)
                    hash_levels.pop(pos_in_hash_table)

        # -
        while True:

            # Calcumos de nuevo SLICE, value e index, pero esta vez, le pasamos el número de discrepancias que haya, no 0 como antes.
            [SLICE, value, index] = nextSlice(depth, index, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)


            # Si value es mayor o igual que 0 y menor que infinito devolvemos su valor.
            # Luego se verá que en algunos casos se devuelve -1 o infinito, por eso este if.
            if value >= 0:
                if value < float('inf'):
                    return value
                else:
                    break

            # Si no hay estados a tratar en SLICE, salimos de while.
            if SLICE is []:
                continue

            # Calculamos el tamaño del camino.
            # Aumentamos la profundidad porque estamos adentrándonos en el grafo.
            # Disminuimos la discrepancias porque ya se ha usado el token.
            pathlenght = BULBprobe(depth+1, discrepancies-1, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)

            # Eliminamos de hash_table todos los estados del SLICE y sus posiciones del hash_levels
            for s in SLICE:
                if s in hash_table:
                    pos_in_hash_table = hash_table.index(s)
                    hash_table.remove(s)
                    # memory_table_instance.memory_table.remove(s)
                    hash_levels.pop(pos_in_hash_table)

            # Si el tamaño del caminos es menor que infinito es que hemos encontrado solución y la devolvemos.
            if pathlenght < float('inf'):
                return pathlenght

        # Calculamos de nuevo SLICE, value e index.
        # Discrepancias vuelve a valer 0 porque hemos gastado todos los token de discrepancias permitidas.
        [SLICE, value, index] = nextSlice(depth, 0, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)

        # Si value es mayor o igual que 0 devolvemos su valor.
        # Luego se verá que en algunos casos se devuelve -1 por eso este if.
        if value >= 0:
            return value

        # Si no hay estados a tratar, devolvemos infinito.
        if SLICE is []:
            return float('inf')

        # Calculamos el tamaño del camino.
        # Incrementamos la profundidas porque estamos en un nivel inferior en el árbol.
        pathlenght = BULBprobe(depth+1, discrepancies, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)

        # Borramos los estados de SLICE del hash_table y sus posiciones del hash_levels.
        for s in SLICE:
            if s in hash_table:
                pos_in_hash_table = hash_table.index(s)
                hash_table.remove(s)
                # memory_table_instance.memory_table.remove(s)
                hash_levels.pop(pos_in_hash_table)

        # Devolvemos la longitud del árbol.
        return pathlenght

# Aquí calculamos el siguinete grupo de elementos a tratar.
def nextSlice(depth, index, B, hash_table, hash_levels, goal_state, memory, num_estados_generados):

    # Tabla dnde guardaremos los estados del hash_level de la profundidas dada.
    currentlayer = []

    # Contador que actua como puntero a la posición de hash_table.
    pos_in_list = 0

    # g() obtener el nivel del estado: Sacar de la memoria el bloque que está en el nivel s
    # Recorremos el hash_levels.
    for i in hash_levels:
        # Cuando un nivel del hash_levels coreesponda con la profundidad...
        if i == depth:

            # print("pos_in_list: %s" % (pos_in_list))
            # print("hash_table: %s" % (hash_table))
            # print("hash_levels: %s" % (hash_levels))

            # ... se lo añadimos al currentlayer.
            currentlayer.append(hash_table[pos_in_list])
        # Incrementamos el puntero a la posición de hash_table.
        pos_in_list = pos_in_list + 1


    # Generamos los sucesores que nos están en hash_table.
    SUCCS = generateNewSuccessor(currentlayer, hash_table, num_estados_generados)

    # Si no hay sucesores o el index, que marca a partir de qué elemento vamos a continuar con el algoritmo, apunta fuera de la lista...
    if SUCCS is [] or index == len(SUCCS):
        # ... Devolvemos:
            # SLICE vacío
            # value infinito
            # index -1
        return [[], float('inf'), -1]

    # Si el estado final está dentro de los sucesores,
    if goal_state in SUCCS:
        # ... devolvemos
            # SLICE vacío
            # value la solución del problema.
            # indez -1
        return [[], depth + 1, -1]

    # Vaciamos el SLICE
    SLICE = []

    # Guardamos en i el valor de index.
    i = index;

    # Mientras que i no llegue al final de los sucesores y el SLICE no se mayor que el tamaño del haz.
    while(i < len(SUCCS) and len(SLICE) < B):

        # Si el sucesor en la posición i no está en el hash_table...
        if(SUCCS[i] not in hash_table):

            ## g(SUCCS[i]) := depth + 1

            # Añadimos al SLICE el estado
            SLICE.append(SUCCS[i])

            # Añadimos al hash_table el estado.
            hash_table.append(SUCCS[i])
            memory_table_instance.memory_table.append(SUCCS[i])

            # Añadimos al hash_levels la profundidad del estado.
            hash_levels.append(depth + 1)

            # Si se excede la memoria...
            if len(hash_table) >= memory:
                # ... borramos lo que haya todos lo elementos que hubiesemos añadido en esta iteración...
                for s in SLICE:
                    if s in hash_table:
                        pos_in_hash_table = hash_table.index(s)
                        hash_table.remove(s)
                        memory_table_instance.memory_table.remove(s)
                        hash_levels.pop(pos_in_hash_table)

                # ... y devolvemos un SLICE vacío, un value infinito y un index -1
                return [[], float('inf'), -1]

        # Incrementamos el contador y seguimos con el siguiente sucesor.
        i = i + 1

    # Devolvemos el SLICE, value -1 e index con el valor que haya quedado i.
    return [SLICE, -1, i]

# Funciona bien.
# Comprobado con un BEAM de tamaño 1 y 2
# Comprobado con hash_table vacío y con varios estados incluidos

# Aquí se generan los sucesores que no estén en hash_table.
# Básicamente es nuestro neighbours pero con la variante de que comprueba el hash_table
def generateNewSuccessor(stateset, hash_table, num_estados_generados):

    # Tabla para guardar los sucesores desordenados.
    UnsortedSUCCS = []

    # Generate the SET nodes
    for state in stateset:
        contadoor = 0
        for successor in neighbours(state):
            if successor not in hash_table:
                if successor not in UnsortedSUCCS:
                    UnsortedSUCCS.append(successor)
            contadoor = contadoor + 1

    ## Sort states in SUCCS in order of increasing heuristic values

    # Si no hay sucesores, es una perdida de tiempo ordenarlos y se devuelve la lista vacía.
    if not UnsortedSUCCS:
        return []

    SUCCS = []
    # print("UnsortedSUCCS: %s" % (UnsortedSUCCS))
    currentState = UnsortedSUCCS[0]

    for a in UnsortedSUCCS:
        cS = deepcopy(currentState)
        for eachElelement in UnsortedSUCCS:
            if cS not in SUCCS:
                break
            else:
                cS = deepcopy(eachElelement)
        currentState = deepcopy(cS)

        for state in UnsortedSUCCS:
            if (heuristic(state) < heuristic(currentState)) and (state not in SUCCS):
                currentState = deepcopy(state)
        SUCCS.append(currentState)

    # print("SUCCS: %s" % (SUCCS))
    # print("==========")

    # Aumentamos el contador de estados generados.
    estados_generados_instance.num_estados_generados = estados_generados_instance.num_estados_generados + len(SUCCS)

    return SUCCS