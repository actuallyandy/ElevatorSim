# ElevatorSim
Simulates an Elevator 

Settings GUI
The settings GUI is the first part of the application, where the user can set the parameters for the elevator's operation. This GUI includes various options such as the number of floors, the elevator's movement mechanism, and the type of cargo the elevator will handle (This determines the elevators speed). The user can select the desired options and click on the "okay" button to save the settings.

Simulator:
The simulator is the second part of the application, which runs the elevator simulation based on the settings selected in the settings GUI. The simulator will simulate the movement of the elevator and how it handles floor requests from the passengers. The simulator will keep track of the elevator's current floor, the floors the elevator was requested to travel to and the elevator's direction of movement. The simulator will also update the main GUI with the current floor information.

Main GUI:
The main GUI is the third and final part of the application, which displays the current floor of the elevator and the buttons for each floor. The buttons will be highlighted based on the requests made by simulated passangers. The main GUI will be updated by the simulator with the current floor information


#Assumptions
1. Zeroth Floor does not exist.
2. Request Simulator: People will not issue a command to go down the elevator and put a request in for a higher floor.
3. Elevator does not move in an algorthmic pattern. If the elevator was requested to go up, it will go up until the highest request floor is reached before switching directions.
4. Elevator's speed and weight capacity were estimated based on ranges of different elevator types. In reality it varies from manufacturer to manufacturer
5. Elevator's floor settings are based on the standard skyscraper size but most only can service a limited number of floors.
6. Elevator does not accelerate and only travels at max speed during trip.


#Features Not Implemented
1. There is no feature to indicate when a floor is passed, like a beep.
2. There are no Door-Open Door-Close buttons that force the elevator to open or close
3. There are no emergency buttons that initiate emergency procedures for the elevator.
4. There are no simulated emergency procedures like power outages, elevator malfunctions or fire alarms
5. There is no mechanism that names each floor and provides a custom greeting at each floor.
6. GUI only runs in sim mode, any input into the GUI by the user will not be processed.
7. Stationary Mode is not implemented as intended. Elevator currently only operates in UP or DOWN mode.
8. There is no weight handling algorithm in this app. Intended feature was to prevent more requests by estimating if elevator was at capacity by requests*average_cargo_weight
9. There is no implemented performance metrics. Metrics intended to be implemented: Response Time, Capacity Utilization, Average Waiting Time, and Downtime
10. Elevator will skip dumb requests for current floor requests. For example, if a person gets on floor 2 and requests floor 2, the elevator will skip this request. Although in real life, the elevator will simply open its doors again.
11. There is no indicator in which direction the elevator is moving.
