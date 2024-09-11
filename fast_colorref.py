from graph import *
from graph_io import *
import queue

# we need a pi for containing all the colors
# a queue which is needed for colors to be refined
def fast_colorref(G, lists):
    c = [0]
    group_partitions = []

    if not any(lists):
        for k in range(len(G)):
            partition = {}
            for vertex in G[k].vertices:
                vertex.label = vertex.degree
                if vertex.label > c[0]:
                    c[0] = vertex.label
                if vertex.label not in partition.keys():
                    partition[vertex.label] = [vertex]
                else:
                    partition[vertex.label].append(vertex)
            group_partitions.append(partition)
    else:
        for k in range(len(G)):
            partition = {}
            for vertex in G[k].vertices:
                if G[k].vertices.index(vertex) in lists[k]:
                    vertex.label = lists[k].index(G[k].vertices.index(vertex)) + 1
                else:
                    vertex.label = 0
                if vertex.label not in partition.keys():
                    partition[vertex.label] = [vertex]
                else:
                    partition[vertex.label].append(vertex)
                if c[0] < vertex.label:
                    c[0] = vertex.label
            group_partitions.append(partition)

    all_partition_keys = sorted(set([key for dict_ in group_partitions for key in dict_.keys()]))

    q = queue.Queue()
    for k in all_partition_keys:
        q.put(k)

    while not q.empty():
        # print(q.queue)
        partition_new = []
        #A list of all the A's of all the graphs
        A = []
        color = q.get()
        for k in group_partitions:
            if color not in k.keys():
                partition_new.append(k)
                A.append([])
                continue
            a = []
            C = k.get(color)
            for vertex in C:
                for neighbour in vertex.neighbours:
                    if neighbour not in a:
                        a.append(neighbour)
            A.append(a)
            partition_new.append({})
        
        maximum_colors = sorted(set([key for dict_ in group_partitions for key in dict_.keys()]))

        for i in range(len(maximum_colors)):
            b = False
            for graph_dict in group_partitions:
                if maximum_colors[i] not in graph_dict.keys():
                    continue
                color_vertex = graph_dict.get(maximum_colors[i])
                d1 = []
                d2 = []
                for vertex in color_vertex:
                    if vertex in A[group_partitions.index(graph_dict)]:
                        d2.append(vertex)
                    else:
                        d1.append(vertex)
                if len(d1) == 0 or len(d2) == 0:
                    partition_new[group_partitions.index(graph_dict)][color_vertex[0].label] = color_vertex
                    continue
                b = True
                partition_new[group_partitions.index(graph_dict)][c[0] + 1] = d1
                partition_new[group_partitions.index(graph_dict)][d2[0].label] = d2
                if d2[0].label in list(q.queue):
                    if c[0]+1 not in list(q.queue):
                        q.put(c[0]+1)
                else:
                    if (len(d2) < len(d1)):
                        if d2[0].label not in list(q.queue):
                            q.put(d2[0].label)
                    else:
                        if c[0]+1 not in list(q.queue):
                            q.put(c[0]+1)
                for element in d1:
                    element.label = c[0] + 1
            if b:
                c[0] += 1
        group_partitions = partition_new
    for k in range(len(G)):
        for vertex in G[k].vertices:
            vertex.colornum = vertex.label

    return [[vertex.label for vertex in graph.vertices] for graph in G]


            