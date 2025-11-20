from classes import *

import tkinter as tk
from tkinter import ttk
# Ensure all your graph classes/functions are included here

# --- Drawing Functions ---

def draw_nodes_and_edges():
    """Draws the entire graph on the canvas."""
    map_canvas.delete("all") # Clear previous drawings

    # 1. Draw Edges (Simple straight lines between coordinates)
    for u, v, _ in EDGE_LIST:
        x1, y1 = NODE_POSITIONS[u]
        x2, y2 = NODE_POSITIONS[v]
        map_canvas.create_line(x1, y1, x2, y2, fill="gray", width=1)

    # 2. Draw Nodes
    for key, (x, y) in NODE_POSITIONS.items():
        color = EAA_NODE_COLOR if key in EAA_NODES else DEFAULT_NODE_COLOR
        
        # Draw the circle (oval is used for circles in Tkinter)
        map_canvas.create_oval(
            x - NODE_RADIUS, y - NODE_RADIUS, 
            x + NODE_RADIUS, y + NODE_RADIUS, 
            fill=color, tags=(key, "node") # Assign the node key as a tag
        )
        
        # Add the label
        map_canvas.create_text(x + NODE_RADIUS + 5, y, text=key, tags=(key, "label"))

# --- Pathfinding and Display Logic ---

def find_nearest_eaa(start_node: str):
    """Runs Dijkstra's to find the shortest path to the nearest EAA."""
    shortest_path = []
    min_cost = float('inf')
    best_eaa = "N/A"

    for end_node in EAA_NODES:
        # Use the core logic from section 1
        path, cost = dijkstra(CAMPUS_GRAPH, start_node, end_node) 
        
        if cost < min_cost:
            min_cost = cost
            shortest_path = path
            best_eaa = end_node
            
    return shortest_path, min_cost, best_eaa

def draw_path(path: list[str]):
    """Highlights the calculated shortest path."""
    map_canvas.delete("path_line") # Clear old path lines
    
    if len(path) < 2:
        return

    # Draw line segments for the path
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        x1, y1 = NODE_POSITIONS[u]
        x2, y2 = NODE_POSITIONS[v]
        map_canvas.create_line(x1, y1, x2, y2, fill=PATH_COLOR, width=PATH_WIDTH, tags="path_line")
        
    # Re-draw all nodes on top of the path to keep them visible
    draw_nodes_and_edges()
    
    # Highlight the start node
    start_key = path[0]
    x, y = NODE_POSITIONS[start_key]
    map_canvas.create_oval(
        x - NODE_RADIUS, y - NODE_RADIUS, 
        x + NODE_RADIUS, y + NODE_RADIUS, 
        fill=START_NODE_COLOR, outline="black", width=2, tags=("path_line", start_key)
    )

    # Highlight the end node (EAA)
    end_key = path[-1]
    x, y = NODE_POSITIONS[end_key]
    map_canvas.create_oval(
        x - NODE_RADIUS - 2, y - NODE_RADIUS - 2, 
        x + NODE_RADIUS + 2, y + NODE_RADIUS + 2, 
        outline="black", width=4, tags=("path_line", end_key)
    )

def handle_canvas_click(event):
    """
    Called when the user clicks the canvas.
    Determines if a node was clicked and calculates the path.
    """
    global selected_start_node
    
    # Use find_closest to see what is near the click point (x, y)
    clicked_items = map_canvas.find_closest(event.x, event.y)
    
    if clicked_items:
        # Get the tags of the closest item
        item_tags = map_canvas.gettags(clicked_items[0])
        
        # Check if one of the tags is a node key (e.g., 'M', 'O', 'XV')
        for tag in item_tags:
            if tag in NODE_POSITIONS:
                
                # We found the starting node!
                selected_start_node = tag
                
                # 1. Calculate Path
                path, cost, eaa = find_nearest_eaa(selected_start_node)
                
                # 2. Display Results
                if path:
                    path_text = " -> ".join(path)
                    result_label.config(text=f"Start: {selected_start_node}\nNearest EAA: {eaa}\nShortest Path: {path_text}\nTotal Cost: {cost:.2f}")
                    draw_path(path) # 3. Draw Path on Canvas
                else:
                    result_label.config(text=f"Error: Path not found from {selected_start_node}.")
                    map_canvas.delete("path_line") # Clear path
                
                return # Stop after finding the node

# --- GUI Setup ---
root = tk.Tk()
root.title("ADMU Evacuation Route Planner")

# Frame for Inputs and Results
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(input_frame, text="Click a RED node to select your starting location and find the shortest evacuation route.", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

result_label = ttk.Label(input_frame, text="Awaiting selection...", padding="10")
result_label.grid(row=1, column=0, sticky=(tk.W, tk.E))

# Map Canvas
map_canvas = tk.Canvas(root, width=800, height=600, bg="white")
map_canvas.grid(row=2, column=0, padx=10, pady=10)

# Bind the left mouse button click event to the handler function
map_canvas.bind('<Button-1>', handle_canvas_click)

# Initial drawing of the graph
draw_nodes_and_edges()

root.mainloop()