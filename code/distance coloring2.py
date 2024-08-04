import numpy as np
import matplotlib.pyplot as plt

# Initialize the grid size and create a mesh grid
grid_size = 100
x = np.arange(grid_size)
y = np.arange(grid_size)
xx, yy = np.meshgrid(x, y)

# Squares A and B (initialize them with top-left and bottom-right corners)
square_A = ((35, 40), (40, 50))
square_B = ((10, 25), (30, 20))

# Variables to track dragging
dragging_square = None
dragging_corner = None

# Function to calculate distance from a square
def distance_to_square(square, xx, yy):
    (x1, y1), (x2, y2) = square
    
    # Calculate distance from the edges of the square
    dx = np.maximum(np.maximum(x1 - xx, 0), xx - x2)
    dy = np.maximum(np.maximum(y1 - yy, 0), yy - y2)
    return np.sqrt(dx**2 + dy**2)

# Function to update the grid colors
def update_grid():
    if square_A == ((-1, -1), (-1, -1)) or square_B == ((-1, -1), (-1, -1)):
        return

    # Calculate distances to squares A and B
    dist_to_A = distance_to_square(square_A, xx, yy)
    dist_to_B = distance_to_square(square_B, xx, yy)

    # Determine grid color based on distance
    grid = np.where(dist_to_A < dist_to_B, 0, 1)

    # Display the grid
    plt.imshow(grid, cmap='bwr') # Use the blue-white-red colormap
    # Draw squares
    rect_A = plt.Rectangle(square_A[0], square_A[1][0] - square_A[0][0], square_A[1][1] - square_A[0][1], linewidth=1, edgecolor='red', facecolor='none')
    rect_B = plt.Rectangle(square_B[0], square_B[1][0] - square_B[0][0], square_B[1][1] - square_B[0][1], linewidth=1, edgecolor='blue', facecolor='none')
    plt.gca().add_patch(rect_A)
    plt.gca().add_patch(rect_B)
    plt.draw()

# Mouse click event handler
def on_click(event):
    global square_A, square_B, dragging_square, dragging_corner

    if event.inaxes:
        if event.button == 1:  # Left click
            # Check if clicking near any corner of the squares for resizing
            if is_near_corner(event, square_A):
                dragging_square = 'A'
                dragging_corner = get_near_corner(event, square_A)
            elif is_near_corner(event, square_B):
                dragging_square = 'B'
                dragging_corner = get_near_corner(event, square_B)
            else:
                # Start dragging the whole square
                dragging_square = 'A' if distance_to_square(square_A, event.xdata, event.ydata) < distance_to_square(square_B, event.xdata, event.ydata) else 'B'
                dragging_corner = None
        elif event.button == 3:  # Right click
            # Switch to setting the other square
            dragging_square = 'B' if dragging_square == 'A' else 'A'
            dragging_corner = None

def on_motion(event):
    global square_A, square_B, dragging_square, dragging_corner

    if dragging_square and event.inaxes:
        if dragging_square == 'A':
            if dragging_corner:
                square_A = resize_square(square_A, event.xdata, event.ydata, dragging_corner)
            else:
                square_A = move_square(square_A, event.xdata, event.ydata)
        elif dragging_square == 'B':
            if dragging_corner:
                square_B = resize_square(square_B, event.xdata, event.ydata, dragging_corner)
            else:
                square_B = move_square(square_B, event.xdata, event.ydata)
        update_grid()

def on_release(event):
    global dragging_square, dragging_corner
    dragging_square = None
    dragging_corner = None

def is_near_corner(event, square):
    corners = [square[0], (square[0][0], square[1][1]), (square[1][0], square[0][1]), square[1]]
    return any(np.hypot(event.xdata - cx, event.ydata - cy) < 3 for cx, cy in corners)

def get_near_corner(event, square):
    corners = [square[0], (square[0][0], square[1][1]), (square[1][0], square[0][1]), square[1]]
    for corner in corners:
        if np.hypot(event.xdata - corner[0], event.ydata - corner[1]) < 3:
            return corner
    return None

def resize_square(square, x, y, corner):
    (x1, y1), (x2, y2) = square
    if corner == square[0]:
        x1, y1 = x, y
    elif corner == (x1, y2):
        x1, y2 = x, y
    elif corner == (x2, y1):
        x2, y1 = x, y
    elif corner == square[1]:
        x2, y2 = x, y
    return ((min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2)))

def move_square(square, x, y):
    (x1, y1), (x2, y2) = square
    width, height = x2 - x1, y2 - y1
    return ((x - width // 2, y - height // 2), (x + width // 2, y + height // 2))

# Set up the plot
fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)
plt.xlim(0, grid_size-1)
plt.ylim(0, grid_size-1)
plt.gca().invert_yaxis()

update_grid()
plt.show()
