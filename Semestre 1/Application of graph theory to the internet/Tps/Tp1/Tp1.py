import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

Liste_aretes = []
i = 1

print("=" * 100)
nbr_sommets = int(input("Entrer le nombre de sommets: "))
Liste_sommets = list(map(lambda i: chr(65 + i), range(nbr_sommets)))
print(f"La liste des sommets est: \033[93m{Liste_sommets}\033[0m")

print("=" * 100)
while(1):
    arete = input(f"Entrer l'arete numero {i}: ").upper()
    reverse_arete = arete[::-1]
    if (arete != "FIN"):
        if len(arete) != 3 or arete[1] != '-':
            print("\033[91mLa forme d'arete devrait etre comme ca: sommet1-sommet2\033[0m")
        elif arete[0] not in Liste_sommets and arete[2] not in Liste_sommets:
            print(f"\033[91mLes deux sommet {arete[0]} et {arete[2]} n'existe pas dans la liste des sommets!\033[0m")   
        elif arete[0] not in Liste_sommets:
            print(f"\033[91mLe sommet {arete[0]} n'existe pas dans la liste des sommets!\033[0m")
        elif arete[2] not in Liste_sommets:
            print(f"\033[91mLe sommet {arete[2]} n'existe pas dans la liste des sommets!\033[0m")
        elif (arete in Liste_aretes) or (reverse_arete in Liste_aretes):
            print("\033[91mVous avez dega entrer cette arete!\033[0m")
        else:
            Liste_aretes.append(arete)
            i += 1
    else:
        break
if Liste_aretes:
    print(f"La liste des aretes est: \033[93m{Liste_aretes}\033[0m")
else:
    print("\033[93mIl n'existe pas des aretes!\033[0m")

print("=" * 100)
matrix = np.zeros((nbr_sommets,nbr_sommets), dtype=int)
for arete in (Liste_aretes):
    first_sommet = arete[0]
    second_sommet = arete[2]
    
    first_sommet_index = Liste_sommets.index(first_sommet)
    second_sommet_index = Liste_sommets.index(second_sommet)
    
    matrix[first_sommet_index][second_sommet_index] = 1
    matrix[second_sommet_index][first_sommet_index] = 1
print(f"La matrice d'adjacence est: \n\033[93m{matrix}\033[0m")

G = nx.from_numpy_array(matrix)
mapping = dict(zip(range(nbr_sommets), Liste_sommets))
G = nx.relabel_nodes(G, mapping)

plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, node_color='lightblue', node_size=2000, font_size=15, font_weight='bold', edge_color='gray')
plt.show()

print("=" * 100)
degres = []
for i in range(nbr_sommets):
    degres.append(0)
    
for i in range(nbr_sommets):
    for j in range(nbr_sommets):
        if matrix[i][j] == 1:
            degres[i] += 1
for i in range(nbr_sommets):
    print(f"Le degre du sommet \033[93m{chr(65 + i)}\033[0m est: \033[93m{degres[i]}\033[0m")

print("=" * 100)

def find_eulerian_path_or_cycle(matrix, start_vertex):
    stack = [start_vertex]
    path = []
    while stack:
        start_sommmet = stack[-1]
        for end_sommet in range(nbr_sommets):
            if matrix[start_sommmet][end_sommet] == 1:
                stack.append(end_sommet)
                matrix[start_sommmet][end_sommet] = matrix[end_sommet][start_sommmet] = 0
                break
        else:
            path.append(stack.pop())
    return path[::-1]

impair = 0
for i in range(nbr_sommets):
    if (degres[i] % 2) != 0:
        impair += 1
        
if not nx.is_connected(G):
    print("Le graphe est: \033[93mnon connecte\033[0m Donc il est: \033[93mnon eulerien\033[0m")
elif not impair:    
    print("Le graph est: \033[93meulerien\033[0m")
    start_vertex = 0
    cycle = find_eulerian_path_or_cycle(matrix.copy(), start_vertex)
    cycle_str = ' -> '.join(Liste_sommets[v] for v in cycle)
    print(f"Le cycle eulerien est: \033[93m{cycle_str}\033[0m")
elif impair == 2:
    print("Le graph est: \033[93msemi eulerien\033[0m")
    start_vertex = degres.index(next(d for d in degres if d % 2 != 0))
    path = find_eulerian_path_or_cycle(matrix.copy(), start_vertex)
    path_str = ' -> '.join(Liste_sommets[v] for v in path)
    print(f"La chaine eulerienne est: \033[93m{path_str}\033[0m")
else:
    print("Le graph est: \033[93mnon eulerien\033[0m")