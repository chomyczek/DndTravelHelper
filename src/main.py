import tkinter
from tkinter import Tk, Button, filedialog
from PIL import Image, ImageTk


def open_action(image_label):
    file_path = filedialog.askopenfile()
    if not file_path:
        return
    image1 = Image.open(file_path.name)
    test = ImageTk.PhotoImage(image1)

    image_label.config(image=test)
    image_label.image = test


root = Tk()
root.title('DnD travel helper')
root.geometry("600x400")

label1 = tkinter.Label()
click_button = Button(root, text="Open", width=8, command=lambda: open_action(label1))

click_button.pack()
label1.pack()





root.mainloop()
