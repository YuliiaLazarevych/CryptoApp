import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
from logic.md5 import MD5
from ui.base_frame import BaseLabFrame


class Lab2Frame(BaseLabFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2b2b2b")
        self.md5 = MD5()

        tk.Label(self, text="Лабораторна №2: MD5", font=("Arial", 16, "bold"),
                 fg="white", bg="#2b2b2b").pack(pady=10)

        input_frame = tk.Frame(self, bg="#2b2b2b")
        input_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(input_frame, text="Рядок для хешування:", fg="white", bg="#2b2b2b").pack(side="left")
        self.input_text = tk.Entry(self, font=("Arial", 11), width=50)
        self.input_text.pack(pady=5)

        btn_row = tk.Frame(self, bg="#2b2b2b")
        btn_row.pack(fill="x", padx=15, pady=15)

        btns = [
            ("Хеш рядка", self.hash_input_string),
            ("Хеш файлу", self.hash_file_dialog),
            ("Перевірити файл", self.verify_file),
            ("Тест", self.run_full_test),
            ("Очистити", self.clear_res),
            ("Зберегти у файл", self.save_to_file)
        ]

        # поле для очікуваного хешу
        expect_frame = tk.LabelFrame(self, text=" Перевірка цілісності ", fg="#3a7ebf", bg="#2b2b2b", padx=10, pady=5)
        expect_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(expect_frame, text="Вставте очікуваний MD5:", fg="white", bg="#2b2b2b").pack(side="left")

        self.expected_hash_entry = tk.Entry(expect_frame, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4",
                                            insertbackground="white")
        self.expected_hash_entry.pack(side="left", fill="x", expand=True, padx=10)

        for text, cmd in btns:
            btn = ttk.Button(btn_row, text=text, command=cmd)
            btn.pack(side="left", padx=2, fill="x", expand=True)

        # поле результатів
        self.result_area = tk.Text(self, height=14, font=("Consolas", 10),
                                   bg="#1e1e1e", fg="#4EC9B0", padx=10, pady=10)
        self.result_area.pack(pady=5, padx=20, fill="both", expand=True)

        ttk.Button(self, text="Назад до меню",
                   command=lambda: controller.show_frame("MainMenu")).pack(pady=10)

    def hash_input_string(self):
        text = self.input_text.get()
        res = self.md5.hash_string(text)
        self.display_result(f"Input: '{text}'\nMD5: {res}")

    def hash_file_dialog(self):
        path = filedialog.askopenfilename()
        if path:
            try:
                with open(path, "rb") as f:
                    res = self.md5.hash_bytes(f.read())
                self.display_result(f"File: {path.split('/')[-1]}\nMD5: {res}")
            except Exception as e:
                messagebox.showerror("Помилка", str(e))

    def verify_file(self):
        path = filedialog.askopenfilename(title="Виберіть файл для перевірки")

        expected = self.expected_hash_entry.get().strip()

        if not expected:
            messagebox.showwarning("Увага", "Спочатку вставте очікуваний хеш у поле!")
            return

        if path:
            try:
                with open(path, "rb") as f:
                    # обчислюємо реальний хеш файлу
                    actual = self.md5.hash_bytes(f.read())

                if actual.upper() == expected.upper():
                    res_text = f"УСПІХ: Хеші збігаються!\nФайл: {path.split('/')[-1]}\nХеш: {actual}"
                    messagebox.showinfo("Цілісність підтверджена", "Файл цілий, змін не виявлено.")
                else:
                    res_text = f"ПОМИЛКА: Хеші не збігаються!\nФайл: {path.split('/')[-1]}\nОчікували: {expected}\nОтримали: {actual}"
                    messagebox.showerror("Цілісність порушена", "Файл було змінено або пошкоджено!")

                self.display_result(res_text)
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося прочитати файл: {e}")

    def run_full_test(self):
        vectors = [
            ("", "D41D8CD98F00B204E9800998ECF8427E"),
            ("a", "0CC175B9C0F1B6A831C399E269772661"),
            ("abc", "900150983CD24FB0D6963F7D28E17F72"),
            ("message digest", "F96B697D7CB7938D525A2F31AAF161D0"),
            ("abcdefghijklmnopqrstuvwxyz", "C3FCD3D76192E4007DFB496CCA67E13B"),
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "D174AB98D277D9F5A5611C2C9F419D9F"),
            ("12345678901234567890123456789012345678901234567890123456789012345678901234567890",
             "57EDF4A22BE3C955AC49DA2E2107B67A")
        ]
        res_text = "=== Протокол тестування MD5 (RFC 1321) ===\n"
        for msg, exp in vectors:
            actual = self.md5.hash_string(msg)
            status = "OK" if actual == exp else "FAIL"
            display_m = f"H({msg})" if len(msg) < 15 else f"H({msg[:12]}...)"
            res_text += f"{display_m:<20} | {actual} | {status}\n"
        self.display_result(res_text)

    def clear_res(self):
        self.result_area.delete(1.0, tk.END)
        self.input_text.delete(0, tk.END)
        self.expected_hash_entry.delete(0, tk.END)

    def display_result(self, text):
        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, text)

    def save_to_file(self):
        # беремо контент із текстового поля
        content = self.result_area.get(1.0, tk.END).strip()

        if not content:
            messagebox.showwarning("Попередження", "Поле результатів порожнє. Немає чого зберігати!")
            return

        # діалог "Зберегти як..."
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="md5_report.txt",
            title="Зберегти результат хешування"
        )

        # якщо юзер не натиснув "Скасувати" (тобто file_path не порожній)
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Успіх", f"Файл успішно збережено за шляхом:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")

        self.setup_context_menu(self.n_entry, self.result_area)