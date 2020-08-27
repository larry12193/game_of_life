import cv2
import time
import numpy as np

class GameOfLife:

    # Define alive/dead pixel values
    alive = 0
    dead = 255

    # Define common objects to spawn
    glider = np.uint8([[alive,  dead,   dead],  #  1 0 0
                       [dead,   alive,  alive], #  0 1 1
                       [alive,  alive,  dead]]) #  1 1 0

    blinker = np.uint8([[alive, alive, alive]]) # 1 1 1

    toad = np.uint8([[dead,  alive, alive, alive], # 0 1 1 1
                     [alive, alive, alive, dead]]) # 1 1 1 0

    beacon = np.uint8([[alive,alive,dead,dead],  # 1 1 0 0
                       [alive,alive,dead,dead],  # 1 1 0 0
                       [dead,dead,alive,alive],  # 0 0 1 1
                       [dead,dead,alive,alive]]) # 0 0 1 1

    acorn = np.uint8([[dead,alive,dead,dead,dead,dead,dead],        # 0 1 0 0 0 0 0
                      [dead,dead,dead,alive,dead,dead,dead],        # 0 0 0 1 0 0 0
                      [alive,alive,dead,dead,alive,alive,alive]])   # 1 1 0 0 1 1 1

    gosper_gun = np.uint8([[dead,  dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead, dead, dead, dead, dead, dead, dead,dead,dead, dead, dead, dead,dead,alive,dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead],
                           [dead,  dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead, dead, dead, dead, dead, dead, dead,dead,dead, dead, dead,alive,dead,alive,dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead],
                           [dead,  dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead,alive,alive, dead, dead, dead, dead,dead,dead,alive,alive, dead,dead, dead,dead,dead,dead,dead,dead,dead,dead,dead,dead,alive,alive],
                           [dead,  dead,dead,dead,dead,dead,dead,dead,dead,dead, dead,alive, dead, dead, dead,alive, dead, dead,dead,dead,alive,alive, dead,dead, dead,dead,dead,dead,dead,dead,dead,dead,dead,dead,alive,alive],
                           [alive,alive,dead,dead,dead,dead,dead,dead,dead,dead,alive, dead, dead, dead, dead, dead,alive, dead,dead,dead,alive,alive, dead,dead, dead,dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead],
                           [alive,alive,dead,dead,dead,dead,dead,dead,dead,dead,alive, dead, dead, dead,alive, dead,alive,alive,dead,dead, dead, dead,alive,dead,alive,dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead],
                           [dead,  dead,dead,dead,dead,dead,dead,dead,dead,dead,alive, dead, dead, dead, dead, dead,alive, dead,dead,dead, dead, dead, dead,dead,alive,dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead],
                           [dead,  dead,dead,dead,dead,dead,dead,dead,dead,dead, dead,alive, dead, dead, dead,alive, dead, dead,dead,dead, dead, dead, dead,dead, dead,dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead],
                           [dead,  dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead,alive,alive, dead, dead, dead, dead,dead,dead, dead, dead, dead,dead, dead,dead,dead,dead,dead,dead,dead,dead,dead,dead, dead, dead]])

    switch_engine1 = np.uint8([[ dead,dead, dead,dead, dead,dead,alive, dead],
                               [ dead,dead, dead,dead,alive,dead,alive,alive],
                               [ dead,dead, dead,dead,alive,dead,alive, dead],
                               [ dead,dead, dead,dead,alive,dead, dead, dead],
                               [ dead,dead,alive,dead, dead,dead, dead, dead],
                               [alive,dead,alive,dead, dead,dead, dead, dead]])

    def __init__(self,grid_size=50):

        # Save off grid size
        self.grid_size = grid_size

        # Initialize maps
        self.map = self.empty_grid()
        self.img = self.empty_grid()

        # Define mapping for searching neighbor space
        self.nmap_r = [-1,-1,-1,0,0,1,1,1]
        self.nmap_c = [-1,0,1,-1,1,-1,0,1]

        # Status of evolution
        self.is_alive = True
        self.n_alive = 0

        # Generation counter
        self.n_gen = 0

        # Setup scale for rendering
        self.scale = 500/self.grid_size

    # Produce empty grid
    def empty_grid(self):
        return self.dead*np.ones((self.grid_size,self.grid_size),dtype=np.uint8)

    # Apply game laws for single step of evolution
    def evolve(self):
        # Reset image grid
        self.img = self.empty_grid()
        # Assume all nodes will die this generation
        self.n_alive = 0
        # Iterate over each node
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                # Number of neighbors a node has
                neighbor_count = 0
                # Check neighbors
                for i in range(len(self.nmap_r)):
                    r_check = r+self.nmap_r[i]
                    c_check = c+self.nmap_c[i]

                    if (r_check > 0 and
                        r_check <= self.grid_size-1 and
                        c_check > 0 and
                        c_check <= self.grid_size-1):

                        if self.map[r_check,c_check] == self.alive:
                            neighbor_count += 1

                # Apply game logic
                if self.map[r,c] == self.alive:
                    if neighbor_count in [2,3]:
                        self.img[r,c] = self.alive
                        self.n_alive += 1
                else:
                    if neighbor_count == 3:
                        self.img[r,c] = self.alive
                        self.n_alive += 1

        # Copy new map into static map
        self.map = self.img
        # Incrememnt generation counter
        self.n_gen += 1

    def render(self):
        S = cv2.resize(self.img,None,fx=self.scale,fy=self.scale,interpolation=cv2.INTER_NEAREST)
        S = self.apply_overlay(S)
        cv2.imshow('Game of Life',S)
        cv2.waitKey(300)

    def apply_overlay(self,s):
        font     = cv2.FONT_HERSHEY_SIMPLEX
        origin   = (10,20)
        fscale   = 0.5
        fcolor   = (0,0,0)
        linetype = 1
        text     = 'Generation %d' % self.n_gen
        return cv2.putText(s,text,origin,font,fscale,fcolor,linetype,cv2.LINE_AA)

    # Run game
    def run(self):
        # Run while someone is still alive
        while self.is_alive:
            self.render()
            self.evolve()
            if self.n_alive == 0:
                self.is_alive = False
            print('Generation %d' % self.n_gen)

        # Wait and destroy window
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def spawn(self,obj,o):
        for r in range(obj.shape[0]):
            for c in range(obj.shape[1]):
                rin = o[0]+r
                cin = o[1]+c
                self.map[rin,cin] = obj[r,c]

if __name__ == "__main__":
    gol = GameOfLife()
    gol.spawn(gol.switch_engine1,(20,20))
    gol.run()
