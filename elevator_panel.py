#include audio here
#include floor indicators and warning messages
#include emergency procedures: power outages, elevator malfunctions, fire alarms
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
    _minFloors = 0
    _maxFloors = 1
    _currentFloor = 1
    _buttonDict = {}
    flag = True
    def __init__(self, simSettings):
        self.root = tk.Tk()
        self.root.title("Elevator")
        self._minFloors = simSettings.belowfloors
        self._maxFloors = simSettings.abovefloors
        width = self.root.winfo_width() + 220
        height = self.root.winfo_height() + (45 * math.ceil((self._maxFloors+self._minFloors)/2)) +120
        self.root.geometry(f"{width}x{height}")
        
        self._floorDisplay = FloorDisplay(self.root, width=150, height=100)
        self._floorDisplay.pack(padx=10, pady=10)
        self._floorDisplay.set_number(1)
        self.create_buttons()
        ##Start Simulator
        self.buttonQueue = queue.Queue()
        self.currentfloorQueue = queue.Queue()
        self._simID = threading.Thread(target=self.runSimulator, args=(simSettings, self.buttonQueue, self.currentfloorQueue))
        self._simID.start()
        self.root.mainloop()
    
    def getFloorText(self, num):
        if num < 0:
            return f"G{abs(num)}"
        else:
            return f"{num}"
    def orderButtonColumns(self, lowerBound, upperBound, iterator, parent):
        for i in range(lowerBound, upperBound, iterator):
            if i == 0:
                continue
            text = self.getFloorText(i)
            eb = ElevatorButton(parent=parent, text=text, command=lambda input_value=i: self.button_callback(input_value))
            eb.pack(side="bottom")
            self._buttonDict[i] = eb
        
    def twoColumns(self, panel_frame):
        left_frame = tk.Frame(panel_frame)
        left_frame.pack(side='left')
        right_frame = tk.Frame(panel_frame)
        right_frame.pack(side='right')
        self.orderButtonColumns(-self._minFloors, self._maxFloors+1, 2, left_frame)
        self.orderButtonColumns(-self._minFloors+1, self._maxFloors+1, 2, right_frame)
            
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
    
    def button_callback(self, floor):
        self._floorDisplay.set_number(floor)
        
        
    def bing_bong(self):
        pygame.init()
        sound = pygame.mixer.Sound('./sound_effects/bing_bong.mp3')
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(5)
        pygame.quit()
        
    def simulateButtonPress(self):
        while not self.buttonQueue.empty():
            buttonID = self.buttonQueue.get()
            button = self._buttonDict[buttonID]
            button.sim_click()
        
    def simulateMoveElevator(self):
        while not self.currentfloorQueue.empty():
            floorID = self.currentfloorQueue.get()
            self._floorDisplay.set_number(floorID)
            self._currentFloor = floorID
            button = self._buttonDict[floorID]
            button.resetButton()
            
    
    #### MAIN CODE
    def runSimulator(self, simSettings, buttonQueue, currentfloorQueue):
        sim = ElevatorSimulator(simSettings.abovefloors, simSettings.belowfloors,
                                simSettings.weightLimit, simSettings.speedLimit)
        sim.initializeSimulator()
        while True:
            #Coin flip that decides whether request is created
            if choice([True, False]):
                sim.generateRequest(buttonQueue)
            else:
                print("Elevator Waiting.")
                time.sleep(5) #Elevator Waiting
            self.simulateButtonPress()
            sim.moveElevator(currentfloorQueue)
            old_floor = self._currentFloor
            self.simulateMoveElevator()
            new_floor = self._currentFloor
            if old_floor != new_floor:
                t = threading.Thread(target=self.bing_bong())
                t.start()
                t.join()
            sim.arrivedElevator()
            
        
if __name__ == "__main__":
    print("Running Elevator Simulator")
    elevator_settings = si.elevatorSettings()
    simSettings = elevator_settings.selectedSettings
    if simSettings is None:
        sys.exit()
    elevator = ElevatorPanel(simSettings)
    threads = threading.enumerate()
    for thread in threads:
        if thread != threading.main_thread():
            thread.join()
    
    raise SystemExit
    