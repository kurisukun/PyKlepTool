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
    
    #(ssk, psk)
    (__ssk, __psk) = (0, 0)
    #(sk, pk)
    (__sk, __pk) = (0, 0)

    #(Ki, Ci, tau)
    (__Ki1, __Ci1, __tau1) = (0, 0, 0)
    (__Ki2, __Ci2, __tau2) = (0, 0, 0)

    #(c, tag, n)
    (__c1, __tag1, __n1) = (0, 0, 0)
    (__c2, __tag2, __n2) = (0, 0, 0)

    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title(self.__WINDOW_TITLE)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(f'{width}x{height}')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.__create_widgets()
        self.__psk, self.__ssk = ASA_Gen()
        self.__sk, self.__pk  = ecies_key_gen()

    def __swap_attack_is_ready(self):
        self.__attack_is_ready = True

    def __send_message(self, in_title, in_mail, out_field):
        plain_mail = (f'TITLE: {in_title.get()}   FROM: ALICE\n\n'
        f'{in_mail.get("1.0", "end-1c")}\n\n')
        plain_mail = plain_mail.encode('utf-8')
        c = ""
        if self.__attack_is_ready == False:
            (self.__Ki1, self.__Ci1, self.__tau1) = ASA_Enc(self.__pk, self.__psk, 0)
            (self.__c1, self.__tag1, self.__n1) = DEM_Encrypt(self.__Ki1, plain_mail)
            c = self.__c1
        else:
            (self.__Ki2, self.__Ci2, self.__tau2) = ASA_Enc(self.__pk, self.__psk, self.__tau1)
            (self.__c2, self.__tag2, self.__n2) = DEM_Encrypt(self.__Ki2, plain_mail)
            c = self.__c2

        mail_content = plain_mail + (f'Encrypted content: {c}\n'
        f'----------------------------------------------------------\n\n').encode('utf-8')
        out_field.insert("1.0", mail_content)
        in_title.delete(0, tk.END)
        in_mail.delete(1.0, tk.END)

    def __asa_attack(self, attacker_psk, attacker_ssk, bob_psk, c1, c2, key, m):
        attacker_ssk.delete("1.0", tk.END)
        attacker_ssk.insert("1.0", self.__ssk)
        attacker_psk.delete("1.0", tk.END)
        attacker_psk.insert("1.0", self.__psk)
        bob_psk.delete("1.0", tk.END)
        bob_psk.insert("1.0", self.__pk)
        c1.delete("1.0", tk.END)
        c1.insert("1.0", self.__c1)
        c2.delete("1.0", tk.END)
        c2.insert("1.0", self.__c2)

        Ki_comp = ASA_Rec(self.__pk, self.__ssk, self.__Ci2, self.__Ci1)
        m_broken = asa_decrypt_broken(Ki_comp, self.__c2, self.__tag2, self.__n2)
        key.delete(0, tk.END)
        key.insert(0, Ki_comp)
        m.delete("1.0", tk.END)
        m.insert("1.0", m_broken)

    def __create_tab1(self, tab1, tab2):
        top_box = tk.Frame(tab1)
        top_box.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        bottom_box = tk.Frame(tab1)
        bottom_box.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)
        step_box = StepBox(top_box, text="ASA attack against ECIES KEM", relief=tk.RIDGE, steps=asa_ecies_steps1)
        step_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        chat_box = tk.LabelFrame(bottom_box, text="Send message to Bob")
        chat_box.pack(expand=True, fill=tk.X)
        
        in_mailbox = tk.Text(top_box)
        #Prevent the user to be able to write in the text areas
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
                                self.__send_message(in_title, in_mail, in_mailbox),
                                self.__swap_attack_is_ready()
                            ])
        bt_send.grid(row=2, column=0, padx=(10, 0), pady=(10, 10))

    def __create_tab2(self, tab):
        left_box = tk.Frame(tab)
        left_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        right_box = tk.Frame(tab)
        right_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        #LEFT
            # TOP
        keys_box = tk.Frame(left_box)
        keys_box.grid(row=0, column=0)

        attacker_keys_box = tk.LabelFrame(keys_box, text="Attacker keys")
        attacker_keys_box.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        lbl_attacker_ssk = tk.Label(attacker_keys_box, text="psk")
        lbl_attacker_ssk.grid(row=0,column=0)
        in_attacker_ssk = tk.Text(attacker_keys_box, height=5, width=60)
        in_attacker_ssk.bind("<Key>", lambda e: "break")
        in_attacker_ssk.grid(row=0, column=1)
        lbl_attacker_psk = tk.Label(attacker_keys_box, text="ssk")
        lbl_attacker_psk.grid(row=1,column=0)
        in_attacker_psk = tk.Text(attacker_keys_box, height=5, width=60)
        in_attacker_psk.bind("<Key>", lambda e: "break")
        in_attacker_psk.grid(row=1, column=1)

        bob_keys_box = tk.LabelFrame(keys_box, text="Bob's keys")
        bob_keys_box.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
        lbl_bob_psk = tk.Label(bob_keys_box, text="psk")
        lbl_bob_psk.grid(row=1,column=0)
        in_bob_psk = tk.Text(bob_keys_box, height=5, width=60)
        in_bob_psk.bind("<Key>", lambda e: "break")        
        in_bob_psk.grid(row=1, column=1)

            #BOTTOM
        ciphertexts_box = tk.Frame(left_box)
        ciphertexts_box.grid(row=1, column=0)
        c1_box = tk.LabelFrame(ciphertexts_box, text="Ciphertext1")
        c1_box.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        lbl_c1 = tk.Label(c1_box, text="")
        lbl_c1.grid(row=0,column=0)
        in_c1 = tk.Text(c1_box)
        in_c1.bind("<Key>", lambda e: "break")
        in_c1.grid(row=0, column=1)

        c2_box = tk.LabelFrame(ciphertexts_box, text="Ciphertext2")
        c2_box.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
        lbl_c2 = tk.Label(c2_box, text="")
        lbl_c2.grid(row=0,column=0)
        in_c2 = tk.Text(c2_box)
        in_c2.bind("<Key>", lambda e: "break")
        in_c2.grid(row=0, column=1)


        asa_box = tk.LabelFrame(left_box, text="ASA")
        asa_box.grid(row=2, column=0)
        lbl_session_key = tk.Label(asa_box, text="Session key")
        lbl_session_key.grid(row=0,column=0)
        in_session_key = tk.Entry(asa_box)
        in_session_key.bind("<Key>", lambda e: "break")
        in_session_key.grid(row=0, column=1)

        lbl_message = tk.Label(asa_box, text="Message")
        lbl_message.grid(row=1,column=0)
        in_message = tk.Text(asa_box)
        in_message.bind("<Key>", lambda e: "break")
        in_message.grid(row=1, column=1)

        bt_load_asa_params = tk.Button(left_box, text="ASA attack", 
                                        command=lambda: [
                                            self.__asa_attack(in_attacker_psk, in_attacker_ssk,
                                                    in_bob_psk, 
                                                    in_c1, in_c2, 
                                                    in_session_key, in_message)
                                        ])
        bt_load_asa_params.grid(row=3, column=0, columnspan=2, sticky='nesw', pady=(20, 20))

        #RIGHT
        step_box = StepBox(right_box, text="ASA attack against ECIES KEM", relief=tk.RIDGE, steps=asa_ecies_steps2)
        step_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        step_box.bind("<Key>", lambda e: "break")

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

        self.__create_tab1(tab1, tab2)
        self.__create_tab2(tab2)