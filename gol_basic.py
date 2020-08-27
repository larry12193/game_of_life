import cv2
import time
import numpy as np

# Initial map
M = np.uint8([[0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,255,255,0],
    [0,0,255,255,0],
    [0,0,0,0,0]])
val_alive = 255
val_dead = 0
map_size = 5

# Map that gets displayed
Mshow = np.zeros((map_size,map_size),dtype=np.uint8)

# Mapping for releative neighbor coordinates
nmap = [-1,0,1]
nmap_r = [-1,-1,-1,0,0,1,1,1]
nmap_c = [-1,0,1,-1,1,-1,0,1]

# Flag when no node are alive, halts program
is_alive = True

n_generation = 0
n_still_alive = 0

# Run evolution
while is_alive:

    # Display state
    S = cv2.resize(M,None,fx=100,fy=100,interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Game of Life',S)
    cv2.waitKey(300)

    # Clear map that gets displayed
    Mshow = np.zeros((map_size,map_size),dtype=np.uint8)
    n_still_alive = 0

    # Iterate over each node
    for r in range(5):
        for c in range(5):
            # Number of neighbors a node has
            neighbor_count = 0
            # Check neighbors
            for i in range(len(nmap_r)):
                r_check = r+nmap_r[i]
                c_check = c+nmap_c[i]

                if (r_check > 0 and
                    r_check <= map_size-1 and
                    c_check > 0 and
                    c_check <= map_size-1):

                    if M[r_check,c_check] == val_alive:
                        neighbor_count += 1

            # Apply game logic
            if M[r,c] == val_alive:
                if neighbor_count in [2,3]:
                    Mshow[r,c] = val_alive
                    n_still_alive += 1
            else:
                if neighbor_count == 3:
                    Mshow[r,c] = val_alive
                    n_still_alive += 1

    # Upadate map
    M = Mshow
    n_generation += 1
    print('Generation = %d' % n_generation)

    if n_still_alive == 0:
        is_alive = False
        print('Evolution has ceased.')

cv2.waitKey(0)
cv2.destroyAllWindows()
