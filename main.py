from Data import Data
from MainView import MainView
from Page1 import Page1
from Page2 import Page2
from Page3 import Page3
from Page4 import Page4
import tkinter as tk


def main():
    root = tk.Tk()
    root.resizable(False, False)
    shared_data = Data()

    mainPage = MainView(root, shared_data)
    mainPage.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x600")

    p1 = Page1(mainPage)
    p2 = Page2(mainPage, shared_data)
    p3 = Page3(mainPage, shared_data)
    p4 = Page4(mainPage, shared_data)
    shared_data.page3 = p3
    shared_data.page2 = p2

    buttonframe = tk.Frame(mainPage)
    buttonframe.configure(bg="#d5e8d8")
    container = tk.Frame(mainPage)
    buttonframe.pack(side='top', fill='x', expand=False)
    container.pack(side='top', fill="both", expand=True)

    p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
    p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
    p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
    p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

    btn1 = tk.Button(p1, text="Add a new configuration", width=20, height=1, background='#b2ebe3', font='Arial',
                     command=p4.lift).place(x=50, y=50)

    b1 = tk.Button(buttonframe, text="Home Page", command=p1.lift, background='#b2ebe3', fg='black')
    b2 = tk.Button(p1, text="Preview configuration", command=p2.lift, width=20, height=1, background='#b2ebe3',
                   font='Arial').place(x=520, y=50)
    b1.pack(side='left', padx=15, pady=10)
    back = tk.Button(p3, text="Back", command=p2.lift, width=8, height=1, background='#b2ebe3', font='Arial').place(
        x=1, y=30)
    startAlgBtn = tk.Button(p3, text="GO!", command=mainPage.startAlg, width=8, height=1, background='#b2ebe3',
                            font='Arial').place(x=685, y=30)
    showConfig = tk.Button(p3, text="Show", command=mainPage.showConfig, width=8, height=1, background='#b2ebe3',
                            font='Arial').place(x=685, y=100)

    p1.show()

    root.mainloop()


if __name__ == '__main__':
    main()
