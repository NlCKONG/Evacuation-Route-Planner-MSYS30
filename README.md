# Evacuation Route Planner for the ADMU College Campus
The evacuation route planner is a simple Python application for the Ateneo College Campus, using the Tkinter package.
## Description
<strong>Purpose</strong>
<br>This project finds the optimal route from any building to one of three evacuation areas in the campus. Since the campus is located near the West Valley Fault, this project aimed to provide a quick solution for
students who need to find the fastest way to get to one of the evacuation areas. 
<br>Currently, this project does not accurately depict the campus map, the distances between nodes, and is not easily accessible to students. Further improvements have been identified, but development has been paused for the meantime.
<br><strong>Features</strong>
<br>The project makes use of three classes—Vertex, Edge, and Graph—which are used to construct the map. The Graph class holds the adjacency list, which is a dictionary where every key is a building code, and 
its corresponding value is a list of tuples representing its direct neighbors and distances to them. This will be looped through by Dijkstra's algorithm to find its neighbors, and ultimately the shortest path. It also stores a list of every Edge 
object created from the input data. This is essential when making the GUI using Tkinter when the edges need to be drawn in the program.
<br>Dijkstra's algorithm was chosen for the optimal route finder. While other algorithms could have been used like Prim's, Dijkstra's algorithm is the best choice because in case a pathway is blocked, it would find 
the next shortest route.
<br>The project uses the built-in Tkinter package to create a simple GUI. The constructed graph with the values of the building names, edge values, etc. is used as a reference for the interactive map in the program.
In the middle, the interactive graph consists of nodes, where the evacuation areas are colored yellow, while the buildings and other common areas on the college campus is colored red. Edges connect these nodes, which hold the path value indicating the distance between them. The left sidebar consists of the instructions, a summarized text version of the optimal path,
as well as the step-by-step path the user must take from the starting point to end. The right sidebar holds the node legend, translating the node names to their respective building names.
## Usage
Simply click on one of the red nodes to select as your starting point. Once clicked, the node becomes green, and the path towards the nearest evacuation area (EAA) will be highlighted in orange. 
<br>Selecting node C (Schmitt Hall)
<img width="1625" height="808" alt="image" src="https://github.com/user-attachments/assets/5e08cbcd-35c3-49a7-b83b-07a80b031cfc" />
<br>Selecting node SEC-A
<img width="1630" height="814" alt="image" src="https://github.com/user-attachments/assets/449519b3-56e7-475a-be6e-70dcc9423840" />
