import tkinter as tk
from PIL import Image, ImageTk
from classes import *
import ttkbootstrap as ttk


#GUI
root = tk.Tk()
root.title("ADMU Evacuation Route Planner")

# App Icon
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)

root.configure(bg="#f5f5f5")

# Global Font
DEFAULT_FONT = ("Segoe UI", 10)

style = ttk.Style()
style.configure("TFrame", background="#ffffff")
style.configure("TLabel", background="#ffffff", font=DEFAULT_FONT)
style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), background="#ffffff")
style.configure("Sidebar.TFrame", background="#fafafa")
style.configure("TButton", font=("Segoe UI", 10), padding=6)


# Top Navigation Bar
navbar = tk.Frame(root, bg="white", height=50)
navbar.grid(row=0, column=0, columnspan=2, sticky="nsew")

tk.Label(
    navbar, 
    text="ADMU Evacuation Route Planner",
    bg="white",
    fg="#333333",
    font=("Segoe UI Semibold", 14)
).pack(side="left", padx=20)

ttk.Separator(root, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew")


# Sidebar (Instructions + Results)
sidebar = ttk.Frame(root, style="Sidebar.TFrame", padding=15)
sidebar.grid(row=2, column=0, sticky="nsw", padx=10, pady=10)

# --- Instructions Header ---
ttk.Label(
    sidebar,
    text="Instructions",
    style="Header.TLabel"
).grid(row=0, column=0, sticky="w")

ttk.Label(
    sidebar,
    text="Click a RED node to select a starting location.\n"
         "Path to nearest EAA will be shown.",
    wraplength=250
).grid(row=1, column=0, pady=(5, 10), sticky="w")

# --- Results Box ---
result_label = ttk.Label(
    sidebar,
    text="Awaiting selection…",
    padding=10,
    background="#eef2ff",
    anchor="w",
    justify="left"
)
result_label.grid(row=2, column=0, sticky="ew", pady=(0, 15))


# Directions Panel
directions_frame = ttk.Labelframe(
    sidebar,
    text="Directions"
)
directions_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))

# Make directions frame expandable
sidebar.grid_rowconfigure(3, weight=1)

# Directions Textbox
directions_text = tk.Text(
    directions_frame,
    width=32,
    height=5,
    wrap="word",
    font=("Segoe UI", 9),
    state="disabled"
)
directions_text.grid(row=0, column=0, sticky="nsew")

# Allow directions frame to res
directions_frame.grid_rowconfigure(0, weight=1)
directions_frame.grid_columnconfigure(0, weight=1)


# Map Canvas
canvas_frame = tk.Frame(root, bg="white")
canvas_frame.grid(row=2, column=1, padx=10, pady=10)

campus_map = Image.open("Ateneo College Map.png").resize((800, 600))
current_scale = 1.0
campus_map_tk = ImageTk.PhotoImage(campus_map)

map_canvas = tk.Canvas(canvas_frame, width=800, height=600, bg="white", highlightthickness=0)
map_canvas.pack()


# Legend (Right Side)
legend_frame = ttk.Frame(root, padding="10", relief="groove")
legend_frame.grid(row=2, column=2, padx=10, pady=10, sticky="n")

ttk.Label(legend_frame, text="Node Legend", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0,5))
ttk.Separator(legend_frame).grid(row=1, column=0, columnspan=2, sticky="ew")

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


# --- Helper: lookup edge weight quickly ---
_edge_weight_map = { (u, v): w for u, v, w in EDGE_LIST }
# Make symmetric entries too
_edge_weight_map.update({ (v, u): w for (u, v), w in list(_edge_weight_map.items()) })

def edge_weight(u: str, v: str) -> float:
    """Return weight for edge (u,v). Returns 0 if edge not found (shouldn't happen)."""
    return float(_edge_weight_map.get((u, v), 0.0))

def path_to_steps(path: list[str]) -> tuple[list[tuple[str,str,float]], float]:
    """
    Convert path list -> list of (from, to, weight) and total cost.
    Returns: (steps, total_cost)
    """
    steps = []
    total = 0.0
    if not path or len(path) < 2:
        return steps, total

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        w = edge_weight(u, v)
        steps.append((u, v, w))
        total += w
    return steps, total



# --- Drawing Functions ---

def draw_nodes_and_edges():
    """Draws the entire graph on the canvas."""
    map_canvas.delete("all") # Clear previous drawings

    #Background
    map_canvas.create_image(0, 0, image=campus_map_tk, anchor="nw", tags = "bg")

    map_canvas.tag_lower("bg")
    
    # 1. Draw Edges
    for u, v, _ in EDGE_LIST:
        x1, y1 = NODE_POSITIONS[u]
        x2, y2 = NODE_POSITIONS[v]
        map_canvas.create_line(x1, y1, x2, y2, fill="blue", width=1)

    # 2. Draw Nodes
    for key, (x, y) in NODE_POSITIONS.items():
        color = EAA_NODE_COLOR if key in EAA_NODES else DEFAULT_NODE_COLOR
        
        # Draw the circle
        map_canvas.create_oval(
            x - NODE_RADIUS, y - NODE_RADIUS, 
            x + NODE_RADIUS, y + NODE_RADIUS, 
            fill=color, tags=(key, "node")
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
        # Compute shortest route to each EAA
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

# Click Handler
def handle_canvas_click(event):

    global selected_start_node
    
    clicked_items = map_canvas.find_closest(event.x, event.y)
    
    if clicked_items:
        item_tags = map_canvas.gettags(clicked_items[0])
        
        for tag in item_tags:
            if tag in NODE_POSITIONS:
                
                selected_start_node = tag
                
                path, cost, eaa = find_nearest_eaa(selected_start_node)

    if not path:
        return

    result_label.config(
        text=(f"Start: {selected_start_node}\n"
              f"Nearest area: {eaa}\n"
              f"Total Cost: {cost:.2f}")
    )

    steps, total_cost = path_to_steps(path)

    buf_lines = []
    for idx, (u, v, w) in enumerate(steps, start=1):
        buf_lines.append(f"{idx}) {u} → {v}    ({w:.2f})")

    buf_lines.append("")
    buf_lines.append(f"Total: {total_cost:.2f}")

    directions_text.config(state="normal")
    directions_text.delete("1.0", "end")
    directions_text.insert("1.0", "\n".join(buf_lines))
    directions_text.config(state="disabled")

    draw_path(path)


def on_hover_enter(event):
    map_canvas.itemconfig("hover", outline="yellow", width=3)

def on_hover_leave(event):
    map_canvas.itemconfig("hover", outline="#333", width=1)

map_canvas.bind("<Button-1>", handle_canvas_click)

# Right-click for debugging
map_canvas.bind("<Button-3>", lambda e: print("Coords:", e.x, e.y))

draw_nodes_and_edges()
root.mainloop()
