import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from setup_attacks.rsa.setup_rsa import *
from setup_attacks.rsa.rsa_demo import RsaDemo

def about():
    tk.messagebox.showinfo('About', 'Author: Chris Barros Henriques')


def main():
    window = tk.Tk()
    window.title("PyKlepTool")
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry(f'{width}x{height}')

    menu = tk.Menu(window)

    lbl = tk.Label(window, text="Welcome in PyKlepTool")
    lbl.pack()

    menu_item1 = tk.Menu(menu, tearoff=0)
    menu_item1.add_command(label='RSA', command=RsaDemo)
    menu_item1.add_command(label='ECIES', command=about)
    menu.add_cascade(label='Algorithms', menu=menu_item1)

    menu_item2 = tk.Menu(menu, tearoff=0)
    menu_item2.add_command(label='About', command=about)
    menu.add_cascade(label='More', menu=menu_item2)
    window.config(menu=menu)

    window.mainloop()


if __name__ == '__main__':
    main()
