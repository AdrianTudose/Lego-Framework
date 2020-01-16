import pickle
import random
import numpy as np
import Pieces
from Configuration import Configuration
from Page import Page
import tkinter as tk
from Render import Render
from tkinter import messagebox

class Page4(Page):
    def __init__(self, mainPage, data):
        Page.__init__(self, mainPage)
        self.data = data
        self.name = ''
        self.configure(bg="#fcdfc7")
        self.space = np.zeros((self.data.SPACE_WIDTH, self.data.SPACE_HEIGHT, self.data.SPACE_LENGTH), dtype=int)

        photo = tk.PhotoImage(file=r"images\b4.png")
        w = tk.Label(self, image=photo)
        w.place(x=0, y=0, relwidth=1, relheight=1)
        w.image = photo

        img_list = list(Pieces.pieces.keys())

        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill='both', expand=True, padx=100)
        canvas.configure(bg="#d5e8d8")
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scroll.pack(side=tk.RIGHT, fill='y')
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_frame.configure(bg='#d5e8d8')
        canvas.create_window(0, 0, window=scrollable_frame, anchor='nw')

        label_entry = tk.Label(canvas, text='Name your configuration:', font="Arial", fg="black",
                             bg="#d5e8d8").place(x=330, y=30)

        self.e = tk.Entry(canvas)
        self.e.pack(anchor='ne', pady=67, padx=80)

        saveConf = tk.Button(self, text="Save configuration", width=20, height=1, background='#b2ebe3',  command=self.saveConfig,
                      font='Arial').place(x=420, y=100)
        clear = tk.Button(self, text="Reset configuration",command=self.newSpace, width=20, height=1, background='#b2ebe3',
                                  font='Arial').place(x=420, y=150)

        for i in range(len(img_list)):
            btn1 = tk.Button(scrollable_frame, text="Add", width=20, height=1, background='#b2ebe3',
                             font='Arial',
                             command=lambda arg=i: self.draw(img_list[arg]))

            label_img = tk.Label(scrollable_frame, text='{} :'.format(img_list[i]), font="Arial 14", fg="black",
                                 bg="#d5e8d8")
            label_img.pack(anchor='w', padx=30, pady=7, expand=True)
            btn1.pack(anchor='w', padx=30, pady=7, expand=True)

            photo = tk.PhotoImage(file=r"images\img\{}.PNG".format(img_list[i]))

            w = tk.Label(scrollable_frame, image=photo)
            w.pack(anchor='w', padx=30, pady=7, expand=True)
            w.image = photo

        canvas.config(yscrollcommand=scroll.set)
        canvas.pack()

    def draw(self, arg):
        if self.e.get() == '':
            messagebox.showwarning("Warning", "Please name your configuration first")
            return
        if ' ' in self.e.get():
            messagebox.showwarning("Warning", "Invalid name.\nDon't use spaces for name.")
            return
        render = Render(self.data.SPACE_WIDTH, self.data.SPACE_HEIGHT, self.data.SPACE_LENGTH, (7,6,-8))
        piece = Pieces.Piece(Pieces.pieces[arg], random.randint(0, 6))
        new_space = render.render("add", piece, self.space, save_name=self.e.get())
        if type(new_space) == list:
            self.space = new_space

    def newSpace(self):
        self.space = np.zeros((self.data.SPACE_WIDTH, self.data.SPACE_HEIGHT, self.data.SPACE_LENGTH), dtype=int)
        self.e.delete(0, tk.END)

    def saveConfig(self):
        if self.e.get() == '':
            tk.messagebox.showwarning("Warning", "Please set a name for your configuration.")
            return
        if ' ' in self.e.get():
            tk.messagebox.showwarning("Warning", "Invalid name.\nDon't use spaces for name.")
            return

        conf = Configuration(self.e.get(), self.space)

        with open('ConfigurationsList.bin', 'rb') as f:
            data_loaded = pickle.load(f)

        data_loaded.append(conf)

        with open('ConfigurationsList.bin', 'wb') as f:
            pickle.dump(data_loaded, f)
