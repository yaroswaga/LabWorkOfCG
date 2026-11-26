import numpy as np
from src.rast import get_normal, get_normal_cross, print_treug
from numba import njit
# from cfg import persp_ref


class Renderer:

    def __init__(self, width, height, zoom, light, t, persp_ref):
        self.width = width
        self.height = height
        self.zoom = zoom
        self.angles = np.zeros(3) # [alpha, beta, gamma]
        self.offset_x = width // 2
        self.offset_y = height // 2
        self.persp_ref = persp_ref
        self.t = np.array(t, dtype=np.float64)
        self.light = light
        self.perspective = True

    def render(self, img_mat, z_buffer, scene):
        render(
            img_mat=img_mat, 
            z_buffer=z_buffer, 
            scene_coords=scene.coords, 
            scene_fs=scene.fs, 
            zoom=self.zoom,
            offset_x=self.offset_x, 
            offset_y=self.offset_y, 
            light=self.light
            )
    def render(self, img_mat, z_buffer, scene):
        coords = self.transform(scene.coords)
        a = self.zoom * (self.persp_ref if self.perspective else 1.0)
        render(img_mat, z_buffer, coords, scene.fs, a,
                      self.width / 2.0, self.height / 2.0,
                      self.light, self.perspective)
    
    @staticmethod
    def rotation_matrix(alpha, beta, gamma):
        """ Возвращает R """
        ca, sa = np.cos(alpha), np.sin(alpha)
        cb, sb = np.cos(beta), np.sin(beta)
        cg, sg = np.cos(gamma), np.sin(gamma)
        rx = np.array([[1, 0, 0], [0, ca, sa], [0, -sa, ca]])
        ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
        rz = np.array([[cg, sg, 0], [-sg, cg, 0], [0, 0, 1]])
        return rx @ ry @ rz
    
    def transform(self, coords):
        R = self.rotation_matrix(*self.angles)
        return coords @ R.T + self.t              # X' = R·X + t
    


@njit(cache=True)
def render(img_mat, z_buffer, scene_coords, scene_fs, zoom, offset_x, offset_y, light, perspective):
    lx, ly, lz = light[0], light[1], light[2]
    for i in scene_fs:
        v0 = scene_coords[i[0]]
        v1 = scene_coords[i[1]]
        v2 = scene_coords[i[2]]

        x0, y0, z0 = v0[0], v0[1], v0[2]
        x1, y1, z1 = v1[0], v1[1], v1[2]
        x2, y2, z2 = v2[0], v2[1], v2[2]

        nx, ny, nz = get_normal(x0, y0, z0, x1, y1, z1, x2, y2, z2)
        normal_cross = get_normal_cross(nx, ny, nz, lx, ly, lz)

        if normal_cross < 0:
            if perspective:
                px0 = x0 * zoom / z0 + offset_x
                py0 = -y0 * zoom / z0 + offset_y
                px1 = x1 * zoom / z1 + offset_x
                py1 = -y1 * zoom / z1 + offset_y
                px2 = x2 * zoom / z2 + offset_x
                py2 = -y2 * zoom /z2 + offset_y
            else:
                px0 = x0 * zoom + offset_x
                py0 = -y0 * zoom + offset_y
                px1 = x1 * zoom + offset_x
                py1 = -y1 * zoom + offset_y
                px2 = x2 * zoom + offset_x
                py2 = -y2 * zoom + offset_y

            color = np.array([-255 * normal_cross, 0, 0])

            print_treug(px0, py0, z0,
                        px1, py1, z1,
                        px2, py2, z2,
                        img_mat, color, z_buffer
                        )
