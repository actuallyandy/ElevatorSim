from selection_interface import elevatorSettings
      
import enum
import sys
import selection_interface as si
import simulate_requests as sr
import queue
import time
from random import choice
from copy import deepcopy

class ElevatorSimulator:
    _floorHeight = 3.28 #meters
    _currentFloor = 1
    class DoorStatus(enum.Enum):
        OPEN = 1
        CLOSED = 2
    _DoorStatus = DoorStatus.OPEN
    
    _floorQueue = None
    _nextFloorQueue = None
    class Direction(enum.Enum):
        UP = 1
        DOWN = 2
        STATIONARY = 3
    _direction = None
    _maxSpeed = 0
    _maxWeight = 0
    _maxFloor = 0
    _minFloor = 0
    
    def __init__(self, abovefloors, belowfloors, weightLimit, speedLimit):
        self._maxFloor = abovefloors
        self._minFloor = belowfloors
        self._maxWeight = weightLimit
        self._maxSpeed = speedLimit
        self._floorQueue = queue.Queue()
        self._nextFloorQueue = queue.Queue()
        ## BUILD PANEL HERE
    
    def animate_sleep(self, time_interval, msg):
        time_delta = time_interval/10
        for i in range(10):
            print(f"\r{msg}{'.'*(i+1)}", end="")
            time.sleep(time_delta)    
    
    def animate_sleep_floors(self, time_interval, msg, floors):
        dots = floors * 3
        time_delta = time_interval/dots
        for i in range(dots):
            print(f"\r{msg}{'.'*(i+1)}", end="")
            time.sleep(time_delta)
        
    def moveElevator(self):
        if self._floorQueue.empty():
            if self._nextFloorQueue.empty():
                return
            while not self._nextFloorQueue.empty():
                floor = self._nextFloorQueue.get()
                self._floorQueue.put(floor)
            if self._direction == self.Direction.UP:
                self._direction = self.Direction.DOWN
            else:
                self._direction = self.Direction.UP
            try:
                self._nextFloorQueue.clear()
            except AttributeError:
                print("Next Floor Queue is empty when reversing directions")
        
        next_floor = self._floorQueue.get()
        if self._currentFloor < next_floor:
            floors_to_move = next_floor - self._currentFloor
        else:
            floors_to_move = self._currentFloor - next_floor
        if (floors_to_move == 0):
            return
        print(f"Current Floor: {self._currentFloor}, NextFloor: {next_floor}, Move: {floors_to_move}")
        traveltime = (floors_to_move * self._floorHeight)/self._maxSpeed
        self.animate_sleep_floors(traveltime, "Moving", floors=floors_to_move)
        #print("Moving...")
        #time.sleep(traveltime)
        self._currentFloor = next_floor
        print(f"\nArrived at Destination Floor {self._currentFloor}")
        print("FloorQueue: ", end="")
        for floor in self._floorQueue.queue:
            print(floor, end=' ')
        print("\n")
        self.animate_sleep(10, "Door Closing")
        print("\n")
        
        #Maybe check requests here to see if it should ignore generating another request
        
    def adjustFloorQueue(self):
        temp_list = [self._floorQueue.get() for _ in range(self._floorQueue.qsize())]
        temp_next_list = [self._nextFloorQueue.get() for _ in range(self._nextFloorQueue.qsize())]
        unique_list = [floor for i, floor in enumerate(temp_list) if floor not in temp_list[:i]]
        unique_next_list = [floor for i, floor in enumerate(temp_next_list) if floor not in temp_next_list[:i]]
        #print(f"Unique Floor list: {unique_list}\nUnique Next-Floor list: {unique_next_list}")
        if self._direction == self.Direction.UP:
            unique_list.sort()
            unique_next_list.sort()
            unique_next_list.reverse()
        else: #DOWN
            unique_list.sort()
            unique_list.reverse()
            unique_next_list.sort()
        self._floorQueue.queue.clear()
        self._nextFloorQueue.queue.clear()
        for floor in unique_list:
            self._floorQueue.put(floor)
        for floor in unique_next_list:
            self._nextFloorQueue.put(floor)
        
    def generateRequest(self):
        request = self.requestSimulator.generateRequest(self._currentFloor)
        request_direction = list(request.keys())
        request_floors = list(request.values())
        request_floors = request_floors[0]
        request_direction = self.Direction[request_direction[0].name]
        print(f"Generating New Request: Direction | {request_direction}, Floors | {request_floors}")
        if request_direction == self.Direction.UP:
            request_floors.sort()
        else:
            request_floors.sort()
            request_floors.reverse()
        if self._direction is None:
            print(f"Elevator is stationary. Moving: {request_direction}")
            self._direction = request_direction
        
        for floor in request_floors:
            if self._direction == self.Direction.UP:
                #print("Going Up!")
                if floor < self._currentFloor:
                    #print(f"Floor {floor} placed in next queue")
                    self._nextFloorQueue.put(floor)
                else:
                    #print(f"Floor {floor} placed in current queue")
                    self._floorQueue.put(floor)
            else: #if elevator is going down
                #print("Going Down!")
                if floor > self._currentFloor:
                    #print(f"Floor {floor} placed in next queue")
                    self._nextFloorQueue.put(floor)
                else:
                    #print(f"Floor {floor} placed in current queue")
                    self._floorQueue.put(floor)
        self.adjustFloorQueue()
    
    def initializeRequestSimulator(self):
        self.requestSimulator = sr.requestSimulator(self._maxFloor, self._minFloor)
        
        
        
if __name__ == "__main__":
    print("Running Elevator Simulator")
    elevator_settings = si.elevatorSettings()
    simSettings = elevator_settings.selectedSettings
    if simSettings is None:
        sys.exit()
    sim = ElevatorSimulator(simSettings.abovefloors, simSettings.belowfloors,
                            simSettings.weightLimit, simSettings.speedLimit)
    sim.initializeRequestSimulator()
    while True:
        #Coin flip that decides whether request is created
        if choice([True, False]):
            sim.generateRequest()
        else:
            print("Elevator Waiting.")
            time.sleep(5) #Elevator Waiting
        sim.moveElevator()
    
    
        