import tkinter as tk
import time
#Draws a black box with an input number displayed. It can be updated with set_number method. 
#Also changes negative numbers to G: -1 -> G1
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
