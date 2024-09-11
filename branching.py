from graph_io import load_graph
from graph import *
from basic_colorref import *
from fast_colorref import *
import copy
import time
import os


# bool automorphism: true -> count all isomorphisms; false -> stop at first isomorphism
def count_isomorphism(G, H, coloring, automorphism=True):
    old_coloring = copy.deepcopy(coloring)

    graphs = [G, H]
    # refined = basic_colorref(graphs, old_coloring)
    refined = fast_colorref(graphs, old_coloring)

    refined_g, refined_h = refined[0], refined[1]

    if sorted(refined_g) != sorted(refined_h):
        return 0

    # if we get here, graphs must be balanced => enough to perform discrete/bijection check only on one
    if len(refined_g) == len(set(refined_g)):
        return 1

    # define the new branching color and assign
    colornums_g = G.colornums
    grouped_colornums = [[x for _ in range(colornums_g.count(x))] for x in set(colornums_g)]
    filtered_colornums = [color for color in grouped_colornums if len(color) > 1]
    branch_color = sorted(filtered_colornums, key=len)[0][0]

    x = -1
    for index, color in enumerate(refined_g):
        if color == branch_color:
            x = index
            break

    num = 0
    old_coloring[0].append(x)

    for y, color in enumerate(refined_h):
        if branch_color == color:
            # update coloring
            next_coloring = copy.deepcopy(old_coloring)
            next_coloring[1].append(y)

            num += count_isomorphism(G, H, next_coloring, automorphism)

            # stop here if no need to count automorphisms
            if not automorphism and num > 0:
                break
    return num


def branch_result(file, check_automorphism):
    graph_list1 = []
    graph_list2 = []

    with open(f"{file}") as f:
        graph_list1 = load_graph(f, Graph, True)[0]

    with open(f"{file}") as fi:
        graph_list2 = load_graph(fi, Graph, True)[0]

    array = []
                
    for i in range(len(graph_list1)):
        array.append(i)
    
    array_2 = [[0]]
    for i in range(1, len(array)):
        c = 0
        for j in range(len(array_2)):
            if count_isomorphism(graph_list1[array_2[j][0]], graph_list2[i], [[],[]], False) > 0:
                array_2[j].append(i)
                c = 1
        if c == 0:
            array_2.append([i])
    
    if not check_automorphism:
        return array_2

    result = []
    for sublist in array_2:
        num = count_isomorphism(graph_list1[sublist[0]], graph_list2[sublist[0]], [[], []], True)
        result.append((sublist, num))

    return result


def run():
    directory = r"absolute_path/to/directory"

    for file_name in os.listdir(directory):
        filepath = os.path.join(directory, file_name)
        
        if os.path.isfile(filepath):
            if not file_name.endswith(".gr") and not file_name.endswith(".grl"):
                continue

            check_auto = False
            if file_name.endswith(".gr"):
                check_auto = True
            elif file_name.endswith(".grl") and "aut" in file_name.lower():
                check_auto = True

            start = time.time()
            res = branch_result(filepath, check_auto)
            end = time.time()
            
            print()
            print(file_name)
            print("Sets of isomorphic graphs with automorphisms:")
            for t in res:
                if check_auto:
                    print(f"{t[0]}: {t[1]}")
                else:
                    print(t)

            print(f"\nTime: {end - start} seconds")

    
if __name__ == "__main__":
    start = time.time()
    run()
    end = time.time()
    print(f"\nTotal compilation time: {end - start} seconds\n")
