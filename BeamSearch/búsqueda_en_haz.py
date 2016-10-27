# BeamSearch from Artificial Intelligence Subject

# Important data:
#   h           -> Heuristic function
#   B           -> The number of nodes that are stored at each level of the Breadth-First Search.
#   BEAM        -> Store the nodes that are to be expanded in the next loop of the algorithm.
#   hash_table  -> Store nodes that have been visited. (Memory)
#   g           -> Used to keep track of the depth of the search, which is the cost of reaching a node at that level.
#   SET         -> Set of successor nodes

# How it works:
# - Each time through the main loop of the algorithm, Beam Search adds all of the nodes connected to the nodes in the BEAM to its SET of successor nodes and then adds the B nodes with the best heuristic values from the SET to the BEAM and the hash table.
# - Note that a node that is already in the hash table is not added to the BEAM because a shorter path to that node has already been found.
# - This process continues until the goal node is found, the hash table becomes full (indicating that the memory available has been exhausted), or the BEAM is empty after the main loop has completed (indicating a dead end in the search).

from copy import deepcopy

import timeit

global heuristic
global neighbours

def busqueda_en_haz(B, initial_state, memory, goal_state):
    start = timeit.default_timer()
    # Initialization
    g = 0  # Cost
    hash_table = []  # Memory

    ####################################################################
    # Metemos el estado inicial tanto en el BEAM como en el hash_table #
    ####################################################################
    hash_table.append(initial_state)
    BEAM = [initial_state]
    num_estados_generados = 0
    time = 0

    # Main loop
    while len(BEAM) != 0:  # loop until the BEAM contains no nodes
        # print("-----------------")
        SET = []  # the empty set

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

        if len(SET) == 0:
            break

        ###################################
        # Ordenamos el SET por heurística #
        ###################################

        SETOrdered = []

        currentState = SET[0]

        for a in SET:  # Recorremos una vez el SET por cada elemento que contenga

            # Filtramos primero para asegurarnos de que el estado recorrido no esté ya en la lista ordenada
            cS = deepcopy(currentState)
            for eachElement in SET:
                if (cS not in SETOrdered):
                    break
                else:
                    cS = deepcopy(eachElement)
            currentState = deepcopy(cS)

            # Ahora cogemos el mejor de esta iteración, sin tener en cuenta los ya cogidos en iteraciones anteriores

            for state in SET:
                if (heuristic(state) < heuristic(currentState)) and (state not in SETOrdered):
                    # print("Supuestamente %s no está en %s" % (state, SETOrdered))
                    currentState = deepcopy(state)
            # print("sucessor: %s (Heur: %s)" % (currentState, heuristic(currentState)))
            SETOrdered.append(currentState)


        SET = SETOrdered

        # print("SET ordenado: %s" % (SET))

        #####################################################################
        # Generamos un nuevo BEAM a partir de los B mejores estados del SET #
        #####################################################################

        BEAM = []
        g = g + 1

        while len(SET) != 0 and B > len(BEAM):
            state = SET.pop(0)
            if state not in hash_table:
                # print("HT: %s MM: %s" % (len(hash_table), memory))
                if len(hash_table) >= memory:
                    ######################################################################################################
                    # Aquí llegamos en caso de quedarnos sin memoria mientras guardamos cada estado del BEAM en la misma #
                    ######################################################################################################
                    return float('inf')

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
                # print("A memoria: %s" % (state))

                BEAM.append(state)
                # print("BEAM: %s" % (BEAM))

    ##################################################################################################################
    # Aquí llegamos en caso de que lleguemos al final del árbol (a una hoja del mismo) sin encontrar solución alguna #
    ##################################################################################################################
    return [0, g, num_estados_generados, len(hash_table), time]
