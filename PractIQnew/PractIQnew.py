import tkinter as tk
from tkinter import filedialog as fd, font, messagebox
from random import randint
from Ciphres import newkeys, encrypt, decrypt, PrivateKey

class Crypto(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._methods = [("RSA", 1)] #[("RSA", 1), ("ECB", 2), ...]
        self.method = tk.IntVar()
        self._default_data = ''
        self.name = ''
        self._key = tk.StringVar()

    def encry(self):
        if(self._default_data != ''):
            (self._pubkey, self.__privkey) = newkeys(82 + len(self._default_data)*8) #Первые 82 байта заняты методом. Каждые 8 следующих байт идут на один символ сообщения в файле
            self.__crypto_data = encrypt(self._default_data, self._pubkey)
            with open (self.name, 'w') as f:
                f.write(self.__crypto_data)
            keys_file = 'keys.txt'
            with open (keys_file, 'w') as f:
                f.write(str(self.__privkey) + '\n')
                f.write(str(self._pubkey))
            messagebox.showinfo("Оповещение", "Файл зашифрован\nКлючи находятся в файле " + keys_file)
        else:
            messagebox.showinfo("Замечание", "Нечего шифровать")

    def decry(self):
        if(self._default_data != ''):
            k = self._key.get()
            if(k):
                self.__subkeys = k.split(', ')
                if(len(self.__subkeys) == 5):
                    self.__privkey = PrivateKey(int(self.__subkeys[0]), int(self.__subkeys[1]), int(self.__subkeys[2]), int(self.__subkeys[3]), int(self.__subkeys[4]))
                    self.__crypto_data = decrypt(self._default_data, self.__privkey)
                    with open (self.name, 'w') as f:
                        f.write(self.__crypto_data)
                    messagebox.showinfo("Оповещение", "Файл расшифрован")
                else: messagebox.showinfo("Замечание", "Что-то не так с закрытым ключом")
            else:
                messagebox.showinfo("Замечание", "Закрытый ключ не указан")
        else:
            messagebox.showinfo("Замечание", "Нечего расшифровывать")

class Khalifard(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text = 'Главная')
        label.pack(pady = 10, padx = 10)
        button = tk.Button(self, text = 'Лечение вирусного файла', font = "georgia 10",
                           command = lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text = 'Маскировка', font = "georgia 10",
                            command = lambda: controller.show_frame(PageTwo))
        button2.pack()

class PageOne(tk.Frame):
    def show_message(self):
        messagebox.showinfo("GUI Python", self.message.get())

    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text = 'Лечение вирусного файла', font = "georgia 10",)
        label.pack(pady = 10, padx = 10)

        button1 = tk.Button(self, text = 'На главную', font = "georgia 10",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()

class PageTwo(Crypto):

    def callback(self):
        self.name = fd.askopenfilename()
        if self.name:
            with open (self.name, 'r') as f:
                self._default_data = f.read()
                if(self._default_data == ''): messagebox.showinfo("Оповещение", "Файл пуст")
                else: self.file_button.config(text = 'Файл выбран', bg = '#F07241', fg = '#120012')
        else:
            messagebox.showinfo("Оповещение", "Вы не выбрали файл")

    def entry_key(self):
        self.key_button.pack_forget()
        self.message_entry.pack(fill = 'x', pady = "5", side = 'bottom')

    def update_pos(self):
        self.on_main_button.place(relx = 0.5, rely = 1 - (0.06 * 322 / self.winfo_height()), anchor = 'center', height = 20, width = 85)
        self.after(50, self.update_pos)

    def encrypt_radio_activate(self):
        self.key_button.pack_forget()
        self.message_entry.pack_forget()
        self._key.set('')

    def decrypt_radio_activate(self):
        self.key_button.pack(fill='x', side='bottom')
        self.message_entry.pack_forget()
        self._key.set('')

    def select(self):
        l = self.method.get()
        if l == 1:
            self.sel.config(text = "Выберите дальнейшее действие")
            self.decrypt_radio.place(relx=0.25, rely=0.4 + self.row/10.0, anchor='center', height = 30, width = 112)
            self.encrypt_radio.place(relx=0.75, rely=0.4 + self.row/10.0, anchor='center', height = 30, width = 112)
    
    def apply(self):
        u = self.operation.get()
        if u == 1:
            self.decry()
        elif u == 2:
            self.encry()
        else:
            messagebox.showinfo("Оповещение", "Не выбрано действие или метод шифрования")

    def __init__(self, parent, controller):
        super().__init__(parent)     
        self.config(bg = '#240024')
        label = tk.Label(self, text = 'Маскировка', bg = '#120012', fg = '#c84848', padx = "228", pady = "14")\
                             .pack(side = 'top', fill = 'x')

        self.file_button = tk.Button(self, text = "Выберите файл", bg = '#120012', fg = '#c84848', font = "georgia 10", command = self.callback)
        self.file_button.pack(fill = 'x')

        header = tk.Label(self, text = "Выберите метод шифрования", font = "font 8", padx = 15, pady = 10, bg = '#240024', fg = '#F07241')\
                              .place(relx = 0.5, rely = 0.3, anchor = 'center', height = 30, width = 220)

        self.row = 1
        for txt, val in self._methods:
            tk.Radiobutton(self, text = txt, value = val, variable = self.method, padx = 15,
                           pady = 10, command=self.select, bg = '#240024', fg = '#c84848')\
                               .place(relx=0.5, rely=0.3 + self.row/10.0, anchor='center', height = 30, width = 220)
            self.row += 1
        #Если потом понадобится постоянно дополнять список, то можно установить self.row у главного класса.
        #Чтобы иничиализировать начальную высоту оконного приложения при запуске в зависиммости от значения self.row.
 
        self.sel = tk.Label(self, padx = 15, pady = 10, bg = '#240024', fg = '#F07241')
        self.sel.place(relx = 0.5, rely = 0.3 + self.row/10.0, anchor = 'center', height = 30, width = 220)

        self.operation = tk.IntVar()
        self.decrypt_radio = tk.Radiobutton(self, text = 'Расшифровать', value = 1, variable = self.operation, padx = 15, pady = 10,
                                            bg = '#240024', fg = '#c84848', command = self.decrypt_radio_activate)
        
        self.encrypt_radio = tk.Radiobutton(self, text = 'Зашифровать', value = 2, variable = self.operation, padx = 15, pady = 10,
                                            bg = '#240024', fg = '#c84848', command = self.encrypt_radio_activate)  

        footer = tk.Label(self, bg = '#120012', fg = '#c84848', padx = "228", pady = "20")\
            .pack(side = 'bottom', fill = 'x')

        crypt_button = tk.Button(self, text = 'Применить', font = "georgia 10", bg = '#120012', fg = '#c84848', command = self.apply)
        crypt_button.pack(fill='x', side='bottom')

        self.key_button = tk.Button(self, text = "Введите закрытый ключ", bg = '#120012', fg = '#c84848', font = "georgia 10", command = self.entry_key)

        self.message_entry = tk.Entry(self, textvariable = self._key, font = "georgia 10")
        
        self.on_main_button = tk.Button(self, text = 'На главную', font = "georgia 10", bg = '#120012', bd = 0, fg = '#c84848',
                                        command = lambda: (self.sel.config(text = ""), controller.show_frame(StartPage)))
        self.on_main_button.place(relx = 0.5, rely = 1 - 0.06, anchor = 'center', height = 20, width = 85)
        self.update_pos()

if __name__ == '__main__':
    app = Khalifard()
    app.title("VSA_05370")
    app.geometry("228x322")
    app.minsize(228, 322)
    app.mainloop()