import time
from graphics import *
from math import sqrt

class A_Star:
    def __init__(self):
        self.grid = [
            [1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,255,255,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,255,255,255,255,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,255,1,1,1,1,255,255,255,255,255,255,255,255],
            [1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,255,255,255,255,255,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        self.open_set = {} #cell (row, col) : cost
        self.closed_set = {} # cell (row:col) : parent (row, col)
        self.start = (19,0)
        self.goal = (0,19)
        self.wall_value = 255
        self.path = []
        self.parent_dict = {}
        self.alpha = 1.6
        self.beta = 1
        self.h_type = "eucl"

    def heuristic (self, cell):
        if self.h_type == "manhattan":
            return abs(cell[0]-self.goal[0]) + abs(cell[1]-self.goal[1])
        else:   #use eucledian distance
            return sqrt((cell[0]-self.goal[0])**2 + (cell[1]-self.goal[1])**2)

    def check_neighbours(self, curr_cell):

            for di in [-1,0,1]:
                for dj in [-1,0,1]:
                    if ((curr_cell[0]+di, curr_cell[1]+dj) not in self.open_set
                        and (curr_cell[0]+di, curr_cell[1]+dj) not in self.closed_set
                        and curr_cell[0]+di in range (0, len(self.grid))
                        and curr_cell[1]+dj in range (0, len(self.grid[0]))
                        and self.grid[curr_cell[0]+di][curr_cell[1]+dj] != self.wall_value):
                            cost = self.alpha*self.grid[curr_cell[0]+di][curr_cell[1]+dj] * sqrt(di**2 + dj**2)
                            heur = self.beta*self.heuristic((curr_cell[0]+di, curr_cell[1]+dj))
                            #print ("Cost: {}, Heur:{}".format(cost,heur))
                            self.open_set[(curr_cell[0]+di, curr_cell[1]+dj)] = cost + heur
                            self.parent_dict[(curr_cell[0]+di, curr_cell[1]+dj)] = curr_cell
                            

    def traverse(self, curr_cell):
        next_cell = min(self.open_set, key=self.open_set.get)
        self.closed_set[next_cell] = curr_cell
        del self.open_set[next_cell]
        return next_cell

    def find_path(self):
        curr_cell = self.start
        self.closed_set[self.start] = self.start

        while curr_cell != self.goal:   
            self.check_neighbours(curr_cell)
            curr_cell = self.traverse(curr_cell)
            if not self.open_set:
                break

        if curr_cell == self.goal:
            print ("Goal found!")
        else:
            print ("No path from start to goal")

        while curr_cell is not self.start:
            #self.path.append(self.closed_set[curr_cell])
            self.path.append(self.parent_dict[curr_cell])
            curr_cell = self.parent_dict[curr_cell]
        self.path.reverse()

        self.draw_path()
        time.sleep(2)

    def draw_path(self):

        #Print path
        print("Path:", end="")
        for p in self.path:
            print("{}-->".format(p), end="")
        print("{}\n\n".format(self.goal))

        #Draw path
        padding =  len(str(len(self.path)))+2
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if (row, col) in self.path:
                    print ("{}".format(self.path.index((row, col))).center(padding), end="")
                elif self.grid[row][col] == 1:
                    print("o".center(padding), end="")
                else:
                    print("X".center(padding), end="")
            print ("")

class Visualizer:
    def __init__(self, grid):
        self.window_width = 500
        self.window_height = 500
        self.grid = grid

        self.win = GraphWin('Map', self.window_width, self.window_height)
        self.win.setCoords(20.0, 20.0, 20.0, 0.0)
        self.win.setBackground("gray")

    def draw_fancy_path(self):
        # draw grid
        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                self.win.plotPixel(x*self.window_width/len(self.grid[0]), y*self.window_height/len(self.grid), "white")
        self.draw_square((2,3),"green")
        self.win.getMouse()
        self.win.close()

    def draw_square(self, cell, colour):
        cell_width = self.window_width/len(self.grid[0])
        print (cell_width)
        square = Rectangle(Point(cell[1]*cell_width-cell_width/2.0, cell[0]*cell_width-cell_width/2.0),
                           Point(cell[1]*cell_width+cell_width/2.0, cell[0]*cell_width+cell_width/2.0))
        square.draw(self.win)
        square.setFill(colour)

        self.win.getMouse()
        self.win.close()

 
if __name__ == '__main__':
    astar = A_Star()
    astar.find_path()