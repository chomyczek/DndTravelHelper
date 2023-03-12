from tkinter import *
from tkinter import ttk, filedialog

from src.tkinter_extends.zoomable_image import ZoomableImage

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400


def update_image(image_object):
    file_path = filedialog.askopenfile(filetypes=[('Images', '*.jpg *.png'), ('All', '*.*')])
    if not file_path:
        return
    image_object.set_image(file_path.name)


win = Tk()
win.title('DnD travel helper')
win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
img = ZoomableImage(win)
button = ttk.Button(win, text="Open",
                    command=lambda: update_image(img))
button.grid(column=0, row=img.grid_size()[1])

win.mainloop()
