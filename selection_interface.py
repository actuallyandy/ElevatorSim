import tkinter as tk
from tkinter import ttk
from collections import namedtuple
import enum

class elevatorSettings:
    class PrimaryType(enum.Enum):
        HYDRAULIC = 1
        TRACTION = 2
        MACHINE_ROOM_LESS = 3
        VACUUM = 4
        PNEUMATIC = 5
    class SecondaryType(enum.Enum):
        PASSENGER = 1
        FREIGHT = 2
    _settings = namedtuple("settings", ["abovefloors","belowfloors", "weightLimit", "speedLimit"])
    #Estimates for Floor Limits
    _floorLimit = {PrimaryType.HYDRAULIC:8, PrimaryType.TRACTION:100, 
                   PrimaryType.MACHINE_ROOM_LESS:100, PrimaryType.VACUUM:5, 
                   PrimaryType.PNEUMATIC:5}
    #Estimates for Weight Limits for Passenger and Freight Elevators
    _weightLimit = {PrimaryType.HYDRAULIC:{SecondaryType.PASSENGER:1500, SecondaryType.FREIGHT:4000},
                    PrimaryType.TRACTION:{SecondaryType.PASSENGER:2000, SecondaryType.FREIGHT:10000},
                    PrimaryType.MACHINE_ROOM_LESS:{SecondaryType.PASSENGER: 2000, SecondaryType.FREIGHT:10000},
                    PrimaryType.VACUUM:{SecondaryType.PASSENGER:450, SecondaryType.FREIGHT:750},
                    PrimaryType.PNEUMATIC:{SecondaryType.PASSENGER:450, SecondaryType.FREIGHT:1000}
                    }
    #Estimates for Speed limits for Passender and Freight Elevators. Units in m/s
    _speedLimit =  {PrimaryType.HYDRAULIC:{SecondaryType.PASSENGER:0.2, SecondaryType.FREIGHT:0.6},
                    PrimaryType.TRACTION:{SecondaryType.PASSENGER:1, SecondaryType.FREIGHT:3},
                    PrimaryType.MACHINE_ROOM_LESS:{SecondaryType.PASSENGER: 1, SecondaryType.FREIGHT:3},
                    PrimaryType.VACUUM:{SecondaryType.PASSENGER:5, SecondaryType.FREIGHT:7},
                    PrimaryType.PNEUMATIC:{SecondaryType.PASSENGER:7, SecondaryType.FREIGHT:7}
                    }
    _selectedPrimaryType = None
    _selectedSecondaryType = None
    _maxFloors = 8 #default value
    selectedSettings = None
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Elevator Settings")
        self.root.geometry("250x250") # set the window size

        # create a label for the first dropdown
        label1 = ttk.Label(self.root, text="Elevator Type:")
        label1.pack()

        # create the first dropdown thats the elevator type (not editable)
        type_options = [primarytype.name for primarytype in self.PrimaryType]
        self.ptype_var = tk.StringVar()
        self.ptype_dropdown = ttk.Combobox(self.root, textvariable=self.ptype_var, values=type_options)
        self.ptype_dropdown.current(0) # set the default value
        self.ptype_dropdown.pack()
        self.ptype_dropdown.config(state="readonly")

        # create a label for the second dropdown
        label2 = ttk.Label(self.root, text="Cargo Type:")
        label2.pack()

        # create the second dropdown thats cargo type (not editable)
        type_options = [secondarytype.name for secondarytype in self.SecondaryType]
        self.stype_var = tk.StringVar()
        self.stype_dropdown = ttk.Combobox(self.root, textvariable=self.stype_var, values=type_options)
        self.stype_dropdown.current(0) # set the default value
        self.stype_dropdown.pack()
        self.stype_dropdown.config(state="readonly")

        #Create Validation function to ensure only numeric input into field
        def validate_numeric(new_value):
            if new_value == '':
                return True
            try:
                if (len(new_value) > 3):
                    return False
                int(new_value)
                return True
            except ValueError:
                return False
        validate_cmd = self.root.register(validate_numeric)

        #Create above floor label. Prevent non-numeric input and set default
        above_label = ttk.Label(self.root, text="Number of above-ground floors:")
        above_label.pack(pady=5)
        self.above_entry = ttk.Entry(self.root, validate='key', 
                                     validatecommand=(self.root.register(validate_numeric), '%P'))
        self.above_entry.pack(pady=5)
        self.above_entry.insert(0,'1')
            
        #Create below floor label. Prevent non-numeric input and set default
        underground_label = ttk.Label(self.root, text="Number of underground floors:")
        underground_label.pack(pady=5)
        self.underground_entry = ttk.Entry(self.root, validate='key', 
                                           validatecommand=(self.root.register(validate_numeric), '%P'))
        self.underground_entry.pack(pady=5)
        self.underground_entry.insert(0,'0')
        
        #Create label to inform users of Max floors for elevator type.
        _maxFloors = "Max Number of Floors: " + str(self._floorLimit[self.PrimaryType[self.ptype_dropdown.get()]])
        _maxFloors_label = ttk.Label(self.root, text=_maxFloors)
        _maxFloors_label.pack()


        # create the frame for the buttons
        button_frame = ttk.Frame(self.root)

        # create the "Okay" button and pack it to the left
        okay_button = ttk.Button(button_frame, text="Okay", command=self.okay)
        okay_button.pack(side="left", padx=5, pady=5)

        # create the "Cancel" button and pack it to the left
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side="left", padx=5, pady=5)

        # pack the button frame to the bottom of the window
        button_frame.pack(side="bottom", pady=10)
        
        #Function to update max floors label and update internal max floors value
        def on_type_changed(event):
            new_text = "Max Number of Floors: " + str(self._floorLimit[self.PrimaryType[self.ptype_dropdown.get()]])
            self._maxFloors = int(self._floorLimit[self.PrimaryType[self.ptype_dropdown.get()]])
            _maxFloors_label.config(text=new_text)
        #Calls above function when new selection is picked
        self.ptype_dropdown.bind("<<ComboboxSelected>>", on_type_changed)
        self.root.mainloop()
    
        
    #pulls values from app and stores them in a safe space
    def okay(self):
        self._selectedPrimaryType = self.ptype_dropdown.get()
        self._selectedSecondaryType = self.stype_dropdown.get()
        above_floors = int(self.above_entry.get())
        below_floors = int(self.underground_entry.get())
        total_floors = above_floors + below_floors
        if (total_floors > self._maxFloors):
            tk.messagebox.showwarning("Warning", "Total Number of Floors exceeds Elevator Type Limit!")
            return
        print(f"Type: {self._selectedPrimaryType}, Cargo: {self._selectedSecondaryType}, Floors: {total_floors}")
        weight_limit = self._weightLimit[self.PrimaryType[self._selectedPrimaryType]][self.SecondaryType[self._selectedSecondaryType]]
        speed_limit = self._speedLimit[self.PrimaryType[self._selectedPrimaryType]][self.SecondaryType[self._selectedSecondaryType]]
        self.selectedSettings = self._settings(above_floors, below_floors, weight_limit, speed_limit)
        self.root.destroy()
    #closes app
    def cancel(self):
        self.root.destroy()

if __name__ == "__main__":
    interface = elevatorSettings()
    
