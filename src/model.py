import numpy as np
from math import floor


class Model:
    def __init__(self, img_mat, zoom):
        self.full_coords = []
        self.img_mat = img_mat
        self.coords = []
        self.zoom = zoom
        self.fs = []
        self.open_coords()  
    
    
    def open_coords(self):
        with open("objects/model.obj") as file:
            for line in file:
                sp = line.split()
                # add_el = 
                if sp[0] == "v":
                    add_el = np.array(list(map(float, sp[1:])))
                    self.coords.append(add_el)
                elif sp[0] == "f":
                    add_el = np.array(list([int(x.split("/")[0]) - 1 for x in sp[1:]]))
                    self.fs.append(add_el)
                else:
                    add_el = sp
                self.full_coords.append(add_el)


    def print_line(self, x0, y0, x1, y1):
        dmax = max(abs(abs(floor(x0)) - abs(floor(x1))), abs(abs(floor(y0)) - abs(floor(y1))))

        L = dmax + 1
        if L == 1:
            self.img_mat[-floor(y0), floor(x0)] = 255
            return
        
        dx = (x1 - x0)/(L - 1)
        dy = (y1 - y0)/(L - 1)

        x = x0
        y = y0

        # while (floor(x) != floor(x1) and floor(y) != floor(y1)):
        for _ in range(L):
            self.img_mat[-floor(y), floor(x)] = 255
            x += dx
            y += dy

    def print_coords(self):
        for coord in self.coords:
            self.img_mat[-floor(coord[1] * self.zoom + self.zoom // 10), floor(coord[0] * self.zoom + self.zoom // 10)] = 255

    def print_poligons(self):
        for i in self.fs:
            # print(self.coords[i[0]])
            self.print_line(
                self.coords[i[0]][0] * self.zoom + self.zoom // 10, self.coords[i[0]][1] * self.zoom + self.zoom // 10, 
                self.coords[i[1]][0] * self.zoom + self.zoom // 10, self.coords[i[1]][1] * self.zoom + self.zoom // 10 
                )
            self.print_line(
                            self.coords[i[0]][0] * self.zoom + self.zoom // 10, self.coords[i[0]][1] * self.zoom + self.zoom // 10, 
                            self.coords[i[2]][0] * self.zoom + self.zoom // 10, self.coords[i[2]][1]* self.zoom + self.zoom // 10
                            )
            self.print_line(
                            self.coords[i[1]][0] * self.zoom + self.zoom // 10, self.coords[i[1]][1] * self.zoom + self.zoom // 10, 
                            self.coords[i[2]][0] * self.zoom + self.zoom // 10, self.coords[i[2]][1] * self.zoom + self.zoom // 10
                            )

    def print_model(self):
        self.print_coords()
        self.print_poligons()
