import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Default number of rows and columns
rows, cols = 10, 10

# Function to generate the maze
# "maze" is a 3-D list that contains information about a cell position and its 4 walls [top(0), bottom(1), left(2), right(3)]
# "visited" is a 2-D list that keep track of the cells visited, cell positions are appended once these are visited
# "current_cell" keeps track of the cell currently under operation
def create_maze(maze, visited, current_cell):
    cell_stack = [current_cell]
    while cell_stack:
        x, y = cell_stack[-1] # access the topmost cell in the stack
        visited[x, y] = True
        # "neighbors" list to list all the unvisited neighbours of the current_cell
        neighbors = [] # Declared and initialized as empty list
        # Find valid unvisited neighbors, considering top left corner as origin, and x-coordinate increases on moving downwards and y-coordinate increases on moving rightwards
        if x > 0 and not visited[x - 1, y]:  # Up
            neighbors.append((x - 1, y))
        if x < rows - 1 and not visited[x + 1, y]:  # Down
            neighbors.append((x + 1, y))
        if y > 0 and not visited[x, y - 1]:  # Left
            neighbors.append((x, y - 1))
        if y < cols - 1 and not visited[x, y + 1]:  # Right
            neighbors.append((x, y + 1))
        
        if neighbors:
            next_cell = neighbors[np.random.randint(0, len(neighbors))]
            # Remove walls between the current cell and the next cell
            # next_cell[0]= x-coordinate, next_cell[1]= y-coordinate
            if next_cell[0] == x + 1:  # Moved down
                maze[x, y, 1] = 0  # Remove bottom wall of current cell
                maze[next_cell[0], next_cell[1], 0] = 0  # Remove top wall of next cell
            if next_cell[0] == x - 1:  # Moved up
                maze[x, y, 0] = 0  # Remove top wall of current cell
                maze[next_cell[0], next_cell[1], 1] = 0  # Remove bottom wall of next cell
            if next_cell[1] == y + 1:  # Moved right
                maze[x, y, 3] = 0  # Remove right wall of current cell
                maze[next_cell[0], next_cell[1], 2] = 0  # Remove left wall of next cell
            if next_cell[1] == y - 1:  # Moved left
                maze[x, y, 2] = 0  # Remove left wall of current cell
                maze[next_cell[0], next_cell[1], 3] = 0  # Remove right wall of next cell
            cell_stack.append(next_cell) # Append the next_cell to cell_stack for backtracking
        else:
            cell_stack.pop() # Cell does not have valid unvisited neighbours

# Function to draw the maze
# mplot is the subplot on the figure where the maze is to be created
# maze is the data about the created maze that is to be drawn
# start is the coordinate of fixed starting point
# end is the coordinate of the randomly chosen ending point
def draw_maze(mplot, maze, start, end):
    mplot.clear() # Clears all plots drawn in the subploat
    mplot.set_aspect('equal') # Ensures that both x and y axes have same scale
    mplot.set_title('MAZE GENERATOR (Use up/down arrow keys to change size of maze)\nGreen -> Start, Red -> End',color='white', fontsize=15)
    # Create the outer boundary
    for i in range(rows):
        for j in range(cols):
            x, y = j, rows - 1 - i #Origin is adjusted to top-left corner
            # Draw walls if they exist (1 = wall exists, 0 = no wall)
            if maze[i, j, 0] == 1:  # Up wall
                mplot.plot([x, x + 1], [y + 1, y + 1], color='#94c0f7',linewidth=2)
            if maze[i, j, 1] == 1:  # Down wall
                mplot.plot([x, x + 1], [y, y], color='#94c0f7',linewidth=2)
            if maze[i, j, 2] == 1:  # Left wall
                mplot.plot([x, x], [y, y + 1], color='#94c0f7',linewidth=2)
            if maze[i, j, 3] == 1:  # Right wall
                mplot.plot([x + 1, x + 1], [y, y + 1], color='#94c0f7',linewidth=2)
    mplot.add_patch(patches.Rectangle((start[1], rows - 1 - start[0]), 1, 1, color='green'))
    mplot.add_patch(patches.Rectangle((end[1], rows - 1 - end[0]), 1, 1, color='red'))
    mplot.set_xlim(0, cols)
    mplot.set_ylim(0, rows)
    mplot.axis('off')

# Key event handler to modify rows and cols
def on_key(event):
    global rows, cols # To access and modify the global variables 'rows' and 'cols'
    if event.key == 'up':
        rows = rows + 1
        cols = cols + 1
    elif event.key == 'down' and rows > 2 and cols > 2:
        rows = rows - 1
        cols = cols - 1
    update_maze()

# Update the maze and redraw it
def update_maze():
    fig.clear()
    maze = np.ones((rows, cols, 4), dtype=int)  # 4 directions (walls) for each cell, initially 1 for all walls to exist
    visited = np.zeros((rows, cols), dtype=bool) # Initially 0 (False) to indicate all cells are unvisited
    create_maze(maze, visited, (0, 0))  # Start from the top-left corner
    start = (0, 0) # Fixed starting position
    end = (np.random.randint(0, rows - 1), np.random.randint(0, cols - 1)) # Randomly chosen ending position
    mplot = fig.add_subplot(111) # adds a subplot in the figure with 1 row and 1 column
    draw_maze(mplot, maze, start, end)
    plt.draw()

# Set up the plot and figure
fig = plt.figure(figsize=(8, 8), facecolor='#002366')  # Creating a 8 inches by 8 inches figure
fig.canvas.mpl_connect('key_press_event', on_key) # Connects the different functions to user interaction event that modifies the canvas of the figure
update_maze()

plt.show()

