from cfg import OBJECTS
import numpy as np


class Scene:
    def __init__(self, filename="model.obj"):
        self.coords, self.fs = self.load_obj(filename)

    def load_obj(self, filename):
        coords = []
        fs = []
        with open(f"{OBJECTS}/{filename}", encoding="utf-8") as file:
            for line in file:
                sp = line.split()
                if not sp:
                    continue
                if sp[0] == "v":
                    coords.append([float(x) for x in sp[1:4]])
                elif sp[0] == "f":
                    idx = [int(x.split("/")[0]) - 1 for x in sp[1:]]
                    # веерная триангуляция (работает и для квадов, и для n-угольников)
                    for k in range(1, len(idx) - 1):
                        fs.append([idx[0], idx[k], idx[k + 1]])
        self.coords = np.array(coords, dtype=np.float64)
        self.fs = np.array(fs, dtype=np.int64)
        
        return (np.array(coords, dtype=np.float64),
                np.array(fs, dtype=np.int64))