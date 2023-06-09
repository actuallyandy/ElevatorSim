import random as rand
import math as m
import enum

class requestSimulator:
    """
    Requests are designed as follows:
        1. Outerlayer is Direction and Innerlayer is array of floors
        Example: {u: [2,4,10]}
        Maximum number of requests that can be made are the total number of floors
        For example if the max floors are 4 floors + 1 underground floor then the
        total request will be: {u: [-1,1,2,3,4]}
    """
    _maxFloor = 0
    _minFloor = 0
    def __init__(self, maxFloor, minFloor):
        self._maxFloor = maxFloor
        self._minFloor = minFloor
        
    class Direction(enum.Enum):
        UP = 1
        DOWN = 2
    #Prevents invalid direction requests being generated if on the top or bottom floor.
    #Can't go down if theres nowhere to go
    def _generateDirectionRequest(self, currentFloor):
        if currentFloor == self._maxFloor:
            return self.Direction.DOWN
        if currentFloor == self._minFloor:
            return self.Direction.UP
        options = (self.Direction.DOWN, self.Direction.UP)
        return rand.choice(options)
        
    #Function checkes the number of available floors in current direction. Creates low biased number
    #of requests. That is if there are twenty floors, it will generate 5 floors more often than 20
    def _generateNumberofFloorRequests(self, direction, currentFloor, minFloor, maxFloor):
        if direction == self.Direction.UP:
            avail_floors = [i for i in range(currentFloor, maxFloor) if i!=0]
        else:
            avail_floors = [i for i in range(-1*minFloor, currentFloor) if i!=0]
        num_avail_floors = len(avail_floors)  
        max_exp = m.log(num_avail_floors+1)
        exponent = rand.uniform(0, max_exp)
        biased_random = int(m.exp(exponent))
        return biased_random
    #Tries to generate sequence of numbers from current floor to specified bound. It will then
    #take a random sample to create the floor requests array
    def _generateFloorRequests(self, direction, currentFloor, lowerBound, upperBound, size):
        while True:
            try:
                if direction == self.Direction.UP:
                    sequence = [i for i in range(currentFloor, upperBound) if i!=0]
                else:
                    sequence = [i for i in range(-1*lowerBound, currentFloor) if i!=0]
                if size > len(sequence):
                    raise ValueError()
                floorRequests = rand.sample(sequence, size)
                return floorRequests
            except ValueError:
                size = size - 1
                continue
        return floorRequests
    """
    Main Logic for Generating a Request when an Elevator hits a new floor
    -	First the direction is requested
    -	Second the number of floors is requested
    -	Third, filter out the current floor (cause pressing 2 when you're on floor 2 is dumb)
    -	Fourth, package request into dictionary and return it
    """        
    def generateRequest(self, currentFloor):
        direction_request = self._generateDirectionRequest(currentFloor)
        num_floor_requests = self._generateNumberofFloorRequests(direction_request, currentFloor, 
                                                                 self._minFloor, self._maxFloor)
        floor_requests = self._generateFloorRequests(direction_request, currentFloor,
                                                     self._minFloor, self._maxFloor, 
                                                     num_floor_requests)
        if currentFloor in floor_requests:
            floor_requests.remove(currentFloor)
        requestPackage = {direction_request:floor_requests}
        return requestPackage
        
if __name__ == "__main__":
    #Testng Scheme
    req = requestSimulator(15, -5)
    request = req.generateRequest(5)
    print(request)
        
