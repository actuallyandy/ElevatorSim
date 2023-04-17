import tkinter as tk
import math
from FloorDisplay import FloorDisplay
from elevatorButton import ElevatorButton
import time
import pygame

from random import choice
import threading
import queue
import sys
import selection_interface as si
from elevator_simulator import ElevatorSimulator


class ElevatorPanel:
    #Setting defaults
    _minFloors = 0
    _maxFloors = 1
    _currentFloor = 1
    _buttonDict = {} #This dictionary contains the floor number and the button object
    flag = True
    def __init__(self, simSettings):
        self.root = tk.Tk()
        self.root.title("Elevator")
        #Pulls in the values selected from selection interface
        self._minFloors = simSettings.belowfloors
        self._maxFloors = simSettings.abovefloors
        #Psuedo dynamically sets the size of the GUI based on the number of buttons
        width = self.root.winfo_width() + 220
        height = self.root.winfo_height() + (45 * math.ceil((self._maxFloors+self._minFloors)/2)) +120
        self.root.geometry(f"{width}x{height}")
        #Sets the default size of the floor display to accomodate upto three digits
        self._floorDisplay = FloorDisplay(self.root, width=150, height=100)
        self._floorDisplay.pack(padx=10, pady=10)
        self._floorDisplay.set_number(1)
        self.create_buttons()
        ##Start Simulator
        self.buttonQueue = queue.Queue() #Queue to handle inter-thread requests
        self.currentfloorQueue = queue.Queue() #Queue to handle inter-thread floor reached
        self._simID = threading.Thread(target=self.runSimulator, args=(simSettings, self.buttonQueue, self.currentfloorQueue))
        self._simID.start()
        self.root.protocol("WM_DELETE_WINDOW", self.stop_threads) #Protocol to kill sim thread on Window close
        self.root.mainloop()
    
    #Returns string for floor value with appended G to the number if the floor is underground
    def getFloorText(self, num):
        if num < 0:
            return f"G{abs(num)}"
        else:
            return f"{num}"
    #Function that creates elevator buttons from bottom of parent frame to top and puts button in dictionary with  floor number
    def orderButtonColumns(self, lowerBound, upperBound, iterator, parent):
        for i in range(lowerBound, upperBound, iterator):
            if i == 0:
                continue
            text = self.getFloorText(i)
            eb = ElevatorButton(parent=parent, text=text, command=lambda input_value=i: self.button_callback(input_value))
            eb.pack(side="bottom")
            self._buttonDict[i] = eb
    #Creates two columns of buttons for small elevators 
    def twoColumns(self, panel_frame):
        left_frame = tk.Frame(panel_frame)
        left_frame.pack(side='left')
        right_frame = tk.Frame(panel_frame)
        right_frame.pack(side='right')
        self.orderButtonColumns(-self._minFloors, self._maxFloors+1, 2, left_frame)
        self.orderButtonColumns(-self._minFloors+1, self._maxFloors+1, 2, right_frame)
    #Creates three columns of buttons for medium sized elevators      
    def threeColumns(self, panel_frame):
        left_frame = tk.Frame(panel_frame)
        left_frame.grid(row=1, column=3)
        middle_frame = tk.Frame(panel_frame)
        middle_frame.grid(row=1, column=1)
        right_frame = tk.Frame(panel_frame)
        right_frame.grid(row=1, column=2)
        self.orderButtonColumns(-self._minFloors, self._maxFloors+1, 3, left_frame)
        self.orderButtonColumns(-self._minFloors+1, self._maxFloors+1, 3, middle_frame)
        self.orderButtonColumns(-self._minFloors+2, self._maxFloors+1, 3, right_frame)
    #Creates four columns of buttons for large elevators    
    def fourColumns(self, panel_frame):
        left_frame = tk.Frame(panel_frame)
        left_frame.grid(row=1, column=4)
        middle_frame1 = tk.Frame(panel_frame)
        middle_frame1.grid(row=1, column=1)
        middle_frame2 = tk.Frame(panel_frame)
        middle_frame2.grid(row=1, column=2)
        right_frame = tk.Frame(panel_frame)
        right_frame.grid(row=1, column=3)
        self.orderButtonColumns(-self._minFloors, self._maxFloors+1, 4, left_frame)
        self.orderButtonColumns(-self._minFloors+1, self._maxFloors+1, 4, middle_frame1)
        self.orderButtonColumns(-self._minFloors+2, self._maxFloors+1, 4, middle_frame2)
        self.orderButtonColumns(-self._minFloors+3, self._maxFloors+1, 4, right_frame)
    #Creates five columns of buttons for huge elevators    
    def fiveColumns(self, panel_frame):
        left_frame = tk.Frame(panel_frame)
        left_frame.grid(row=1, column=5)
        middle_frame1 = tk.Frame(panel_frame)
        middle_frame1.grid(row=1, column=1)
        middle_frame2 = tk.Frame(panel_frame)
        middle_frame2.grid(row=1, column=2)
        middle_frame3 = tk.Frame(panel_frame)
        middle_frame3.grid(row=1, column=3)
        right_frame = tk.Frame(panel_frame)
        right_frame.grid(row=1, column=4)
        self.orderButtonColumns(-self._minFloors, self._maxFloors+1, 5, left_frame)
        self.orderButtonColumns(-self._minFloors+1, self._maxFloors+1, 5, middle_frame1)
        self.orderButtonColumns(-self._minFloors+2, self._maxFloors+1, 5, middle_frame2)
        self.orderButtonColumns(-self._minFloors+3, self._maxFloors+1, 5, middle_frame3)
        self.orderButtonColumns(-self._minFloors+4, self._maxFloors+1, 5, right_frame)
    #Function that initialized button columns based on total amount of floors from settings    
    def create_buttons(self):
        panel_frame = tk.Frame(self.root)
        panel_frame.pack()
        total_floors = self._minFloors+self._maxFloors
        if  total_floors <= 40:
            self.twoColumns(panel_frame)
            return
        if total_floors <= 60:
            self.threeColumns(panel_frame)
            return
        if total_floors <= 80:
            self.fourColumns(panel_frame)
        if total_floors <= 100:
            self.fiveColumns(panel_frame)
    #NOT IMPLEMENTED
    def button_callback(self, floor):
        self._floorDisplay.set_number(floor)
        
    #Plays bing bong noise when floor is reached    
    def bing_bong(self):
        pygame.init()
        sound = pygame.mixer.Sound('./sound_effects/bing_bong.mp3')
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(5)
        pygame.quit()
    #Takes in request from inter-thread queue and highlights appropriate buttons    
    def simulateButtonPress(self):
        while not self.buttonQueue.empty():
            buttonID = self.buttonQueue.get()
            button = self._buttonDict[buttonID]
            button.sim_click()
    #Takes in current floor from inter-thread cue since the simulator handles the logic
    def simulateMoveElevator(self):
        while not self.currentfloorQueue.empty():
            floorID = self.currentfloorQueue.get()
            self._floorDisplay.set_number(floorID)
            self._currentFloor = floorID
            button = self._buttonDict[floorID]
            button.resetButton()
    #Stops the background sim thread. Only works sometimes...        
    def stop_threads(self):
        #print("\nTrying to stop thread")
        self._simID.do_run = False
        self.root.destroy()
    #### MAIN CODE ####
    def runSimulator(self, simSettings, buttonQueue, currentfloorQueue):
        #Creates and builds simulator
        sim = ElevatorSimulator(simSettings.abovefloors, simSettings.belowfloors,
                                simSettings.weightLimit, simSettings.speedLimit)
        sim.initializeSimulator()
        while True:
            #Coin flip that decides whether request is created
            if choice([True, False]):
                #Generates request of people who get on elevator on the current floor
                sim.generateRequest(buttonQueue)
            else:
                #Elevator is "waiting for input"
                print("Elevator Waiting.")
                time.sleep(5) #Elevator Waiting
            #simulates the buttons being pressed if people were on the elevator
            self.simulateButtonPress()
            #runs main logic of sim to move elevator
            sim.moveElevator(currentfloorQueue)
            old_floor = self._currentFloor
            #updates the GUI to reflect change in elevator position
            self.simulateMoveElevator()
            new_floor = self._currentFloor
            #checks to see if elevator has moved before it issues bing-bong
            if old_floor != new_floor:
                t = threading.Thread(target=self.bing_bong())
                t.start()
                t.join()
            #Prints information regarding elevator arrival
            sim.arrivedElevator()
            
        
if __name__ == "__main__":
    print("Running Elevator Simulator")
    #starts settings GUI
    elevator_settings = si.elevatorSettings()
    simSettings = elevator_settings.selectedSettings
    if simSettings is None:
        sys.exit()
    #starts elevator GUI
    elevator = ElevatorPanel(simSettings)
    
    raise SystemExit
    
