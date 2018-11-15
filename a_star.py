import time

class A_Star:
    def __init__(self):
        self.grid = [
            [1,1,1,1,1,255,1,1,1,1],
            [1,1,1,1,1,255,1,1,1,1],
            [1,1,1,1,1,255,1,1,1,1],
            [1,1,1,1,1,1,255,1,1,1],
            [1,1,1,1,1,1,1,255,1,255],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
        ]
        self.open_set = {} #cell (row, col) : cost
        self.closed_set = {} # cell (row:col) : parent (row, col)
        self.start = (9,0)
        self.goal = (0,9)
        self.wall_value = 255
        self.path = []
        self.alpha = 1
        self.beta = 1
        self.h_type = "manhattan"

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
                            self.open_set[(curr_cell[0]+di, curr_cell[1]+dj)] = self.alpha*self.grid[curr_cell[0]+di][curr_cell[1]+dj]+self.beta*self.heuristic((curr_cell[0]+di, curr_cell[1]+dj))

    def traverse(self, curr_cell):
        if not self.open_set:   #no path found
            return

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

        if curr_cell == self.goal:
            print ("Goal found!")
        else:
            print ("No path from start to goal")

        while curr_cell is not self.start:
            self.path.append(self.closed_set[curr_cell])
            curr_cell = self.closed_set[curr_cell]
        self.path.reverse()
        
        self.draw_path()

    def draw_path(self):

        #Print path
        print("Path:")
        for p in self.path:
            print("-->{}".format(p), end="")
        print("\n\n")

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
        

if __name__ == '__main__':
    astar = A_Star()
    astar.find_path()