import tkinter as tk
#This class is inheriting from canvas to allow custom buttons to be drawn
class ElevatorButton(tk.Canvas):
    def __init__(self, parent, text='', command=None, radius=20, border_width=2, border_color='black', highlight_color='red', **kwargs):
        super().__init__(parent, width=2*radius, height=2*radius, **kwargs)
        self.text = text
        self.command = command
        self.radius = radius
        self.border_width = border_width
        self.border_color = border_color
        self.highlight_color = highlight_color
        self.draw_button()
        
    #This draws a black circle on the canvas and adds floor text to it.
    def draw_button(self):
        self.delete('all')
        self.circleID = self.create_oval(self.border_width, self.border_width, 
                                         2*self.radius-self.border_width, 
                                         2*self.radius-self.border_width, 
                                         width=self.border_width)
        self.itemconfigure(self.circleID, fill="#D4D4D4")
        self.textID = self.create_text(self.radius, self.radius, text=self.text)
	#defines behavior when a button is clicked
        self.bind('<Button-1>', self.on_click)
        
    #Changes button to selected red like in real life elevators and calls the command
    #assigned to it.
    def on_click(self, event):
        self.itemconfigure(self.circleID, outline='red')
        self.itemconfigure(self.textID, fill='red')
        if self.command:
            self.command()
    #This simulates a click when running the simulators
    def sim_click(self):
        self.itemconfigure(self.circleID, outline='red')
        self.itemconfigure(self.textID, fill='red')
    #This resets the color of the button when the floor has been reached
    def resetButton(self):
        self.itemconfigure(self.circleID, outline='black')
        self.itemconfigure(self.textID, fill='black')
