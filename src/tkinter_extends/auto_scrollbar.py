import tkinter
from tkinter import ttk


class AutoScrollbar(ttk.Scrollbar):
    """
    A scrollbar that hides itself if it's not needed.
    Works only if you use the grid geometry manager.

    Borrowed: https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan/48137257#48137257
    """
    def set(self, lo, hi):
        """
        Set the fractional values of the slider position
        """
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tkinter.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tkinter.TclError('Cannot use place with this widget')