from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

map_img = None


def update_image():
    file_path = filedialog.askopenfile()
    if not file_path:
        return
    # image needs to be hold in global variable
    global map_img
    map_img = ImageTk.PhotoImage(Image.open(file_path.name))
    canvas.itemconfig(image_container, image=map_img)


# Create an instance of tkinter frame
win = Tk()
win.title('DnD travel helper')
win.geometry("750x400")

canvas = Canvas(win, width=650, height=350)
canvas.pack()
button = ttk.Button(win, text="Open",
                    command=lambda: update_image())
button.pack()

image_container = canvas.create_image(0, 0, anchor=NW)
win.mainloop()
