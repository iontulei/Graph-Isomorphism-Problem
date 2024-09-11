from graph_io import load_graph, write_dot
from graph import *

def color_refinement(graphs, is_discreteGraph, lists):
    #   Iterate through graphs
    for graph in graphs:

        #   Stores the last max color used
        max_color = 0

        #   Refinement 1
        if not any(lists):
            for vertex in graph.vertices:
                vertex.colornum = int(vertex.degree)
                #   Store max value of a color used
                max_color = max(max_color, vertex.colornum)
        else:
            for index in range(len(graph.vertices)):
                vertex = graph.vertices[index]
                if index in lists[graphs.index(graph)]:
                    vertex.colornum = lists[graphs.index(graph)].index(index) + 1
                else:
                    vertex.colornum = 0
                #   Store max value of a color used
                max_color = max(max_color, vertex.colornum)
        #   Already 1 after Refinement 1
        iterations = 1

        #    Have condition while the color is being changed
        max_color_changed = True

        #   Refinement 2
        while max_color_changed:

            #    Store vertices which color may change
            structured_vertices = {}

            #   Turn the flag off until no change for max_color
            max_color_changed = False

            #   Add an iteration
            iterations += 1

            #   Group and sort the vertices to be changed by their colors and by their neighbours
            structured_vertices = init_group(graph.vertices)

            #   Store the colors encountered and change those that are already there
            visited_colors = set()

            #   Iterate through vertices groups with same colors and neighbors 
            for vertex_properties, vertices in structured_vertices:

                #   Get the color from the vertex properties
                color = vertex_properties[0]

                #   Find the vertices with the same color but not with same neighbours
                if color in visited_colors:

                    #    Change the colors of those vertices
                    max_color += 1

                    #    Set the condition to true
                    max_color_changed = True

                    #   Change color of each vertice with same neighbours and color
                    for vertex in vertices:
                        vertex.colornum = max_color
                else:
                    #  Color was not saved so add it
                    visited_colors.add(color)

        #       Check if the graph is discrete or not
        is_discreteGraph[graph] = [len(visited_colors) == len(graph.vertices), iterations-1]
    return [[vertex.colornum for vertex in graph.vertices] for graph in graphs]

# Create groups of verticies with their color and neighbors as a key
def init_group(vertices):

    # A dictionary to store the properties of the vertex and the vertex itself
    verticies_dict = dict()

    for vertex in vertices:

        #   Compute the key which will be a tuple of vertex color and its neighbours colors in string
        key = (vertex.colornum, sort_vertices_by_neighbors(vertex.neighbours))

        #   Add the vertex to its properties as a value
        verticies_dict.setdefault(key, []).append(vertex)

    #   Here sort the vertices by the color
    structured_vertices = sort_vertices_by_colors(verticies_dict.items())

    return structured_vertices

#   Return the sorted string of neighbour colos
def sort_vertices_by_neighbors(neighbours):
    sorted_neighbours = ''.join(str(color) for color in sorted(neighbour.colornum for neighbour in neighbours))
    #   Return sorted string
    return sorted_neighbours

#   Sort by vertex groups by colors
def sort_vertices_by_colors(structured_vertices):
    return sorted(structured_vertices, key=lambda vertex_properties: vertex_properties[0])

#   Check if two graphs are isomorph by their edges
def isomorphic(g1, g2, is_discreteGraph):
    #  If graphs have different number of vertices or don't have them same isDiscrete value then return false
    if len(g1.vertices) != len(g2.vertices) or is_discreteGraph[g1][0] != is_discreteGraph[g2][0]:
        return False

    #  Get graph edges sorted
    graph1_edges = sorted([sorted((edge.head.colornum, edge.tail.colornum)) for edge in g1.edges]) 
    graph2_edges = sorted([sorted((edge.head.colornum, edge.tail.colornum)) for edge in g2.edges]) 

    #  If edges are equal return true
    return graph1_edges == graph2_edges

def basic_colorref(file):
    #   Open the file
    with open(f"{file}") as f:
        L = load_graph(f, Graph, True)

    #   Save info about every graph : isDiscrete/iterations
    is_discreteGraph = dict() 

    #   Apply color refinement on graphs
    color_refinement(L[0], is_discreteGraph=is_discreteGraph)

    #   Storage where I will make the needed format
    isomorph_graphs = []

    for i, g in enumerate(L[0]):
        #   Check if i is already in any group
        is_graphInList = False
        for graphs in isomorph_graphs:
            if i in graphs[0]:
                is_graphInList = True
                break

        # If i is not found in any existing group
        if not is_graphInList:
            #    Create new group with that index
            current_group = [i]

            # Check isomorphism with other graphs
            for j in range(i + 1, len(L[0])):
                if isomorphic(g, L[0][j], is_discreteGraph):
                    current_group.append(j)

            # Append to the new group
            isomorph_graphs.append((current_group, is_discreteGraph.get(g)[1], is_discreteGraph.get(g)[0]))

    return isomorph_graphs