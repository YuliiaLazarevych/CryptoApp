import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import time
import os
from logic.rsa import RSA
from logic.rc5 import RC5
from ui.base_frame import BaseLabFrame

ERROR_TITLE = "Помилка"

class Lab4Frame(BaseLabFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2b2b2b")
        self.rsa = RSA()
        self.private_key = None
        self.public_key = None

        tk.Label(self, text="Лабораторна №4: RSA", font=("Arial", 16, "bold"),
                 fg="white", bg="#2b2b2b").pack(pady=10)

        key_frame = tk.LabelFrame(self, text=" Керування ключами ", fg="#3a7ebf", bg="#2b2b2b", padx=10, pady=10)
        key_frame.pack(fill="x", padx=20, pady=5)

        ttk.Button(key_frame, text="Згенерувати ключі", command=self.gen_keys).pack(side="left", padx=5)
        ttk.Button(key_frame, text="Зберегти в PEM", command=self.save_keys).pack(side="left", padx=5)
        ttk.Button(key_frame, text="Завантажити ключі", command=self.load_keys).pack(side="left", padx=5)

        file_btn_row = tk.Frame(self, bg="#2b2b2b")
        file_btn_row.pack(fill="x", padx=15, pady=5)

        ttk.Button(file_btn_row, text="Зашифрувати файл", command=self.encrypt_file_action).pack(side="left", padx=5,
                                                                                                 expand=True, fill="x")
        ttk.Button(file_btn_row, text="Розшифрувати файл", command=self.decrypt_file_action).pack(side="left", padx=5,
                                                                                                  expand=True, fill="x")

        self.input_text = tk.Text(self, height=5, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4",
                                  insertbackground="white")
        self.input_text.pack(pady=5, padx=20, fill="x")
        self.input_text.insert("1.0", "Введіть текст для шифрування тут...")

        btn_row = tk.Frame(self, bg="#2b2b2b")
        btn_row.pack(fill="x", padx=15, pady=10)

        ttk.Button(btn_row, text="Шифрувати", command=self.rsa_encrypt).pack(side="left", padx=5, expand=True,
                                                                                 fill="x")
        ttk.Button(btn_row, text="Розшифрувати", command=self.rsa_decrypt).pack(side="left", padx=5, expand=True,
                                                                                    fill="x")
        ttk.Button(btn_row, text="Очистити", command=self.clear_res).pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(btn_row, text="Порівняти з RC5", command=self.compare_speed).pack(side="left", padx=5, expand=True,
                                                                                     fill="x")

        self.result_area = tk.Text(self, height=10, font=("Consolas", 10), bg="#1e1e1e", fg="#4EC9B0", padx=10, pady=10)
        self.result_area.pack(pady=5, padx=20, fill="both", expand=True)

        ttk.Button(self, text="Назад до меню", command=lambda: controller.show_frame("MainMenu")).pack(pady=10)

        self.setup_context_menu(self.input_text, self.result_area)

    def gen_keys(self):
        self.private_key, self.public_key = self.rsa.generate_keys()
        messagebox.showinfo("Успіх", "Ключі RSA-2048 згенеровано!")

    def save_keys(self):
        if not self.private_key: return messagebox.showwarning("!", "Спершу згенеруйте ключі")
        self.rsa.save_keys(self.private_key, self.public_key)
        messagebox.showinfo("Успіх", "Ключі збережено у файли rsa_private.pem та rsa_public.pem")

    def load_keys(self):
        try:
            self.private_key = self.rsa.load_private_key("rsa_private.pem")
            self.public_key = self.rsa.load_public_key("rsa_public.pem")
            messagebox.showinfo("Успіх", "Ключі завантажено!")
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, f"Не вдалося завантажити ключі: {e}")

    def rsa_encrypt(self):
        if not self.public_key: return messagebox.showwarning("!", "Завантажте або згенеруйте публічний ключ")
        try:
            data = self.input_text.get("1.0", tk.END).strip().encode()
            if not data: return

            start = time.perf_counter()
            encrypted = self.rsa.encrypt_data(self.public_key, data)
            end = time.perf_counter()

            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END,
                                    f"RSA Encryption\nHex: {encrypted.hex()}\n\nЧас: {end - start:.6f} сек.")
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, str(e))

    def rsa_decrypt(self):
        if not self.private_key: return messagebox.showwarning("!", "Завантажте приватний ключ")
        try:
            hex_data = self.input_text.get("1.0", tk.END).strip()
            encrypted_bytes = bytes.fromhex(hex_data)

            decrypted = self.rsa.decrypt_data(self.private_key, encrypted_bytes)
            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, f"RSA Decryption\nТекст: {decrypted.decode('utf-8')}")
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, f"Дешифрування неможливе: {e}")

    def clear_res(self):
        self.input_text.delete("1.0", tk.END)
        self.result_area.delete(1.0, tk.END)

    def compare_speed(self):
        try:
            test_data = os.urandom(51200)

            if not self.public_key:
                self.private_key, self.public_key = self.rsa.generate_keys()

            t1 = time.perf_counter()
            self.rsa.encrypt_data(self.public_key, test_data)
            rsa_time = time.perf_counter() - t1

            key_rc5 = "my_secret_key_16"
            iv_rc5 = b"INIT"
            cipher_rc5 = RC5(key_rc5)

            t2 = time.perf_counter()
            cipher_rc5.process_cbc(test_data, iv_rc5, encrypt=True)
            rc5_time = time.perf_counter() - t2

            if rsa_time > rc5_time:
                ratio = rsa_time / rc5_time
                res_text = f"RC5 швидше за RSA у {ratio:.2f} разів"
            else:
                ratio = rc5_time / rsa_time
                res_text = f"RSA швидше за RC5 у {ratio:.2f} разів"

            report = (
                f"ПОРІВНЯННЯ ШВИДКОДІЇ (50 КБ)\n\n"
                f"RSA-2048: {rsa_time:.6f} сек.\n"
                f"RC5-32/12/16: {rc5_time:.6f} сек.\n\n"
                f"Результат: {res_text}.\n\n"
                f"Примітка: RSA використовує системні C-бібліотеки,\n"
                f"тому на малих даних може випереджати RC5 на Python."
            )
            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, report)
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, f"Не вдалося порівняти: {e}")

    def encrypt_file_action(self):
        if not self.public_key:
            return messagebox.showwarning("!", "Спершу завантажте публічний ключ")

        file_path = filedialog.askopenfilename(title="Виберіть файл для шифрування")
        if not file_path: return

        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()

            start = time.perf_counter()
            encrypted_data = self.rsa.encrypt_data(self.public_key, raw_data)
            end = time.perf_counter()

            save_path = filedialog.asksaveasfilename(defaultextension=".rsa", title="Зберегти зашифрований файл")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(encrypted_data)

                self.result_area.delete(1.0, tk.END)
                self.result_area.insert(tk.END, f"ФАЙЛ ЗАШИФРОВАНО\nОригінал: {os.path.basename(file_path)}\n")
                self.result_area.insert(tk.END,
                                        f"Час роботи: {end - start:.6f} сек.\nРозмір: {len(encrypted_data)} байт")
                messagebox.showinfo("Успіх", "Файл успішно зашифровано!")
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, f"Не вдалося зашифрувати файл: {e}")

    def decrypt_file_action(self):
        if not self.private_key:
            return messagebox.showwarning("!", "Спершу завантажте приватний ключ")

        file_path = filedialog.askopenfilename(title="Виберіть .rsa файл для дешифрування")
        if not file_path: return

        try:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = self.rsa.decrypt_data(self.private_key, encrypted_data)

            save_path = filedialog.asksaveasfilename(title="Зберегти розшифрований файл")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(decrypted_data)

                messagebox.showinfo("Успіх", "Файл успішно розшифровано!")
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, f"Дешифрування файлу неможливе: {e}")