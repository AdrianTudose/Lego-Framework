import random
import Pieces
from Page import Page
import tkinter as tk
from Render import Render


class Page2(Page):
    def __init__(self, mainPage, data):
        Page.__init__(self, mainPage)
        self.data = data

        photo = tk.PhotoImage(file=r"images\b4.png")
        w = tk.Label(self, image=photo)
        w.place(x=0, y=0, relwidth=1, relheight=1)
        w.image = photo

        self.img_list = list(Pieces.pieces.keys())

        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill='both', expand=True, padx=100)
        canvas.configure(bg="#d5e8d8")
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scroll.pack(side=tk.RIGHT, fill='y')
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_frame.configure(bg='#d5e8d8')
        canvas.create_window(0, 0, window=scrollable_frame, anchor='nw')

        for i in range(len(self.img_list)):
            btn1 = tk.Button(scrollable_frame, text="Show 3D model", width=20, height=1, background='#b2ebe3',
                             font='Arial',
                             command=lambda arg=i: self.showPice(self.img_list[arg]))

            label_img = tk.Label(scrollable_frame, text='{} :'.format(self.img_list[i]), font="Arial 14", fg="black",
                                 bg="#d5e8d8")
            label_img.pack(anchor='w', padx=30, pady=7, expand=True)
            btn1.pack(anchor='w', padx=30, pady=7, expand=True)

            photo = tk.PhotoImage(file=r"images\img\{}.PNG".format(self.img_list[i]))

            w = tk.Label(scrollable_frame, image=photo)
            w.pack(anchor='w', padx=30, pady=7, expand=True)
            w.image = photo
            spin = tk.Spinbox(scrollable_frame, from_=0, to=25)
            spin.pack(anchor='w', padx=30, pady=10, expand=True)
            self.data.spinners[i] = spin
        configuration = tk.Button(self, text="Configuration", command=mainPage.page3_switch, width=20, height=1,
                                  background='#b2ebe3',
                                  font='Arial').place(x=420, y=50)
        canvas.config(yscrollcommand=scroll.set)
        canvas.pack()

    def showPice(self,arg):
        render = Render(self.data.SPACE_WIDTH, self.data.SPACE_HEIGHT, self.data.SPACE_LENGTH, (0,10,-7))
        piece = Pieces.Piece(Pieces.pieces[arg], random.randint(0, 6))
        render.render("show_piece", piece)

    def getVals(self):
        self.data.piecesToUse.clear()
        for i in range(len(self.data.spinners)):
            val = self.data.spinners[i].get()
            self.data.piecesToUse[self.img_list[i]] = int(val)
