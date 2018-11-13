class A_Star:
    def __init__(self):
        self.grid = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
        ]
        self.open_set = {}
        self.closed_set = {}
        self.start = (0,0)
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
        curr_cell = min(self.open_set, key=self.open_set.get)
        self.closed_set[curr_cell] = self.open_set[curr_cell]
        del self.open_set[curr_cell]
        self.path.append(curr_cell)
        print ("traverse!\n")
        return curr_cell

    def find_path(self):
        curr_cell = self.start
        self.closed_set[self.start] = 0
        print (self.start)

        while curr_cell is not self.goal:   
            self.check_neighbours(curr_cell)
            curr_cell = self.traverse(curr_cell)

        [print(p) for p in self.path]

if __name__ == '__main__':
    astar = A_Star()
    astar.find_path()