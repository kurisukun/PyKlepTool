import tkinter as tk
from tkinter import ttk
from elements.stepbox import StepBox

class EciesDemo:
    """ECIES Demo"""

    __WINDOW_TITLE = "ECIES Demo"

    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title(self.__WINDOW_TITLE)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(f'{width}x{height}')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.__create_widgets()

    def __create_tab2(self, tab):
        top_box = tk.Frame(tab)
        top_box.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        step_box = StepBox(top_box, text="ASA attack against ECIES KEM", relief=tk.RIDGE, steps=setup_rsa_steps)
        step_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        chat_box = tk.Frame(top_box)
        chat_box.pack(expand=True, fill=tk.X)


    def __create_widgets(self):
        # Create some room around all elements of window
        self.window['padx'] = 5
        self.window['pady'] = 5

        frame_main = ttk.Notebook(self.window)
        tab1 = tk.Frame(frame_main)
        tab2 = tk.Frame(frame_main)

        frame_main.add(tab1, text ='Normal ECIES')
        frame_main.add(tab2, text ='ASA ECIES')
        frame_main.pack(expand = 1, fill =tk.BOTH)

        self.__create_tab2(tab2)