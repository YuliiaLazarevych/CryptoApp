import tkinter as tk
import tkinter.ttk as ttk
from ui.lab1_frame import Lab1Frame
from ui.lab2_frame import Lab2Frame
from ui.lab3_frame import Lab3Frame
from ui.lab4_frame import Lab4Frame  # Додаємо імпорт нової лаби


class CryptoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Захист інформації - Юлія")

        window_width = 750
        window_height = 600
        self.geometry(f"{window_width}x{window_height}")

        # Центрування вікна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"+{x}+{y}")

        self.configure(bg="#2b2b2b")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(self, bg="#2b2b2b")
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Додаємо Lab4Frame у список
        for F in (MainMenu, Lab1Frame, Lab2Frame, Lab3Frame, Lab4Frame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0)
            frame.grid_remove()

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2b2b2b")
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Головне меню", font=("Arial", 20, "bold"),
                 fg="white", bg="#2b2b2b").grid(row=1, column=0, pady=30)

        # Список кнопок для зручності
        labs = [
            ("Лабораторна №1: ГПВЧ", "Lab1Frame"),
            ("Лабораторна №2: MD5", "Lab2Frame"),
            ("Лабораторна №3: RC5", "Lab3Frame"),
            ("Лабораторна №4: RSA", "Lab4Frame")  # Нова кнопка
        ]

        for i, (text, target) in enumerate(labs, start=2):
            ttk.Button(self, text=text, width=35,
                       command=lambda t=target: controller.show_frame(t)).grid(row=i, column=0, pady=10)

        self.bind_all("<Control-v>", lambda event: self.handle_clipboard(event, "<<Paste>>"))
        self.bind_all("<Control-c>", lambda event: self.handle_clipboard(event, "<<Copy>>"))
        self.bind_all("<Control-a>", lambda event: self.handle_clipboard(event, "<<SelectAll>>"))

        def handle_clipboard(self, event, action):
            widget = self.focus_get()
            if isinstance(widget, (tk.Entry, tk.Text)):
                widget.event_generate(action)
            return "break"