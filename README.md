# Evacuation Route Planner for the ADMU College Campus
The evacuation route planner is a simple Python application for the Ateneo College Campus, using the Tkinter package.
## Description
<strong>Purpose</strong>
<br>This project finds the optimal route from any building to one of three evacuation areas in the campus. Since the campus is located near the West Valley Fault, this project aimed to provide a quick solution for
students who need to find the fastest way to get to one of the evacuation areas. Currently, this project does not accurately depict the campus map, the distances between nodes, and is not easily accessible to 
students. 
<br><strong>Features</strong>
<br>The project makes use of three classes——Vertex, Edge, and Graph——which are used to construct the map. The Graph class holds the adjacency list, which is a dictionary where every key is a building code, and 
its corresponding value is a list of tuples representing its direct neighbors and distances to them. This will be looped through by Dijkstra's algorithm to find its neighbors. It also stores a list of every Edge 
object created from the input data. This is essential when making the GUI using Tkinter when the edges need to be drawn in the program.
<br>Dijkstra's algorithm was chosen for the optimal route finder. While other algorithms could have been used like Prim's, Dijkstra's algorithm is the best choice because in case a pathway is blocked, it would find 
the next shortest route.
<br>The project uses the built-in Tkinter package to create a simple GUI. The constructed graph with the values of the building names, edge values, etc. is used as a reference for the interactive map in the program.
The evacuation areas are colored yellow, while the buildings and other common areas on the college campus is colored red.
## Usage
