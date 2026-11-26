# import numpy as np
# from PIL import Image, ImageTk
# from cfg import *
# from src.scene import Scene
# from src.renderer import Renderer
# import tkinter as tk


# img_mat = np.zeros((height, width, 3), dtype=np.uint8)
# def reset_img_mat():
#     global img_mat
#     img_mat = np.zeros((height, width, 3), dtype=np.uint8)


# # img_mat = reset_img_mat()
# z_buffer = np.full((height, width), np.inf)
# scene = Scene("model.obj")
# renderer = Renderer(width, height, zoom, start_t, light, persp_ref)

# renderer.render(img_mat, z_buffer, scene)
# class App:
#     def __init__(self, scene, renderer, win_w = 900, win_h = 900):
#         self.scene = scene
#         self.renderer = renderer

#         # Оставляем как есть
#         # Окно верхнего уровня
#         self.root = tk.Tk()
#         # Размеры окна
#         self.root.geometry(f"{win_w}x{win_h}")
#         # Область для рисования внутри окна
#         self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
#         self.canvas.pack(fill='both', expand=True)
#         self.canvas.focus_set()
#         # Обновление изображения при изменении размеров окна
#         self.canvas.bind('<Configure>', lambda e: self._refit())
#         # Привязка обработчика клавиш
#         self.root.bind('<Key>', self.on_key)

#         # Изображение внутри окна
#         self.photo = None
#         self.full_image = None

#         self.render()

#     def on_key(self, event):
#         k = event.keysym

#         if k == 'plus':
#             self.renderer.zoom *= 1.1
#         elif k == 'minus':
#             self.renderer.zoom /= 1.1
#         elif k == 'Left':
#             print("left")
#         elif k == 'Right':
#             print("right")
#         else:
#             return

#         self.render()
#         # Не обрабатываем дальше – return 'brake'
#         return 'break'

#     def render(self):
#         # reset_img_mat()
#         global img_mat, z_buffer
#         img_mat.fill(0)
#         z_buffer.fill(np.inf)

#         self.renderer.render(img_mat, z_buffer, self.scene)
#         self.full_image = Image.fromarray(img_mat)
#         self._refit()

#     # скопировать как есть
#     def _refit(self):
#         # Если ещё не отрендерилось, пропускаем
#         if self.full_image is None: return
#         # Ширина и высота области для рисования
#         ww = self.canvas.winfo_width()
#         wh = self.canvas.winfo_height()
#         # Если вдруг сделали область слишком маленькой
#         if ww < 10 or wh < 10: return
#         # Вписать с сохранением пропорций
#         s = min(ww / width, wh / height)
#         dw = max(1, int(width * s))
#         dh = max(1, int(height * s))
#         disp = self.full_image.resize((dw, dh), Image.BILINEAR)
#         # Очень важно сохранить ImageTk.PhotoImage(disp) в поле класса
#         # Если оно будет локальным, то удалится после выхода сборщиком мусора
#         self.photo = ImageTk.PhotoImage(disp)
#         self.canvas.delete('all')
#         self.canvas.create_image(ww // 2, wh // 2, image=self.photo)

#     # скопировать как есть
#     def run(self):
#         self.root.mainloop()


# img = Image.fromarray(img_mat)
# img.save(IMAGES + "/img1.png")
# if __name__ == '__main__':
#     App(scene, renderer, width, height).run()

import numpy as np
from PIL import Image, ImageTk
from cfg import height, width, zoom, IMAGES, light, start_t, persp_ref
from src.scene import Scene
from src.renderer import Renderer
import tkinter as tk

ROT_STEP = np.radians(5) # шаг поворота
MOVE_STEP = 0.005 # шаг сдвига


img_mat = np.zeros((height, width, 3), dtype=np.uint8)
z_buffer = np.full((height, width), np.inf)
scene = Scene("model.obj")
renderer = Renderer(width, height, zoom, light, start_t, persp_ref)


class App:
    def __init__(self, scene, renderer, win_w = 900, win_h = 900):
        self.scene = scene
        self.renderer = renderer

        self.root = tk.Tk()

        self.root.geometry(f"{win_w}x{win_h}")

        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.focus_set()
        self.canvas.bind('<Configure>', lambda e: self._refit())
        self.root.bind('<Key>', self.on_key)

        # Изображение внутри окна
        self.photo = None
        self.full_image = None

        self.render()

    def on_key(self, event):
        k = event.keysym.lower()
        r = self.renderer

        # масштаб
        if k in ('plus', 'equal'):
            r.zoom *= 1.1
        elif k == 'minus':
            r.zoom /= 1.1
        # сдвиг tX, tY, tZ
        elif k == 'left':
            r.t[0] -= MOVE_STEP
        elif k == 'right':
            r.t[0] += MOVE_STEP
        elif k == 'up':
            r.t[1] += MOVE_STEP
        elif k == 'down':
            r.t[1] -= MOVE_STEP
        elif k == 'bracketright':      # ]  дальше от камеры
            r.t[2] += MOVE_STEP
        elif k == 'bracketleft':       # [  ближе к камере
            r.t[2] -= MOVE_STEP
        # повороты: a/d вокруг Y, w/s вокруг X, q/e вокруг Z
        elif k == 'a':
            r.angles[1] -= ROT_STEP
        elif k == 'd':
            r.angles[1] += ROT_STEP
        elif k == 'w':
            r.angles[0] += ROT_STEP
        elif k == 's':
            r.angles[0] -= ROT_STEP
        elif k == 'q':
            r.angles[2] -= ROT_STEP
        elif k == 'e':
            r.angles[2] += ROT_STEP
        # проекция
        elif k == 'p':
            r.perspective = not r.perspective
        # сброс
        elif k == 'r':
            r.t[:] = start_t
            r.angles[:] = 0.0
            r.zoom = zoom
        else:
            return

        self.render()
        return 'break'

    def render(self):
        # reset_img_mat()
        global img_mat, z_buffer
        img_mat.fill(0)
        z_buffer.fill(np.inf)

        self.renderer.render(img_mat, z_buffer, self.scene)
        self.full_image = Image.fromarray(img_mat)
        self._refit()

    def _refit(self):
        if self.full_image is None: return
        
        ww = self.canvas.winfo_width()
        wh = self.canvas.winfo_height()
        
        if ww < 10 or wh < 10: return
        
        s = min(ww / width, wh / height)
        dw = max(1, int(width * s))
        dh = max(1, int(height * s))
        disp = self.full_image.resize((dw, dh), Image.BILINEAR)
    
        self.photo = ImageTk.PhotoImage(disp)
        self.canvas.delete('all')
        self.canvas.create_image(ww // 2, wh // 2, image=self.photo)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    App(scene, renderer, width, height).run()
