from selection_interface import elevatorSettings
      
import enum
import sys
import selection_interface as si
import simulate_requests as sr
import queue
import time

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
        
    def moveElevator(self):
        if self._floorQueue.empty():
            self._floorQueue = self._nextFloorQueue
            if self._direction == self.Direction.UP:
                self._direction = self.Direction.DOWN
            else:
                self._direction = self.Direction.UP
            try:
                self._nextFloorQueue.clear()
            except AttributeError:
                print("Next Floor Queue is empty when reversing directions")
        next_floor = self._floorQueue.get()
        #This logic is incorrect
        if self._currentFloor < next_floor:
            floors_to_move = next_floor - self._currentFloor
        else:
            floors_to_move = self._currentFloor - next_floor
        if (floors_to_move == 0):
            return
        print(f"Current Floor: {self._currentFloor}, NextFloor: {next_floor}, Move: {floors_to_move}")
        traveltime = (floors_to_move * self._floorHeight)/self._maxSpeed
        time.sleep(traveltime)
        self._currentFloor = next_floor
        print(f"Arrived at Destination Floor {self._currentFloor}")
        print("FloorQueue: ")
        for floor in self._floorQueue.queue:
            print(floor)
        time.sleep(10)
        #Maybe check requests here to see if it should ignore generating another request
        
    def adjustFloorQueue(self):
        temp_list = [self._floorQueue.get() for _ in range(self._floorQueue.qsize())]
        unique_list = [floor for i, floor in enumerate(temp_list) if floor not in temp_list[:i]]
        if self._direction == self.Direction.UP:
            floors = [floor for floor in unique_list if floor >= self._currentFloor]
            floors.sort()
            nextfloors = [floor for floor in unique_list if floor < self._currentFloor]
        else:
            floors = [floor for floor in unique_list if floor <= self._currentFloor]
            floors.sort()
            floors.reverse()
            nextfloors = [floor for floor in unique_list if floor > self._currentFloor]
        self._floorQueue.queue.clear()
        for floor in floors:
            self._floorQueue.put(floor)
        for floor in nextfloors:
            self._nextFloorQueue.put(floor)
        
    def generateRequest(self):
        request = self.requestSimulator.generateRequest(self._currentFloor)
        print(request)
        request_direction = list(request.keys())
        request_floors = list(request.values())
        request_floors = request_floors[0]
        request_direction = self.Direction[request_direction[0].name]
        if self._direction is None:
            self._direction = request_direction
        if request_direction == self.Direction.UP:
            request_floors.sort()
        else:
            request_floors.sort()
            request_floors.reverse()
        for floor in request_floors:
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
        sim.generateRequest()
        sim.moveElevator()
    
    
        