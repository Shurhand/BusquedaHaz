# BeamSearch with Backtracking from Artificial Intelligence Subject

# Important data:
#   h           -> Heuristic function
#   B           -> The number of nodes that are stored at each level of the Breadth-First Search.
#   BEAM        -> Store the nodes that are to be expanded in the next loop of the algorithm.
#   hash_table  -> Store nodes that have been visited. (Memory)
#   g           -> Used to keep track of the depth of the search, which is the cost of reaching a node at that level.
#   SET         -> Set of successor nodes

from copy import deepcopy

import timeit

global heuristic
global neighbours

def busqueda_en_haz_backtracking(B, initial_state, memory, goal_state):
    start = timeit.default_timer()
    # Initialization
    g = 0  # Cost
    hash_table = []         # Memory
    hash_levels = []        # Nivel en el que se encuentra cada elemento de memoria (hash_table) (Las posiciones de este array se corresponden con las de hash_table)
    hash_level_index = []   # Posici�n del nivel que toca explorar (Las posiciones de este array se corresponden con las de cada nivel, siendo 0 el primer nivel)
    BEAM = [initial_state]
    nBacks = 0
    level = 0
    #backtrackingStop = False
    backtrackingCount = 10
    num_estados_generados = 0
    time = 0

    ####################################################################
    # Metemos el estado inicial tanto en el BEAM como en el hash_table #
    ####################################################################
    hash_table.append(initial_state)
    hash_levels.append(level)
    hash_level_index.append(0)

    # Main loop
    while len(BEAM) != 0:  # loop until the BEAM contains no nodes
        #print("-----------------")
        level = level + 1
        if hash_levels[len(hash_levels)-1] + 1 == level:
            hash_level_index.append(0)
        SET = []  # the empty set

        #if backtrackingStop:
        #    if backtrackingCount == 0:
        #        return "Ha hecho backtracking"
        #    backtrackingCount = backtrackingCount - 1

        # print("BEAM: %s" % (BEAM))

        ############################################
        # Generamos un nuevo SET a partir del BEAM #
        ############################################
        for state in BEAM:
            # print("neighbours: %s" % (neighbours(state)))
            contadoor = 0
            for successor in neighbours(state):
                num_estados_generados = num_estados_generados + 1
                # print("Sucesor %s: %s" % (contadoor, successor))
                if successor not in hash_table:
                    if successor == goal_state:
                        #########################################################################################
                        # Aquí llegamos en caso de que encontremos la solución entre los vecinos del BEAM (SET) #
                        #########################################################################################
                        g = g + 1
                        stop = timeit.default_timer()
                        time = stop - start
                        return [1, g, num_estados_generados, len(hash_table), time]
                    if successor not in SET:
                        # print("pre-SET: %s" % (SET))
                        SET.append(successor)
                        # print("añadido")
                        # print("post-SET: %s" % (SET))
                contadoor = contadoor + 1

        # print("SET sin ordenar: %s" % (SET))

        if len(SET) != 0:
            ###################################
            # Ordenamos el SET por heurística #
            ###################################

            SETOrdered = []

            currentState = SET[0]

            for a in SET:  # Recorremos una vez el SET por cada elemento que contenga

                # Filtramos primero para asegurarnos de que el estado recorrido no est� ya en la lista ordenada
                cS = deepcopy(currentState)
                for eachElement in SET:
                    if (cS not in SETOrdered):
                        break
                    else:
                        cS = deepcopy(eachElement)
                currentState = deepcopy(cS)

                # Ahora cogemos el mejor de esta iteraci�n, sin tener en cuenta los ya cogidos en iteraciones anteriores

                for state in SET:
                    if (heuristic(state) < heuristic(currentState)) and (state not in SETOrdered):
                        # print("Supuestamente %s no est� en %s" % (state, SETOrdered))
                        currentState = deepcopy(state)
                #print("sucessor: %s (Heur: %s)" % (currentState, heuristic(currentState)))
                SETOrdered.append(currentState)

            SET = SETOrdered

        ##########################################################################################
        # Filtramos los nodos que ya han sido visitados en este nivel, para no volver a tomarlos #
        ##########################################################################################
        SETToFilter = deepcopy(SET)
        #print("hash_level_index[level]: %s" % (hash_level_index[level]))
        count3 = 0
        #print("SET pre-filter: %s" % (SET))
        for node in SETToFilter:
            if count3 < hash_level_index[level]:
                #print("Already visited: %s" % (SET.pop(0)))
                SET.pop(0)
            count3 = count3 + 1

        #################################################################
        # En caso de llegar a una hoja del árbol (no hay más sucesores) #
        #################################################################
        if len(SET) == 0: # SI LLEGAMOS A UNA HOJA DEL �RBOL (No hay sucesores)
            #backtrackingStop = True
            #print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ Backtracking \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
            #print("nivel: %s" % (level))
            #print("hash_table size: %s" % (len(hash_table)))
            #print("hash_levels size: %s" % (len(hash_levels)))
            
            ##################################################################
            # Borramos los bloques generados en este nivel y del nivel padre #
            ##################################################################
            nivel = level - 1
            count5 = len(hash_levels) - 1
            while count5 >= 0:
                if hash_levels[count5] == nivel:
                    hash_table.pop(count5)
                count5 = count5 - 1
            hash_levels = list(filter((nivel).__ne__, hash_levels)) # Borramos todos los elementos de este nivel

            nivel = level
            count5 = len(hash_levels) - 1
            while count5 >= 0:
                if hash_levels[count5] == nivel:
                    hash_table.pop(count5)
                count5 = count5 - 1
            hash_levels = list(filter((nivel).__ne__, hash_levels)) # Borramos todos los elementos de este nivel

            level = level - 2 # Volvemos al nivel del Padre (BEAM)

            #################################################
            # Volvemos el BEAM anterior (al conjunto padre) #
            #################################################
            BEAM = []
            count4 = 0
            for lvl in hash_levels:
                if lvl == level:
                    BEAM.append(hash_table[count4])
                count4 = count4 + 1

            #print("BEAM tras Backtracking: %s" % (BEAM))

            hash_level_index[level+1] = hash_level_index[level+1] + B

            hash_level_index[level + 2] = 0

            #print("post-hash_table size: %s" % (len(hash_table)))
            #print("post-hash_levels size: %s" % (len(hash_levels)))

            continue

        # print("SET ordenado: %s" % (SET))

        BEAM = []
        g = g + 1

        #####################################################################
        # Generamos un nuevo BEAM a partir de los B mejores estados del SET #
        #####################################################################
        while len(SET) != 0 and B > len(BEAM):
            state = SET.pop(0)
            if state not in hash_table:
                #print("HT: %s MM: %s" % (len(hash_table), memory))
                if len(hash_table) >= memory:
                    ######################################################################################################
                    # Aquí llegamos en caso de quedarnos sin memoria mientras guardamos cada estado del BEAM en la misma #
                    ######################################################################################################
                    #backtrackingStop = True
                    #print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ Backtracking (memory) \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
                    #print("nivel: %s" % (level))
                    #print("hash_table size: %s" % (len(hash_table)))
                    #print("hash_levels size: %s" % (len(hash_levels)))

                    ##################################################################
                    # Borramos los bloques generados en este nivel y del nivel padre #
                    ##################################################################
                    nivel = level - 1
                    count5 = len(hash_levels) - 1
                    while count5 >= 0:
                        if hash_levels[count5] == nivel:
                            hash_table.pop(count5)
                        count5 = count5 - 1
                    hash_levels = list(filter((nivel).__ne__, hash_levels)) # Borramos todos los elementos de este nivel

                    nivel = level
                    count5 = len(hash_levels) - 1
                    while count5 >= 0:
                        if hash_levels[count5] == nivel:
                            hash_table.pop(count5)
                        count5 = count5 - 1

                    hash_levels = list(filter((nivel).__ne__, hash_levels)) # Borramos todos los elementos de este nivel

                    level = level - 2 # Volvemos al nivel del Padre (BEAM)

                    #################################################
                    # Volvemos el BEAM anterior (al conjunto padre) #
                    #################################################
                    BEAM = []
                    count4 = 0
                    for lvl in hash_levels:
                        if lvl == level:
                            BEAM.append(hash_table[count4])
                        count4 = count4 + 1

                    #print("BEAM tras Backtracking: %s" % (BEAM))

                    hash_level_index[level+1] = hash_level_index[level+1] + B

                    hash_level_index[level + 2] = 0

                    #print("post-hash_table size: %s" % (len(hash_table)))
                    #print("post-hash_levels size: %s" % (len(hash_levels)))

                    continue

                    #return float('inf')

                    # para averiguar si hemos implementado bien el que no se tomen en cuenta nodos ya explorados
                    # lst = hash_table
                    # lst2 = []
                    # for key in lst:
                    #     if key not in lst2:
                    #         lst2.append(key)
                    #     else:
                    #         return "Acabó: %s" % (key)
                    # return "No se repite nada"

                hash_table.append(state)
                #print("A memoria: %s" % (state))

                BEAM.append(state)
                hash_levels.append(level)
                # print("HT: %s MM: %s" % (len(hash_table), memory))
        #print("BEAM: %s" % (BEAM))
        #print("level: %s" % (level))

    ############################################################################################################
    # Aquí llegamos en caso de que recorramos todo el árbol sin encontrar solución alguna (no debería ocurrir) #
    ############################################################################################################
    return [0, g, num_estados_generados, len(hash_table), time]
