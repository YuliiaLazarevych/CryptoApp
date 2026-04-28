import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import time
import os
from logic.rc5 import RC5
from ui.base_frame import BaseLabFrame


class Lab3Frame(BaseLabFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2b2b2b")

        tk.Label(self, text="Лабораторна №3: RC5", font=("Arial", 16, "bold"),
                 fg="white", bg="#2b2b2b").pack(pady=10)

        pass_frame = tk.LabelFrame(self, text=" Авторизація (MD5 Ключ) ", fg="#3a7ebf", bg="#2b2b2b", padx=10, pady=5)
        pass_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(pass_frame, text="Парольна фраза:", fg="white", bg="#2b2b2b").pack(side="left")
        self.password_entry = tk.Entry(pass_frame, font=("Arial", 11), show="*", bg="#1e1e1e", fg="#d4d4d4",
                                       insertbackground="white", width=35)
        self.password_entry.insert(0, "yulia_secret")
        self.password_entry.pack(side="left", padx=10, fill="x", expand=True)

        file_btn_row = tk.Frame(self, bg="#2b2b2b")
        file_btn_row.pack(fill="x", padx=15, pady=5)

        ttk.Button(file_btn_row, text="Зашифрувати файл", command=self.encrypt_file_action).pack(side="left", padx=5,
                                                                                                 expand=True, fill="x")
        ttk.Button(file_btn_row, text="Розшифрувати файл", command=self.decrypt_file_action).pack(side="left", padx=5,
                                                                                                  expand=True, fill="x")

        tk.Label(self, text="Вхідні дані (Текст для шифрування або Hex для дешифрування):", fg="white",
                 bg="#2b2b2b").pack(anchor="w", padx=20)
        self.input_text = tk.Text(self, height=5, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4",
                                  insertbackground="white", padx=10, pady=10)
        self.input_text.pack(pady=5, padx=20, fill="x")

        btn_row = tk.Frame(self, bg="#2b2b2b")
        btn_row.pack(fill="x", padx=15, pady=10)

        ttk.Button(btn_row, text="Шифрувати текст", command=self.encrypt_text_action).pack(side="left", padx=5,
                                                                                               expand=True, fill="x")
        ttk.Button(btn_row, text="Розшифрувати Hex", command=self.decrypt_text_action).pack(side="left", padx=5,
                                                                                                expand=True, fill="x")
        ttk.Button(btn_row, text="Очистити", command=self.clear_res).pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(btn_row, text="Тест", command=self.run_self_test).pack(side="left", padx=5, expand=True, fill="x")

        self.result_area = tk.Text(self, height=10, font=("Consolas", 10), bg="#1e1e1e", fg="#4EC9B0", padx=10, pady=10)
        self.result_area.pack(pady=5, padx=20, fill="both", expand=True)

        ttk.Button(self, text="Назад до меню", command=lambda: controller.show_frame("MainMenu")).pack(pady=10)

        self.setup_context_menu(self.input_text, self.result_area, self.password_entry)

    def encrypt_text_action(self):
        try:
            password = self.password_entry.get()
            if not password: return messagebox.showwarning("!", "Введіть пароль")

            data = self.input_text.get("1.0", tk.END).strip().encode('utf-8')
            if not data: return

            cipher = RC5(password)
            iv = b"TEST"

            start = time.perf_counter()
            encrypted = cipher.process_cbc(data, iv, encrypt=True)
            end = time.perf_counter()

            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END,
                                    f"RC5 Encryption (CBC)\nHex: {encrypted.hex()}\n\nЧас: {end - start:.6f} сек.")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def decrypt_text_action(self):
        try:
            password = self.password_entry.get()
            hex_data = self.input_text.get("1.0", tk.END).strip()
            if not hex_data: return

            cipher = RC5(password)
            iv = b"TEST"

            start = time.perf_counter()
            decrypted = cipher.process_cbc(bytes.fromhex(hex_data), iv, encrypt=False)
            end = time.perf_counter()

            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END,
                                    f"RC5 Decryption (CBC)\nТекст: {decrypted.decode('utf-8', errors='replace')}\n\nЧас: {end - start:.6f} сек.")
        except Exception as e:
            messagebox.showerror("Помилка", "Невірний Hex-код або пароль")

    def encrypt_file_action(self):
        password = self.password_entry.get()
        if not password: return messagebox.showwarning("!", "Введіть пароль")

        file_path = filedialog.askopenfilename()
        if not file_path: return

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            cipher = RC5(password)
            start = time.perf_counter()
            encrypted = cipher.encrypt_file(data)
            end = time.perf_counter()

            save_path = filedialog.asksaveasfilename(defaultextension=".rc5")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(encrypted)

                self.result_area.delete(1.0, tk.END)
                self.result_area.insert(tk.END,
                                        f"ФАЙЛ ЗАШИФРОВАНО\nШлях: {os.path.basename(save_path)}\nЧас: {end - start:.6f} сек.")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def decrypt_file_action(self):
        password = self.password_entry.get()
        if not password: return messagebox.showwarning("!", "Введіть пароль")

        file_path = filedialog.askopenfilename(filetypes=[("RC5 files", "*.rc5")])
        if not file_path: return

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            cipher = RC5(password)
            start = time.perf_counter()
            decrypted = cipher.decrypt_file(data)
            end = time.perf_counter()

            save_path = filedialog.asksaveasfilename()
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(decrypted)

                self.result_area.delete(1.0, tk.END)
                self.result_area.insert(tk.END, f"ФАЙЛ РОЗШИФРОВАНО\nЧас: {end - start:.6f} сек.")
        except Exception as e:
            messagebox.showerror("Помилка", "Помилка дешифрування!")

    def run_self_test(self):
        try:
            password = self.password_entry.get()
            cipher = RC5(password)
            msg = b"Hello World! Its RC5 test."
            iv = b"TEST"

            enc = cipher.process_cbc(msg, iv, encrypt=True)
            dec = cipher.process_cbc(enc, iv, encrypt=False)

            res = "OK" if msg == dec else "FAIL"
            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, f"SELF-TEST: {res}\nOriginal: {msg}\nDecrypted: {dec}")
        except Exception as e:
            messagebox.showerror("Тест", str(e))

    def clear_res(self):
        self.input_text.delete("1.0", tk.END)
        self.result_area.delete(1.0, tk.END)