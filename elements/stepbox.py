import tkinter as tk

class StepBox(tk.LabelFrame):

    __steps = []

    def __init__(self, master, **kwargs):
        steps = kwargs.pop('steps')
        self.__steps = steps
        super().__init__(master, **kwargs)


        self.info = tk.Text(self, bg='white', wrap="word")
        #Prevent the user to be able to write in the text areas
        self.info.bind("<Key>", lambda e: "break")
        self.info.tag_configure("hidden", elide=True)
        self.info.tag_configure("bold", font=('Verdana', 10, 'bold'))
        for i, step in reversed(list(enumerate(self.__steps, start=1))):
            s = f'Step {i}: {step}\n'
            self.info.insert(1.0, s, (f'{i}', "bold"))
        self.info.tag_add("hidden", 1.0, tk.END)
        self.info.pack(expand=True, fill=tk.BOTH)


    def display_until_step(self, nb):
        self.info.tag_remove("hidden", 1.0, tk.END)
        _ , end_i = self.info.tag_ranges(f'{nb}')
        self.info.tag_add("hidden", end_i, tk.END)