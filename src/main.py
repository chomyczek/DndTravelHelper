from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from PIL.Image import Resampling

map_img = None
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400
CANVAS_WIDTH = WINDOW_WIDTH - 50
CANVAS_HEIGHT = WINDOW_HEIGHT - 50


def match_2_canvas(image):
    """
    Resize image if is bigger than canvas.
    :param image: Image to resize
    :return: Image that match canvas
    """
    x, y = image.size
    to_resize = False
    if x > CANVAS_WIDTH:
        to_resize = True
        ratio = CANVAS_WIDTH / x
        x = int(x * ratio)
        y = int(y * ratio)
    if y > CANVAS_HEIGHT:
        to_resize = True
        ratio = CANVAS_HEIGHT / y
        x = int(x * ratio)
        y = int(y * ratio)

    if to_resize:
        return image.resize((x, y), Resampling.LANCZOS)
    return image


def update_image():
    file_path = filedialog.askopenfile()
    if not file_path:
        return
    # image needs to be hold in global variable

    image = Image.open(file_path.name)
    image = match_2_canvas(image)
    global map_img
    map_img = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_container, image=map_img)


# Create an instance of tkinter frame
win = Tk()
win.title('DnD travel helper')
win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

canvas = Canvas(win, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()
button = ttk.Button(win, text="Open",
                    command=lambda: update_image())
button.pack()

image_container = canvas.create_image(0, 0, anchor=NW)
win.mainloop()
