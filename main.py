import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import secrets
from setup_attacks.rsa.setup_rsa import *
from setup_attacks.rsa.steps import steps_tab1 as rsa_steps
from setup_attacks.rsa.steps import steps_tab2 as setup_rsa_steps
from base64 import b64encode

def random_key():
    key = b64encode(secrets.token_bytes(16)).decode('utf-8')
    key = numfy(key)
    return key

def change_value_elements(el, value):
    el.delete(1.0, tk.END)
    el.insert(1.0, value)

# Better encoding function thanks to https://stackoverflow.com/a/12626870/13329098
def numfy(s):
    number = 0
    for e in [ord(c) for c in s]:
        number = (number * 0x110000) + e
    return number

# Better decoding function thanks to https://stackoverflow.com/a/12626870/13329098
def denumfy(number):
    l = []
    while(number != 0):
        l.append(chr(number % 0x110000))
        number = number // 0x110000
    return ''.join(reversed(l))

def enable_element(elements):
    for el in elements:
        el["state"] = "normal"

class StepBox(tk.LabelFrame):

    __steps = []

    def __init__(self, master, **kwargs):
        steps = kwargs.pop('steps')
        self.__steps = steps
        super().__init__(master, **kwargs)


        self.info = tk.Text(self, bg='white')
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

class RsaDemo:
    """RSA Demo"""

    __WINDOW_TITLE = "RSA Demo"
    # cryptographic params for the setup attack demonstration
    __symmetric_key = 0
    __enc_symmetric_key = 0
    __NB_BITS_SETUP_ATTACK = 256

    # Parameters from legit RSA explanations where
    # e: is the public key
    # d: the private key
    # n: the modulus
    # p: prime number 1
    # q: prime number 2
    __rsa_params = (0, 0, 0, 0, 0)

    # Both keys use the format (e, d, n) where
    # e: is the public key
    # d: the private key
    # n: the modulus
    __attacker_key = (0, 0, 0)
    __user_key = (0, 0, 0)

    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title(self.__WINDOW_TITLE)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(f'{width}x{height}')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.__create_widgets()
        __symmetric_key = random_key()

    def __generate_symmetric_key(self, entry):
        key = random_key()
        self.__symmetric_key = key
        change_value_elements(entry, key)

    def __generate_enc_symmetric_key(self, entry):
        self.__enc_symmetric_key = rsa_encrypt(self.__symmetric_key, self.__user_key[0], self.__user_key[2])
        change_value_elements(entry, self.__enc_symmetric_key)

    def __generate_setup_key(self, entries):
        params = setup_attacker_key_gen(self.__NB_BITS_SETUP_ATTACK)
        self.__attacker_key = params
        lst_params = list(params)
        for i in range(len(lst_params)):
            change_value_elements(entries[i], lst_params[i])

    def __generate_setup_key_user(self, entries):
        params = setup_victim_key_gen(self.__NB_BITS_SETUP_ATTACK, self.__attacker_key[0], self.__attacker_key[2])
        self.__user_key = params
        lst_params = list(params)
        for i in range(len(lst_params)):
            change_value_elements(entries[i], lst_params[i])

    def __generate_rsa_key(self, entries):
        params = key_gen(self.__NB_BITS_SETUP_ATTACK)
        self.__rsa_params = params
        lst_params = list(params)
        for i in range(len(lst_params)):
            change_value_elements(entries[i], lst_params[i])

    def __encrypt_plaintext(self, in_field, out_field):
        plaintext = in_field.get("1.0", 'end-1c')
        enc_plaintext = numfy(plaintext)
        change_value_elements(out_field, rsa_encrypt(enc_plaintext, self.__rsa_params[0], self.__rsa_params[2]))

    def __decrypt_ciphertext(self, in_field, out_field):
        ciphertext = int(in_field.get("1.0", 'end-1c'))
        enc_plaintext = rsa_decrypt(ciphertext, self.__rsa_params[1], self.__rsa_params[2])
        change_value_elements(out_field, denumfy(enc_plaintext))

    def __set_nb_bits_size_key(self, size_key):
        if size_key == "":
            size_key = 0
        self.__NB_BITS_SETUP_ATTACK = int(size_key)
        print(f'NEW::: {self.__NB_BITS_SETUP_ATTACK}')

    def __create_tab1(self, tab1, tab2):
        top_box = tk.Frame(tab1)
        top_box.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        bottom_box = tk.Frame(tab1)
        bottom_box.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

        step_box = StepBox(top_box, text="RSA steps explanation", relief=tk.RIDGE, steps=rsa_steps)
        step_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)


        params_box = tk.Frame(top_box)
        params_box.pack(expand=True, fill=tk.BOTH)

        # l1
        l1 = tk.LabelFrame(params_box, text="Size of keys (default: 256 bits))")
        l1.pack(expand=True, side=tk.TOP)

        bt_size_key = tk.Button(l1, text="Size", bg="gainsboro",
                                command=lambda: self.__set_nb_bits_size_key(in_size_key.get()))

        bt_size_key.grid(row=1, column=0, padx=(10, 0))
        in_size_key = tk.Entry(l1)
        in_size_key.grid(row=1, column=1, padx=(100, 10), pady=(10,10))


        # l2
        l2 = tk.LabelFrame(params_box, text="User's cryptosystem values")
        # l2.grid(row=1, column=0, sticky=tk.W)
        l2.pack(expand=True, side=tk.BOTTOM)

        bt_user_key = tk.Button(l2, text="Generate new user key", bg="gainsboro",
                                command=lambda: [
                                    enable_element([in_user_e, in_user_d, in_user_n, in_user_p, in_user_q, in_encrypt_plain,
                                                    lbl_user_e, lbl_user_d, lbl_user_n, lbl_user_p, lbl_user_q, 
                                                    bt_encrypt_plain]),
                                    self.__generate_rsa_key([in_user_e, in_user_d, in_user_n, in_user_p, in_user_q]),
                                    step_box.display_until_step(1)])

        bt_user_key.grid(row=0, column=0, columnspan=2, sticky='nesw')
        lbl_user_e = tk.Label(l2, text="E (public exponent)", state="disabled")
        lbl_user_d = tk.Label(l2, text="D (private exponent)", state="disabled")
        lbl_user_n = tk.Label(l2, text="N", state="disabled")
        lbl_user_p = tk.Label(l2, text="P", state="disabled")
        lbl_user_q = tk.Label(l2, text="Q", state="disabled")

        lbl_user_p.grid(row=1, column=0)
        in_user_p = tk.Text(l2, height=5, width=60, state="disabled")
        in_user_p.grid(row=1, column=1, padx=(100, 10))

        lbl_user_q.grid(row=2, column=0)
        in_user_q = tk.Text(l2, height=5, width=60, state="disabled")
        in_user_q.grid(row=2, column=1, padx=(100, 10))

        lbl_user_e.grid(row=3, column=0)
        in_user_e = tk.Text(l2, height=5, width=60, state="disabled")
        in_user_e.grid(row=3, column=1, padx=(100, 10))

        lbl_user_d.grid(row=4, column=0)
        in_user_d = tk.Text(l2, height=5, width=60, state="disabled")
        in_user_d.grid(row=4, column=1, padx=(100, 10))

        lbl_user_n.grid(row=5, column=0)
        in_user_n = tk.Text(l2, height=5, width=60, state="disabled")
        in_user_n.grid(row=5, column=1, padx=(100, 10))

        sym_key_box = tk.LabelFrame(bottom_box, text="Plain- and ciphertexts")
        sym_key_box.pack(expand=True, fill=tk.BOTH)

        bt_encrypt_plain = tk.Button(sym_key_box, text="Encrypt plaintext", bg="gainsboro", state="disabled",
                                     command=lambda: [enable_element([in_encrypt_plain, in_decrypt_cipher,
                                                                    bt_decrypt_cipher]),
                                                      self.__encrypt_plaintext(in_encrypt_plain, in_decrypt_cipher),
                                                      step_box.display_until_step(2)])

        bt_encrypt_plain.grid(row=0, column=0)
        in_encrypt_plain = tk.Text(sym_key_box, height=5, width=60, state="disabled")
        in_encrypt_plain.grid(row=0, column=1, padx=(0, 10))

        bt_decrypt_cipher = tk.Button(sym_key_box, text="Decrypt ciphertext", bg="gainsboro", state="disabled",
                                         command=lambda: [enable_element([in_decrypt_cipher, in_pass_rsa,
                                                                          bt_pass_rsa]),
                                                          self.__decrypt_ciphertext(in_decrypt_cipher, in_pass_rsa),
                                                          step_box.display_until_step(4)])

        bt_decrypt_cipher.grid(row=0, column=2, padx=(10, 0))
        in_decrypt_cipher = tk.Text(sym_key_box, height=5, width=60, state="disabled")
        in_decrypt_cipher.grid(row=0, column=3, padx=(0, 10))

        bt_pass_rsa = tk.Button(sym_key_box, text="Go to SETUP attack", bg="gainsboro", state="disabled",
                                    command=lambda: [
                                        enable_element([in_pass_rsa]),
                                        #self.__decrypt_ciphertext(in_decrypt_cipher, in_pass_rsa),
                                        tab1.master.select(tab2),
                                        step_box.display_until_step(5)])

        bt_pass_rsa.grid(row=0, column=4, padx=(10, 0))
        in_pass_rsa = tk.Text(sym_key_box, height=5, width=60, state="disabled")
        in_pass_rsa.grid(row=0, column=5, padx=(0, 10))



    def __create_widgets(self):
        # Create some room around all elements of window
        self.window['padx'] = 5
        self.window['pady'] = 5

        #frame_main = tk.Frame(self.window)
        frame_main = ttk.Notebook(self.window)
        tab1 = tk.Frame(frame_main)
        tab2 = tk.Frame(frame_main)
        
        #frame_main.pack(fill=tk.BOTH)

        frame_main.add(tab1, text ='Normal RSA')
        frame_main.add(tab2, text ='SETUP RSA')
        frame_main.pack(expand = 1, fill =tk.BOTH)

        self.__create_tab1(tab1, tab2)
        

        top_box = tk.Frame(tab2)
        top_box.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        bottom_box = tk.Frame(tab2)
        bottom_box.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

        step_box = StepBox(top_box, text="SETUP attack against key generation in RSA", relief=tk.RIDGE, steps=setup_rsa_steps)
        step_box.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)


        params_box = tk.Frame(top_box)
        params_box.pack(expand=True, fill=tk.X)
        # l1
        l1 = tk.LabelFrame(params_box, text="Attacker's cryptosystem values")
        l1.pack(expand=True, side=tk.TOP)
        # l1.grid(row=0, column=0, sticky=tk.W)

        bt_attacker_key = tk.Button(l1, text="Generate new attacker key", bg="gainsboro",
                                    command=lambda: [
                                        enable_element([in_attacker_e, in_attacker_d, in_attacker_n,
                                                        lbl_attacker_e, lbl_attacker_d, lbl_attacker_n, bt_user_key]),
                                        self.__generate_setup_key([in_attacker_e, in_attacker_d, in_attacker_n]),
                                        step_box.display_until_step(1)])

        bt_attacker_key.grid(row=0, column=0, columnspan=2, sticky='nesw')
        lbl_attacker_e = tk.Label(l1, text="Attacker's e", state="disabled")
        lbl_attacker_d = tk.Label(l1, text="Attacker's d", state="disabled")
        lbl_attacker_n = tk.Label(l1, text="Attacker's n", state="disabled")

        lbl_attacker_e.grid(row=1, column=0)
        in_attacker_e = tk.Text(l1, height=5, width=60, state="disabled")
        in_attacker_e.grid(row=1, column=1, padx=(100, 10))

        lbl_attacker_d.grid(row=2, column=0)
        in_attacker_d = tk.Text(l1, height=5, width=60, state="disabled")
        in_attacker_d.grid(row=2, column=1, padx=(100, 10))

        lbl_attacker_n.grid(row=3, column=0)
        in_attacker_n = tk.Text(l1, height=5, width=60, state="disabled")
        in_attacker_n.grid(row=3, column=1, padx=(100, 10))

        # l2
        l2 = tk.LabelFrame(params_box, text="User's cryptosystem values")
        # l2.grid(row=1, column=0, sticky=tk.W)
        l2.pack(expand=True, side=tk.BOTTOM)

        bt_user_key = tk.Button(l2, text="Generate new user key", bg="gainsboro", state="disabled",
                                command=lambda: [
                                    enable_element([in_user_e, in_user_d, in_user_n,
                                                    lbl_user_e, lbl_user_d, lbl_user_n, bt_symmetric_key]),
                                    self.__generate_setup_key_user([in_user_e, in_user_d, in_user_n]),
                                    step_box.display_until_step(2)])

        bt_user_key.grid(row=0, column=0, columnspan=2, sticky='nesw')
        lbl_user_e = tk.Label(l2, text="Attacker's E", state="disabled")
        lbl_user_d = tk.Label(l2, text="Attacker's D", state="disabled")
        lbl_user_n = tk.Label(l2, text="Attacker's N", state="disabled")

        lbl_user_e.grid(row=1, column=0)
        in_user_e = tk.Text(l2, height=5, width=60, state="disabled")
        in_user_e.grid(row=1, column=1, padx=(100, 10))

        lbl_user_d.grid(row=2, column=0)
        in_user_d = tk.Text(l2, height=5, width=60, state="disabled")
        in_user_d.grid(row=2, column=1, padx=(100, 10))

        lbl_user_n.grid(row=3, column=0)
        in_user_n = tk.Text(l2, height=5, width=60, state="disabled")
        in_user_n.grid(row=3, column=1, padx=(100, 10))

        sym_key_box = tk.LabelFrame(bottom_box, text="Symmetric key")
        sym_key_box.pack(expand=True, fill=tk.BOTH)

        bt_symmetric_key = tk.Button(sym_key_box, text="Generate symmetric key", bg="gainsboro", state="disabled",
                                     command=lambda: [enable_element([in_symmetric_key, in_enc_symmetric_key,
                                                                      bt_attacker_key, bt_enc_symmetric_key]),
                                                      self.__generate_symmetric_key(in_symmetric_key),
                                                      step_box.display_until_step(3)])
        bt_symmetric_key.grid(row=0, column=0)
        in_symmetric_key = tk.Text(sym_key_box, height=5, width=60, state="disabled")
        in_symmetric_key.grid(row=0, column=1, padx=(0, 10))

        bt_enc_symmetric_key = tk.Button(sym_key_box, text="Encrypt", bg="gainsboro", state="disabled",
                                         command=lambda: [enable_element([in_enc_symmetric_key, in_setup_attack,
                                                                          bt_setup_attack]),
                                                          self.__generate_enc_symmetric_key(in_enc_symmetric_key),
                                                          step_box.display_until_step(4)])

        bt_enc_symmetric_key.grid(row=0, column=2, padx=(10, 0))
        in_enc_symmetric_key = tk.Text(sym_key_box, height=5, width=60, state="disabled")
        in_enc_symmetric_key.grid(row=0, column=3, padx=(0, 10))

        lbl_setup_attack = tk.Label(sym_key_box, text="Decrypted symmetric key by attacker", state="disabled")
        bt_setup_attack = tk.Button(sym_key_box, text="Setup Attack", bg="gainsboro", state="disabled",
                                    command=lambda: [
                                        enable_element([lbl_setup_attack, in_setup_attack]),
                                        change_value_elements(in_setup_attack, rsa_setup_attack(
                                            self.__enc_symmetric_key,
                                            self.__attacker_key[1],
                                            self.__attacker_key[2],
                                            self.__user_key[0],
                                            self.__user_key[2]
                                        )),
                                        step_box.display_until_step(5)])

        bt_setup_attack.grid(row=0, column=4, padx=(10, 0))
        in_setup_attack = tk.Text(sym_key_box, height=5, width=60, state="disabled")
        in_setup_attack.grid(row=0, column=5, padx=(0, 10))


def about():
    tk.messagebox.showinfo('About', 'Author: Chris Barros Henriques')


def main():
    window = tk.Tk()
    window.title("PyKlepTool")
    #width = window.winfo_screenwidth()
    #height = window.winfo_screenheight()
    #window.geometry(f'{width}x{height}')

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
