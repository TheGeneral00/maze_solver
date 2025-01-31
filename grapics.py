from tkinter import Tk, BOTH, Canvas
import tkinter as tk


class Window:
    def __init__(self, width, height):
        self.width = width
        self.heigth = height
        self.__root = tk.Tk()
        self.running = False

        #setting title for the __root widget
        self.__root.title('Maze Solver')
        
        #creating canvas for drawing graphics
        self.canvas = Canvas(self.__root, { 'bg': 'black', 'height': height, 'width': width})
        self.canvas.pack(fill= BOTH, expand=1)
        
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        
        

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color='white'):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color='white'):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win
        self._visited = False

    def draw(self, x1, y1, x2, y2):
        #initializing coordinates of the Cell
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2 

        #drawing the cell walls
        if self.has_left_wall == True:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, fill_color='black')
        
        if self.has_right_wall == True:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line) 
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, fill_color='black')
        
        if self.has_top_wall == True:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, fill_color='black')
        
        if self.has_bottom_wall == True:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, fill_color='black') 
    
    def draw_move(self, to_cell, undo=False):
        center1 = Point(self._x1 + (self._x2 - self._x1)/2, self._y1 + (self._y2-self._y1)/2)
        center2 = Point(to_cell._x1 + (to_cell._x2 - to_cell._x1)/2, to_cell._y1 + (to_cell._y2-to_cell._y1)/2)
        line = Line(center1, center2)
        if undo != False:
            self._win.draw_line(line, fill_color='gray')
        else:
            self._win.draw_line(line, fill_color='red')
