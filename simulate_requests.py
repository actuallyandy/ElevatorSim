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
        
    def _generateDirectionRequest(self, currentFloor):
        if currentFloor == self._maxFloor:
            return self.Direction.DOWN
        if currentFloor == self._minFloor:
            return self.Direction.UP
        options = (self.Direction.DOWN, self.Direction.UP)
        return rand.choice(options)
        
        
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
        
    def generateRequest(self, currentFloor):
        direction_request = self._generateDirectionRequest(currentFloor)
        num_floor_requests = self._generateNumberofFloorRequests(direction_request, currentFloor, 
                                                                 self._minFloor, self._maxFloor)
        floor_requests = self._generateFloorRequests(direction_request, currentFloor,
                                                     self._minFloor, self._maxFloor, 
                                                     num_floor_requests)
        requestPackage = {direction_request:floor_requests}
        return requestPackage
        
if __name__ == "__main__":
    #Testng Scheme
    req = requestSimulator(15, -5)
    request = req.generateRequest(5)
    print(request)
        