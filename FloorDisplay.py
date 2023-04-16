import tkinter as tk

class FloorDisplay(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="black", **kwargs)
        self.number = None
        self.text_id = None
        self.draw()
    def draw(self):
        self.delete("all")
        if self.number is not None:
            text = str(self.number)
            x = self.winfo_width()
            y = self.winfo_width()
            self.text_id = self.create_text(x+50,y+50, text=text, fill="red", font=("Arial", 80))
    def set_number(self, number):
        self.number = number
        self.draw()