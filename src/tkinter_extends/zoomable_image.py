import tkinter
from tkinter import ttk
from PIL import Image, ImageTk, UnidentifiedImageError

from src.tkinter_extends.auto_scrollbar import AutoScrollbar


class ZoomableImage(ttk.Frame):
    """
    Advanced zoom of the image class expanding tkinter Frame class

    Borrowed: https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan/48137257#48137257
    """

    def __init__(self, mainframe):
        """
        Initialize the zoomable image
        :param mainframe: The application main frame
        """
        ttk.Frame.__init__(self, master=mainframe)
        self.container = None
        self.height = None
        self.width = None
        self.image = None
        horizontal_bar, vertical_bar = self._initialize_scrolbars()
        self.canvas = self._initialize_canvas(horizontal_bar, vertical_bar)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas

        self.img_scale = 1.0  # scale for the canvas image
        self.delta = 1.3  # zoom magnitude

    def _initialize_canvas(self, horizontal_bar, vertical_bar):
        """
        Create canvas with events
        """
        canvas = tkinter.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=horizontal_bar.set, yscrollcommand=vertical_bar.set)
        canvas.grid(row=0, column=0, sticky='nswe')
        canvas.update()  # wait till canvas is created

        # Bind events to the Canvas
        canvas.bind('<ButtonPress-3>', self.move_from_event)  # right mouse button
        canvas.bind('<B3-Motion>', self.move_to_event)
        canvas.bind('<MouseWheel>', self.wheel_event)  # with Windows and macOS, but not Linux
        canvas.bind('<Button-5>', self.wheel_event)  # only with Linux, wheel scroll down
        canvas.bind('<Button-4>', self.wheel_event)  # only with Linux, wheel scroll up
        return canvas

    def _initialize_scrolbars(self):
        """
        Initialize vertical and horizontal scrollbars for canvas
        """
        vertical_bar = AutoScrollbar(self.master, orient='vertical')
        horizontal_bar = AutoScrollbar(self.master, orient='horizontal')
        vertical_bar.grid(row=0, column=1, sticky='ns')
        horizontal_bar.grid(row=1, column=0, sticky='we')
        vertical_bar.configure(command=self.scroll_y_command)
        horizontal_bar.configure(command=self.scroll_x_command)
        return horizontal_bar, vertical_bar

    def set_image(self, path):
        """
        Set new image on canvas
        :param path: Path to an image
        """
        try:
            self.image = Image.open(path)
        except UnidentifiedImageError as e:
            print(f'\'{path}\' is not supported image.')
            return
        self.width, self.height = self.image.size
        self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
        self.show_image()

    def scroll_y_command(self, *args, **kwargs):
        """
        Scroll canvas vertically and redraw the image
        """
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x_command(self, *args, **kwargs):
        """
        Scroll canvas horizontally and redraw the image
        """
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from_event(self, event):
        """
        Remember previous coordinates for scrolling with the mouse
        """
        self.canvas.scan_mark(event.x, event.y)

    def move_to_event(self, event):
        """
        Drag (move) canvas to the new position
        """
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def grid_size(self) -> tuple[int, int]:
        """
        Size of the grid
        :return: Tuple of the number of column and rows in the grid
        """
        min_grid_size = 2
        size = super().grid_size()
        return max(min_grid_size, size[0]), max(min_grid_size, size[1])

    def wheel_event(self, event):
        """
        Zoom with mouse wheel
        """
        if not self.container:
            return  # image is not yet loaded
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            pass  # Ok! Inside the image
        else:
            return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.img_scale) < 500:
                return  # image is less than 500 pixels
            self.img_scale /= self.delta
            scale /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.img_scale:
                return  # 1 pixel is bigger than the visible area
            self.img_scale *= self.delta
            scale *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()

    def show_image(self):
        """
        Show image on the Canvas
        """
        if not self.container:
            return  # image is not yet loaded
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.img_scale), self.width)  # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.img_scale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.img_scale), int(y1 / self.img_scale), x, y))
            image_tk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            image_id = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=image_tk)
            self.canvas.lower(image_id)  # set image into background
            self.canvas.image_tk = image_tk  # keep an extra reference to prevent garbage-collection
