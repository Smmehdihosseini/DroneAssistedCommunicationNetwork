#!/usr/bin/python3

import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt

# ******************************************************************************
# Constants
# ******************************************************************************
LOAD = 0.85
SERVICE = 10.0 # av service time
ARRIVAL = SERVICE/LOAD # av inter-arrival time
TYPE1 = 1 
SIM_TIME = 500000

arrivals = 0
users = 0
BusyServer = False # True: server is currently busy; False: server is currently idle
in_service = 0

MM1 = []

temp_st = []
busy_time = 0
delay = []
server_n = 2
loss = 0
# ******************************************************************************
# To take the measurements
# ******************************************************************************
class Measure:
    def __init__(self, Narr, Ndep, NAveraegUser, OldTimeEvent, AverageDelay):
        self.arr = Narr
        self.dep = Ndep
        self.ut = NAveraegUser
        self.oldT = OldTimeEvent
        self.delay = AverageDelay
        self.utq = 0 # data.ut = number of average users in waiting line
        self.st = 0 # Service Time
        self.delays = []
        self.delayed = []
        self.delay_w = 0
        self.st_w = 0
        self.count = 0
        self.dep_w = 0
# ******************************************************************************
# Client
# ******************************************************************************
class Client:
    def __init__(self, type, arrival_time):
        self.type = type
        self.arrival_time = arrival_time
# ******************************************************************************
# Server
# ******************************************************************************
class Server(object):

    # constructor
    def __init__(self):

        # whether the server is idle or not
        self.idle = True

# ******************************************************************************
# Arrivals
# *********************************************************************
def arrival(time, FES, queue):
    global users
    global in_service
    global loss
    
    print("Arrival no. ", data.arr+1," at time ", time, " with ", users," users" )
    
    # cumulate statistics
    data.arr += 1
    data.utq += (users-in_service) * (time - data.oldT)
    data.ut += users*(time-data.oldT)
    data.oldT = time

    # sample the time until the next event
    inter_arrival = random.expovariate(lambd=1.0/ARRIVAL)
    
    # schedule the next arrival
    FES.put((time + inter_arrival, "Arrival"))

    if len(queue) < 1:
        
        users += 1
    
        # create a record for the client
        client = Client(TYPE1, time)

        # insert the record in the queue
        queue.append(client)
        data.delayed.append(client.arrival_time)

        if users==1:
        
            data.delayed.remove(client.arrival_time)
            data.count += 1
            
        # sample the service time
            service_time = random.expovariate(1.0/SERVICE)
            # service_time = 1 + random.uniform(0.1, SERVICE)

        # schedule when the client will finish the server
            FES.put((time + service_time, "Departed from Server"))
            
            in_service += 1
        
    else:
        loss += 1
        
        # print("Last arrival bypassed!")

# ******************************************************************************
# Departures
# *******************************************************************
def departure(time, FES, queue):
    global users
    global delay 
    global in_service
    global busy_time
    
    print("Departure no. ", data.dep+1," at time ", time, " with ", users, " users")
        
    # cumulate statistics
    data.dep += 1
    data.ut += users*(time - data.oldT)
    data.utq += (users - in_service) * (time - data.oldT)
    data.oldT = time
    in_service -= 1

    #for those who experienced delay [waiting line]

         
    if len(queue) !=0 :
    # get the first element from the queue
        client = queue.pop(0)
    
    # do whatever we need to do when clients go away
    
        data.delay += (time-client.arrival_time)
        data.delays.append(time-client.arrival_time)
        users -= 1
        
        if client.arrival_time in data.delayed:
            data.st_w += temp_st[0]
            temp_st.pop(0)
            
    # see whether there are more clients to in the line
        if users > 0:
        # sample the service time
            service_time = random.expovariate(1.0/SERVICE)
            #service_time = random.uniform(0.1, SERVICE)
            
            data.st += service_time
            temp_st.append(service_time)
            
        # schedule when the client will finish the server
            FES.put((time + service_time, "Departed from Server"))
            
            delay.append(time - client.arrival_time)
            busy_time += service_time
            
            in_service += 1
# ******************************************************************************
# The "main" of the simulation
# ******************************************************************************
random.seed(50)

data = Measure(0,0,0,0,0)

# the simulation time 
time = 0

# the list of events in the form: (time, type)
FES = PriorityQueue()


# schedule the first arrival at t=0
FES.put((0, "Arrival"))

# simulate until the simulated time reaches a constant
while time < SIM_TIME:
    (time, event_type) = FES.get()

    if event_type == "Arrival":
        arrival(time, FES, MM1)

    elif event_type == "Departed from Server":
        departure(time, FES, MM1)

lambtda = round(1/ARRIVAL, 3)
mu = round(1/SERVICE, 3)
rho = round(lambtda/mu, 3)
# ******************************************************************************
# Print output data
# ******************************************************************************
print('\n ========= M/M/1 =========')
print("\n Number of arrivals:",data.arr)
print("\n Number of transmitted packets:", data.dep)
print("\n Number of dropped packets:", loss)
print("\n Average number of packets:", round(data.ut/time, 3)) # obtained E[N]
print("\n Expected average number of packets:", round(rho/(1-rho), 3)) # expected E[N]
print("\n Average system delay:",round(data.delay/data.dep, 3) ,"ms") # obtained E[T]
print("\n Expected average system delay:", round(1/(mu - lambtda),3) ,"ms") # expected E[T]

print("\n Average queue delay:", round(((data.delay - data.st)/data.dep),3),"ms" ) #obtained E[Tw]
print("\n Expected average queue delay:", round(rho / (mu - lambtda),3),"ms") # expected E[Tw]
print("\n Average number of packets in queue:", round(data.utq / time,3)) #obtained E[Nw] 
print("\n Expected average number of packets in queue:", round((rho * rho) / (1 - rho),3)) #expected E[Nw]
print("\n Loss probability:",round((loss/data.arr)*100,3),"%")
print("\n Busy time:", round(data.st / time * 100, 3),"%")
print("\n Expected busy time:", round(rho * 100, 3),"%")
print("\n")
# ******************************************************************************
# Plot
# ******************************************************************************
fig = plt.figure()
plt.hist(data.delays, density=False, bins = 1000)
plt.xlabel("Queue delay (ms)")
plt.ylabel("Frequency")
plt.title("Distribution of the queuing delay")
plt.xlim(0.1000)
plt.grid()
plt.show()
