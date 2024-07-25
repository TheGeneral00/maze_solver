from tkinter import Tk, BOTH, Canvas
import tkinter as tk


class window:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.__root = tk.Tk()
        
        #setting title for the __root widget
        self.__root.title('Maze Solver')
        
        #creating canvas for drawing graphics
        self.canvas = Canvas(self.__root, { 'bg': 'black',  })
        self.canvas.pack()
        
        #creating value to track the state of the window
        self.running = False
        
        self.__root.protocol('WM_DELETE_WINDOW', self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.runnig = True
        while self.running == True:
            self.redraw()

    def close(self):
        self.runnig = False
