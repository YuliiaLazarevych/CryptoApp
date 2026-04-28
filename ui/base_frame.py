import tkinter as tk

class BaseLabFrame(tk.Frame):
    def setup_context_menu(self, *widgets):
        for widget in widgets:
            widget.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Копіювати", command=lambda: self.focus_get().event_generate("<<Copy>>"))
        menu.add_command(label="Вставити", command=lambda: self.focus_get().event_generate("<<Paste>>"))
        menu.add_separator()
        menu.add_command(label="Виділити все", command=lambda: self.focus_get().event_generate("<<SelectAll>>"))
        menu.tk_popup(event.x_root, event.y_root)