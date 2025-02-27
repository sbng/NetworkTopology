# NetworkTopology
Scripts to automate network topology diagram creation

# Motivation
1. Manual creation of network topology is tedious and error prone
2. Changes and updates are not timely and subjected to mistakes
3. May not reflect the true status of the network

# Approaches
1. Automte netwotk diagram creatiobn for presentation and documention
2. Collect network information and statistics (via show commands)
3. Fundamental concept:
    - Graph (directed or undirected)
    - Nodes (devices)
    - Edges (links between devices)

Example of adirected graph:
Nodes: A, B, C, D
Edges: A->B A->C B->D C->D 
```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```
# Challenges
1. Data collected from devices are unstructured
2. Clean up and structure the data using script [Python TTP](https://ttp.readthedocs.io/en/latest/)
3. Use the structured data to create Nodes and Edges
4. Many network diagram framework are used to create presentable diagram or html
    - D3.js
    - Graphviz
    - N2G
  
