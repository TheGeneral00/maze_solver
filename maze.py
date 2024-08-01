from grapics import *
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_colls = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def print_cell_properties(self, i, j):
        cell = self._cells[i][j]
        print(f"Properties for Cell({i}, {j}):")
        for key, value in cell.__dict__.items():
            print(f"{key}: {value}")
    
    #populating the self._cells list and drawing the cells on canvas
    def _create_cells(self):
        for i in range(self._num_colls):
            temp = []
            for j in range(self._num_rows):
                temp.append(Cell(self._win))
            self._cells.append(temp)
        for i in range(self._num_colls):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    #helper function to draw each cell
    def _draw_cell(self, i ,j):
        if self._win == None:
            return
        x1 = self._x1 + i*self._cell_size_x
        x2 = self._x1 + (i+1)*self._cell_size_x
        y1 = self._y1 + j*self._cell_size_y
        y2 = self._y1 + (j+1)*self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    # helper function for animation
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)
    
    #setting predefined entrance and exit visualy
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_colls-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_colls-1, self._num_rows-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            temp = []
            #checking for possible directions to move
            #left 
            if i>0 and self._cells[i-1][j]._visited == False:
                temp.append((i-1, j))
            if i<self._num_colls-1 and self._cells[i+1][j]._visited == False:
                temp.append((i+1, j))
            if j>0 and self._cells[i][j-1]._visited == False:
                temp.append((i, j-1))   
            if j<self._num_rows-1 and self._cells[i][j+1]._visited == False:
                temp.append((i, j+1))

            #checking if move into a direction is possible
            if len(temp) == 0:
                self._draw_cell(i, j)
                return

            #selecting direction to go
            direction_index = random.randrange(len(temp))
            next_index = temp[direction_index]
            #breaking connecting walls 
            if next_index[0] == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
            if next_index[0] == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            if next_index[1] == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            if next_index[1] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False
            #recursiv call
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell._visited = False

    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j]._visited = True
        #checking if exit reached
        if i == self._num_colls-1 and j == self._num_rows-1:
            return True
        #checking for possible directions and solving for the cell in that direction
        if i>0 and not self._cells[i-1][j]._visited and not self._cells[i][j].has_left_wall :
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True             
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)

        if i<self._num_colls-1 and not self._cells[i+1][j]._visited and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
            
        if j<self._num_rows-1 and not self._cells[i][j+1]._visited and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
            
        if j>0 and not self._cells[i][j-1]._visited and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
            
        #return False if no direction worked out
        return False
