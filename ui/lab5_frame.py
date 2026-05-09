import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import time
import re
from logic.dsa import DSALogic
from ui.base_frame import BaseLabFrame

ERROR_TITLE = "Помилка"
SUCCESS_TITLE = "Успіх!"

class Lab5Frame(BaseLabFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2b2b2b")
        self.dsa_logic = DSALogic()
        self.private_key = None
        self.public_key = None

        tk.Label(self, text="Лабораторна №5: DSA", font=("Arial", 16, "bold"),
                 fg="white", bg="#2b2b2b").pack(pady=10)

        key_frame = tk.LabelFrame(self, text=" Керування ключами ", fg="#3a7ebf", bg="#2b2b2b", padx=10, pady=10)
        key_frame.pack(fill="x", padx=20, pady=5)

        ttk.Button(key_frame, text="Згенерувати ключі", command=self.gen_keys).pack(side="left", padx=5)
        ttk.Button(key_frame, text="Зберегти в PEM", command=self.save_keys).pack(side="left", padx=5)
        ttk.Button(key_frame, text="Завантажити ключі", command=self.load_keys).pack(side="left", padx=5)

        self.input_text = tk.Text(self, height=5, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4",
                                  insertbackground="white")
        self.input_text.pack(pady=5, padx=20, fill="x")
        self.input_text.insert("1.0", "Введіть текст для підпису тут...")

        btn_row = tk.Frame(self, bg="#2b2b2b")
        btn_row.pack(fill="x", padx=15, pady=5)

        ttk.Button(btn_row, text="Підписати текст", command=self.sign_text_action).pack(side="left", padx=5,
                                                                                        expand=True, fill="x")
        ttk.Button(btn_row, text="Перевірити текст", command=self.verify_text_action).pack(side="left", padx=5,
                                                                                           expand=True, fill="x")
        ttk.Button(btn_row, text="Підписати файл", command=self.sign_file_action).pack(side="left", padx=5, expand=True,
                                                                                       fill="x")
        ttk.Button(btn_row, text="Перевірити файл", command=self.verify_file_action).pack(side="left", padx=5,
                                                                                          expand=True, fill="x")

        clear_btn_row = tk.Frame(self, bg="#2b2b2b")
        clear_btn_row.pack(fill="x", padx=15, pady=5)
        ttk.Button(clear_btn_row, text="Очистити поля", command=self.clear_fields).pack(padx=5, expand=True, fill="x")

        self.result_area = tk.Text(self, height=10, font=("Consolas", 10), bg="#1e1e1e", fg="#4EC9B0", padx=10, pady=10)
        self.result_area.pack(pady=5, padx=20, fill="both", expand=True)

        ttk.Button(self, text="Назад до меню", command=lambda: controller.show_frame("MainMenu")).pack(pady=10)

        self.setup_context_menu(self.input_text, self.result_area)

    def clear_fields(self):
        self.input_text.delete("1.0", tk.END)
        self.result_area.delete("1.0", tk.END)

    def gen_keys(self):
        self.private_key, self.public_key = self.dsa_logic.generate_keys()
        messagebox.showinfo(SUCCESS_TITLE, "Ключі DSA-1024 згенеровано!")

    def save_keys(self):
        if not self.private_key: return messagebox.showwarning("!", "Спершу згенеруйте ключі")
        self.dsa_logic.save_keys(self.private_key, self.public_key)
        messagebox.showinfo(SUCCESS_TITLE, "Ключі збережено!")

    def load_keys(self):
        try:
            self.private_key = self.dsa_logic.load_private_key("dsa_private.pem")
            self.public_key = self.dsa_logic.load_public_key("dsa_public.pem")
            messagebox.showinfo(SUCCESS_TITLE, "Ключі завантажено!")
        except Exception:
            messagebox.showerror(ERROR_TITLE, "Не вдалося знайти файли ключів.")

    def sign_text_action(self):
        if not self.private_key: return messagebox.showwarning("!", "Потрібен приватний ключ!")
        try:
            data = self.input_text.get("1.0", tk.END).strip().encode('utf-8')
            if not data: return

            start = time.perf_counter()
            signature = self.dsa_logic.sign_data(self.private_key, data)
            end = time.perf_counter()

            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, f"Hex: \n{signature.hex()}\n\n")
            self.result_area.insert(tk.END, f"Час генерації: {end - start:.6f} сек.")
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, str(e))

    def verify_text_action(self):
        if not self.public_key: return messagebox.showwarning("!", "Потрібен відкритий ключ!")
        try:
            data = self.input_text.get("1.0", tk.END).strip().encode('utf-8')
            full_content = self.result_area.get("1.0", tk.END).strip()

            hex_match = re.search(r'[0-9a-fA-F]{40,}', full_content)
            if not hex_match:
                return messagebox.showerror(ERROR_TITLE, "Підпис у полі результату не знайдено!")

            sig_bytes = bytes.fromhex(hex_match.group(0))
            is_valid = self.dsa_logic.verify_signature(self.public_key, data, sig_bytes)

            if is_valid:
                res_msg = "УСПІШНО: Підпис дійсний.\n\nЦе означає:\n1. Авторство підтверджено.\n2. Дані цілісні (не змінювались)."
                messagebox.showinfo("Результат перевірки", res_msg)
            else:
                res_msg = "ПОМИЛКА: Підпис недійсний!\n\nМожливі причини:\n1. Текст було змінено.\n2. Використано інший ключ."
                messagebox.showerror("Результат перевірки", res_msg)

        except Exception as e:
            messagebox.showerror(ERROR_TITLE, f"Не вдалося перевірити: {e}")

    def sign_file_action(self):
        if not self.private_key: return
        p = filedialog.askopenfilename()
        if not p: return
        with open(p, "rb") as f:
            sig = self.dsa_logic.sign_data(self.private_key, f.read())
        sp = filedialog.asksaveasfilename(defaultextension=".sig")
        if sp:
            with open(sp, "w") as f: f.write(sig.hex())
            messagebox.showinfo(SUCCESS_TITLE, "Підпис файлу створено!")

    def verify_file_action(self):
        if not self.public_key: return
        fp = filedialog.askopenfilename(title="Файл")
        sp = filedialog.askopenfilename(title="Підпис (.sig)")
        if not fp or not sp: return
        with open(fp, "rb") as f:
            d = f.read()
        with open(sp, "r") as f:
            s = bytes.fromhex(f.read().strip())
        v = self.dsa_logic.verify_signature(self.public_key, d, s)
        msg = "ВЕРИФІКОВАНО: Файл справжній." if v else "КРИТИЧНО: Файл пошкоджено або підпис підроблено!"
        messagebox.showinfo("Файл-чек", msg)