from Page import Page
import tkinter as tk


class Page1(Page):
    def __init__(self, mainPage):
        Page.__init__(self, mainPage)
        photo = tk.PhotoImage(file=r"images\bb.png")
        w = tk.Label(self, image=photo)
        w.place(x=0, y=0, relwidth=1, relheight=1)
        w.image = photo
