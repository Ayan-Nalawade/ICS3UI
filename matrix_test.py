import numpy as np

mtrx = np.array([[3,0,2],
                    [0,3,0],
                    [3,0,0],
                    [1,0,0]
                    ])


d_plyr_pos = np.argwhere(mtrx == 1)[0]
print(d_plyr_pos)
print(mtrx[d_plyr_pos[0]][d_plyr_pos[1]])