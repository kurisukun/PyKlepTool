import tkinter as tk
from tkinter import ttk
from elements.stepbox import StepBox
from klepto_attacks.ecies.steps import steps_tab1 as asa_ecies_steps1
from klepto_attacks.ecies.steps import steps_tab2 as asa_ecies_steps2
from klepto_attacks.ecies.asa_ecies import *

class EciesDemo:
    """ECIES Demo"""

    __WINDOW_TITLE = "ECIES Demo"

    __attack_is_ready = False

    __attacker_keys = (0, 0)
    __alice_keys = (0, 0)
    __bob_keys = (0, 0)

    __ecies_params1 = (0, 0, 0)
    __ecies_params2 = (0, 0, 0)

    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title(self.__WINDOW_TITLE)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(f'{width}x{height}')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.__create_widgets()
        self.__attacker_keys = ASA_Gen()
        self.__alice_keys = ecies_key_gen()
        self.__bob_keys = ecies_key_gen()

    def __set_attack_is_ready(self):
        self.__attack_is_ready = not self.__attack_is_ready 

    def __create_tab1(self, tab):
        top_box = tk.Frame(tab)
        top_box.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        bottom_box = tk.Frame(tab)
        bottom_box.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)
        step_box = StepBox(top_box, text="ASA attack against ECIES KEM", relief=tk.RIDGE, steps=asa_ecies_steps1)
        step_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        chat_box = tk.LabelFrame(bottom_box, text="Send message to Bob")
        chat_box.pack(expand=True, fill=tk.X)
        
        in_mailbox = tk.Text(top_box)
        in_mailbox.bind("<Key>", lambda e: "break")
        in_mailbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        title_box = tk.Frame(chat_box)
        title_box.grid(row=0, column=0)
        from_box = tk.Frame(chat_box)
        from_box.grid(row=0, column=1)

        lbl_title = tk.Label(title_box, text="Title")
        lbl_title.grid(row=0,column=0)
        in_title = tk.Entry(title_box)
        in_title.grid(row=0, column=1)
        in_mail = tk.Text(chat_box)
        in_mail.grid(row=1, column=0)
        bt_send = tk.Button(chat_box, text="Send", bg="gainsboro", 
                            command=lambda:[
                                self.__set_attack_is_ready(),
                                self.__send_message(in_title, in_mail, in_mailbox, self.__attack_is_ready)
                            ])
        bt_send.grid(row=2, column=0, padx=(10, 0), pady=(10, 10))

    def __create_tab2(self, tab):
        left_box = tk.Frame(tab)
        left_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        right_box = tk.Frame(tab)
        right_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        #LEFT
        attacker_keys_box = tk.LabelFrame(left_box, text="Attacker keys")
        attacker_keys_box.pack(expand=True, fill=tk.X)
        
        attacker_keys_box = tk.Frame(attacker_keys_box)
        attacker_keys_box.grid(row=0, column=0)

        lbl_attacker_keys = tk.Label(attacker_keys_box, text="ssk")
        lbl_attacker_keys.grid(row=0,column=0)
        in_attacker_keys = tk.Entry(attacker_keys_box)
        in_attacker_keys.grid(row=0, column=1)
        lbl_attacker_keys = tk.Label(attacker_keys_box, text="psk")
        lbl_attacker_keys.grid(row=1,column=0)
        in_attacker_keys = tk.Entry(attacker_keys_box)
        in_attacker_keys.grid(row=1, column=1)

        #RIGHT
        step_box = StepBox(right_box, text="ASA attack against ECIES KEM", relief=tk.RIDGE, steps=asa_ecies_steps2)
        step_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        step_box.bind("<Key>", lambda e: "break")


    def __send_message(self, in_title, in_mail, out_field, attack_ready):
        plain_mail = (f'TITLE: {in_title.get()}   FROM: ALICE\n\n'
        f'{in_mail.get("1.0", "end-1c")}\n\n')
        plain_mail = plain_mail.encode('utf-8')
        if attack_ready:
            self.__ecies_params1 = ASA_Enc(self.__bob_keys[1], self.__attacker_keys[1], 0)
            (c, tag1, n1) = DEM_Encrypt(self.__ecies_params1[0], plain_mail)
        else:
            self.__ecies_params2 = ASA_Enc(self.__bob_keys[1], self.__attacker_keys[1], self.__ecies_params1[2])
            (c, tag2, n2) = DEM_Encrypt(self.__ecies_params2[0], plain_mail)

        mail_content = plain_mail + (f'Encrypted content: {c}\n'
        f'----------------------------------------------------------\n\n').encode('utf-8')
        out_field.insert("1.0", mail_content)
        in_title.delete(0, tk.END)
        in_mail.delete(1.0, tk.END)

    def __create_widgets(self):
        # Create some room around all elements of window
        self.window['padx'] = 5
        self.window['pady'] = 5

        frame_main = ttk.Notebook(self.window)
        tab1 = tk.Frame(frame_main)
        tab2 = tk.Frame(frame_main)

        frame_main.add(tab1, text ='Send mails')
        frame_main.add(tab2, text ='ASA ECIES')
        frame_main.pack(expand = 1, fill =tk.BOTH)

        self.__create_tab1(tab1)
        self.__create_tab2(tab2)