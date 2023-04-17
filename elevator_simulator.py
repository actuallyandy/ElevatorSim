import enum

import simulate_requests as sr
import queue
import time


class ElevatorSimulator:
    #Constant to calculate travel time
    _floorHeight = 3.28 #meters
    #program default
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
        STATIONARY = 3 #Not Implemented
    _direction = None
    #Constants provided by settings selector
    _maxSpeed = 0
    _maxWeight = 0
    _maxFloor = 0
    _minFloor = 0
    #Constructor initializing private vars from settings selector
    def __init__(self, abovefloors, belowfloors, weightLimit, speedLimit):
        self._maxFloor = abovefloors
        self._minFloor = belowfloors
        self._maxWeight = weightLimit
        self._maxSpeed = speedLimit
        self._floorQueue = queue.Queue()
        self._nextFloorQueue = queue.Queue()
    #Prints a string with an increasing number of dots to provide "Animation"
    def animate_sleep(self, time_interval, msg):
        time_delta = time_interval/10
        for i in range(10):
            print(f"\r{msg}{'.'*(i+1)}", end="")
            time.sleep(time_delta)    
    #Same function as above but changes time based on the number of floors the elevator travels
    def animate_sleep_floors(self, time_interval, msg, floors):
        dots = floors * 3
        time_delta = time_interval/dots
        for i in range(dots):
            print(f"\r{msg}{'.'*(i+1)}", end="")
            time.sleep(time_delta)
    """
    Main Logic for Moving Elevator:
    -	First it checks if the floorQueue for the given directions is empty
    -	Next if the floorQueue for the opposite direction is empty it returns
    -	So, if the floorQueue for the current direction is empty but not the opposite direction,
    	it will pull values for the next direction into the current direction
    -	Next, the elevator will switch directions and try to clear the opposite floor direction
    -	If the error is caught then the program successfully swapped the Queues.
    
     	The second part of the logic:
    -	The next floor will be acquired from the floorQueue and the elevator will calculate how far it has to move
    - 	It will calculate a REAL travel time based on real-life estimates and elevator settings
    -	It will call the animate sleep function to simulate elevator travel time
    -	The current floor will be set and the application's queue will be filled with the new floor
    """        
    def moveElevator(self, externalQueue):
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
        externalQueue.put(self._currentFloor)
    #Function provides elevator information and simulates the elevator waiting for people to board
    #before it closes
    def arrivedElevator(self):
        print(f"\nArrived at Destination Floor {self._currentFloor}")
        print("FloorQueue: ", end="")
        for floor in self._floorQueue.queue:
            print(floor, end=' ')
        print("\n")
        self.animate_sleep(10, "Door Closing")
        print("\n")
    
    """
    Main logic for handling random floor requests:
    -	First the function will take the queues and pull them into unique lists since the 
    	request generator will generate floors that have been already requested and are out of order
    -	It will then check the direction and do the following:
    	-	If the elevator is going up than the next floors it has to visit are in order {1,2,3}
    		and the order of the floors in the opposite direction is reversed {-1,-2,-3}
    	-	If the elevator is going down, then the logic is opposite to the previous statement
    -	The queues are cleared and the correct lists are added back to the queues
    """
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
    """
    Main Logic for Generating Floor Requests:
    -	First the request is generated and the information is extracted properly
    -   Then it checks the requested floors list and ensures they are in the proper
    	order: {1,2,3} or {-1,-2,-3}
    - 	It sets the direction on the first pass
    -	Then it places each requested floor in the external queue which the GUI will handle
    -	Then it places each floor in the appropriate queue:
    	-	If we are going up and the floor is above, put it into the current queue
    		Otherwise, put it in the opposite direction queue
    	-	If we are going down and the floor is below, put it into the current queue
    		Otherwise, put it into the opposite direction queue
    -	Then it calls the adjustFloorsQueue function to ensure the queues are ordered properly.
    	Sometimes the queues would get mangled when the elevator swapped directions.
    """     
    def generateRequest(self, externalQueue):
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
            externalQueue.put(floor)
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
    
    def initializeSimulator(self):
        self.requestSimulator = sr.requestSimulator(self._maxFloor, self._minFloor)
        
        

        
    
    
    
    
        
