import tkinter
from tkinter import Tk, Button, filedialog
from PIL import Image, ImageTk


def open_action(image_label):
    file_path = filedialog.askopenfile()
    if not file_path:
        return
    image = Image.open(file_path.name)
    resized_img = image.resize((600, 350))
    image_tk = ImageTk.PhotoImage(resized_img)

    image_label.config(image=image_tk)
    image_label.image = image_tk


root = Tk()
root.title('DnD travel helper')
root.geometry("600x400")

map_label = tkinter.Label()
click_button = Button(root, text="Open", width=8, command=lambda: open_action(map_label))

click_button.pack()
map_label.pack()

root.mainloop()
