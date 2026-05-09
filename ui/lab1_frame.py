import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from logic.lcg import LCGGenerator
from ui.base_frame import BaseLabFrame


class Lab1Frame(BaseLabFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2b2b2b")
        self.backend = LCGGenerator()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        tk.Label(self, text="Лабораторна №1: ГПВЧ", font=("Arial", 16, "bold"), fg="white", bg="#2b2b2b").grid(row=0,
                                                                                                                  column=0,
                                                                                                                  columnspan=2,
                                                                                                                  pady=20)

        tk.Label(self, text="Кількість чисел (N):", font=("Arial", 11), fg="white", bg="#2b2b2b").grid(row=1, column=0,
                                                                                                       sticky="e",
                                                                                                       padx=10)
        self.n_entry = tk.Entry(self, font=("Arial", 11), width=15)
        self.n_entry.insert(0, "1000")
        self.n_entry.grid(row=1, column=1, sticky="w", padx=10)

        ttk.Button(self, text="1. Генерувати послідовність", width=30, command=self.run_generation).grid(row=2,
                                                                                                         column=0,
                                                                                                         columnspan=2,
                                                                                                         pady=10)

        ttk.Button(self, text="2. Порівняльне тестування (π)", width=30, command=self.run_comparison).grid(row=3,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=10)

        self.result_area = tk.Text(self, height=15, width=55, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4")
        self.result_area.grid(row=4, column=0, columnspan=2, pady=10, padx=20)

        ttk.Button(self, text="Назад до меню", command=lambda: controller.show_frame("MainMenu")).grid(row=5,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          pady=15)

    def run_generation(self):
        try:
            n = int(self.n_entry.get())
            if n <= 0: raise ValueError

            sequence = self.backend.generate_sequence(n)
            p = self.backend.get_period_fast()

            res_text = f" РЕЗУЛЬТАТ ГЕНЕРАЦІЇ (N={n}) \n"
            res_text += f"Період: {p}\n"
            res_text += "\nПерші 50 чисел:\n"
            res_text += ", ".join(map(str, sequence[:50]))
            if n > 50: res_text += "..."

            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, res_text)

            with open("result_lab1.txt", "w", encoding="utf-8") as f:
                f.write(res_text + f"\n\nПовна послідовність:\n{sequence}")

            messagebox.showinfo("Успіх", "Послідовність згенерована та збережена у файл result_lab1")
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректне число N!")

    def run_comparison(self):
        try:
            import math
            n_values = [10, 100, 1000, 10000, 100000, 1000000]
            target_pi = math.pi

            report_for_screen = f"{'N':<10} | {'Err LCG':<12} | {'Err System':<12}\n"
            report_for_screen += "-" * 40 + "\n"

            file_details = ""

            for n in n_values:
                pi_l = self.backend.estimate_pi(n, "lcg")
                pi_s = self.backend.estimate_pi(n, "system")
                err_l = abs(pi_l - target_pi)
                err_s = abs(pi_s - target_pi)

                block = (
                    f"Оцінка π (LCG, n={n}):          {pi_l:.15f}\n"
                    f"Оцінка π (System random):      {pi_s:.15f}\n"
                    f"Еталонне π:                    {target_pi:.15f}\n"
                    f"Абсолютна похибка (LCG):       {err_l:.6f}\n"
                    f"Абсолютна похибка (System):    {err_s:.6f}\n"
                    f"{'-' * 45}\n"
                )
                file_details += block
                report_for_screen += f"{n:<10} | {err_l:.6f}     | {err_s:.6f}\n"

            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, report_for_screen + "\nПовний звіт збережено у файл!")

            with open("result_comparison.txt", "w", encoding="utf-8") as f:
                f.write("ДЕТАЛЬНИЙ ПОРІВНЯЛЬНИЙ ТЕСТ\n")
                f.write("==============================\n")
                f.write(file_details)

            messagebox.showinfo("Готово", "Порівняльний тест завершено!\nРезультати збережено у файл: result_comparison.txt")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

        self.setup_context_menu(self.n_entry, self.result_area)