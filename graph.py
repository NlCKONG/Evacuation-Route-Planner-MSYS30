from classes import *

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


#GUI
root = tk.Tk()
root.title("ADMU Evacuation Route Planner")

campus_map = Image.open("Ateneo College Map.png")
campus_map = campus_map.resize((800, 600))
campus_map_tk = ImageTk.PhotoImage(campus_map)

input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

ttk.Label(
    input_frame,
    text="Click a RED node to select your starting location and find the shortest evacuation route.",
    font=('Arial', 10, 'bold')
).grid(row=0, column=0, padx=5, pady=5)

result_label = ttk.Label(input_frame, text="Awaiting selection...", padding="10")
result_label.grid(row=1, column=0, sticky=(tk.W, tk.E))

map_canvas = tk.Canvas(root, width=800, height=600, bg="white")
map_canvas.grid(row=2, column=0, padx=10, pady=10)

# --- NEW LEGEND FRAME (Positioned right of the map) ---
legend_frame = ttk.Frame(root, padding="10", relief="groove")
legend_frame.grid(row=2, column=1, padx=10, pady=10, sticky="n")

# --- Legend Title ---
ttk.Label(legend_frame, text="Node Label Legend", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 5))
ttk.Separator(legend_frame, orient='horizontal').grid(row=1, column=0, columnspan=2, sticky="ew")

# --- Node Mapping Entries ---
legend_row = 2

for key, name in NODE_KEY_MAPPING:
    # Column 0: Node Key (Bold)
    ttk.Label(
        legend_frame, 
        text=key, 
        font=('Arial', 8, 'bold')
    ).grid(row=legend_row, column=0, padx=5, pady=1, sticky="w")
    
    # Column 1: Building Name
    ttk.Label(
        legend_frame, 
        text=name,
        font=('Arial', 8)
    ).grid(row=legend_row, column=1, padx=5, pady=1, sticky="w")
    
    legend_row += 1

# --- Drawing Functions ---

def draw_nodes_and_edges():
    """Draws the entire graph on the canvas."""
    map_canvas.delete("all") # Clear previous drawings

    #Background
    map_canvas.create_image(0, 0, image=campus_map_tk, anchor="nw", tags = "bg")

    map_canvas.tag_lower("bg")
    
    # 1. Draw Edges (Simple straight lines between coordinates)
    for u, v, _ in EDGE_LIST:
        x1, y1 = NODE_POSITIONS[u]
        x2, y2 = NODE_POSITIONS[v]
        map_canvas.create_line(x1, y1, x2, y2, fill="blue", width=1)

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
        map_canvas.create_text(
            x + NODE_RADIUS + 5, 
            y, 
            text=key, 
            tags=(key, "label"),
            fill=LABEL_COLOR,
            font=LABEL_FONT,
            anchor="w")

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
    draw_nodes_and_edges()
    
    if len(path) < 2:
        return

    # Draw line segments for the path
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        x1, y1 = NODE_POSITIONS[u]
        x2, y2 = NODE_POSITIONS[v]
        map_canvas.create_line(x1, y1, x2, y2, fill=PATH_COLOR, width=PATH_WIDTH, tags="path_line")

    # Highlight the end node (EAA)
    end_key = path[-1]
    x, y = NODE_POSITIONS[end_key]
    map_canvas.create_oval(
        x - NODE_RADIUS - 2, y - NODE_RADIUS - 2, 
        x + NODE_RADIUS + 2, y + NODE_RADIUS + 2, 
        outline="orange", width=4, tags=("path_line", end_key)
    )

    # Ensure nodes and labels are on top of highlighted path
    map_canvas.tag_raise("node")
    map_canvas.tag_raise("label")

    # Highlight the start node
    start_key = path[0]
    x, y = NODE_POSITIONS[start_key]
    map_canvas.create_oval(
        x - NODE_RADIUS, y - NODE_RADIUS, 
        x + NODE_RADIUS, y + NODE_RADIUS, 
        fill=START_NODE_COLOR, outline="orange", width=2, tags=("path_line", start_key)
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
            
    print("LEFT CLICK:", event.x, event.y)


#Clicks
map_canvas.bind("<Button-1>", handle_canvas_click)

def print_coords(event):
    print("Right click at:", event.x, event.y)

map_canvas.bind("<Button-3>", print_coords)


# Initial drawing of the graph
draw_nodes_and_edges()



root.mainloop()