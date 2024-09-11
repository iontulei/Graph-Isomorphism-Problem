# Implementation Project Graph Isomorphism

**Module 7, Bachelor of Technical Computer Science, University of Twente**

**Date:** 15-04-2024

**Team 65:**
- [Dragoș Erhan](https://github.com/Headpoint2042)  
- [Ion Tulei](https://github.com/iontulei)
- [Alexandru Verhovețchi](https://github.com/Alex-Verh)

## Project Overview

This project is part of Module 7 of the Technical Computer Science bachelor's program at the University of Twente. It focuses on solving the **Graph Isomorphism Problem**, which involves determining whether two finite graphs are isomorphic. Specifically, our task was to develop a Python program that can:

1. **Identify isomorphic graphs** from a given list of graphs.

2. **Compute automorphisms** of individual graphs, determining the number of symmetries within each graph.

### Key Features:
- **Basic Colour Refinement Algorithm**: Used to refine partitions of graph vertices based on vertex colours.

- **Fast Partition Refinement Algorithm**: An optimized algorithm for colour refinement based on Hopcroft's minimization algorithm for finite automata.

## Usage

1. Specify the directory with the input files containing graphs you wish to process in `branching.py` (the main program):
    ```python
    # line 93
    directory = r"absolute_path/to/directory"
    ```

2. To toggle between fast and basic colour refinement, comment/uncomment lines 15-16 in branching.py:
    ```python
    # lines 15-16
    # refined = basic_colorref(graphs, old_coloring)
    refined = fast_colorref(graphs, old_coloring)
    ```

3. File types:
    - A .gr file contains a single graph. The task is to compute the number of automorphisms for the graph (e.g., basicAUT***.gr).
    
    - A .grl file contains multiple graphs. The task is to find equivalence classes of isomorphic graphs. If the filename is basicGIAUT***.grl, it also computes the number of automorphisms for each graph.

## Project Components

- **`branching.py`**: The main script that implements the graph isomorphism algorithm.

- **`basic_colorref.py`**: The basic partition refinement algorithm, used for smaller graph instances or when precision is more critical than speed.

- **`fast_colorref.py`**: Contains the fast partition refinement algorithm based on Hopcroft's minimization algorithm for finite automata.

- **`graph.py`**: A custom module for working with directed and undirected multigraphs. Developed by **Paul Bonsma**, **Pieter Bos**, **Tariq Bontekoe**.

- **`graph_io.py`**: A module containing functions for reading and writing graphs. Developed by **Paul Bonsma**, **Pieter Bos**.

## Limitations and Known Issues

The basic colour refinement algorithm does not handle certain complex graphs, such as "basic07GIAut.grl", correctly. However, the fast partition refinement algorithm successfully solves all basic cases from the `basic` directory, making it our default approach for most instances.





