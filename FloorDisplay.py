import tkinter as tk
import time
class FloorDisplay(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="black", **kwargs)
        self.number = None
        self.text_id = None
        self.draw()
    def draw(self):
        self.delete("all")
        if self.number is not None:
            if self.number < 0:
                text = f"G{abs(self.number)}"
            else:
                text = str(self.number)
            self.text_id = self.create_text(76,51, text=text, fill="red", font=("Arial", 80))
    def set_number(self, number):
        self.number = number
        self.draw()