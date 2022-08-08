#!/usr/bin/python3

import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt
import numpy as np

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
busy_time1 = 0
busy_time2 = 0

idle1 = True
idle2 = True
temp_st = []
delay = []
loss = 0

Buffer_size = 5
# Buffer_size = np.inf
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
        self.st2 = 0 # Service Time2
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
class Server():

    # constructor
    def __init__(self):

        # whether the server is idle or not
        self.idle = True
    def busy(self):
        self.idle = False
    def ready(self):
        self.idle = True
    def status(self):
        return self.idle 
        
S1 = Server()
S2 = Server()

# ******************************************************************************
# Arrivals
# *********************************************************************
def arrival(time, FES, queue):
    global users, in_service
    global loss

    print("users in queue last time", users,
            ",Arrival no.", data.arr+1, " at time ", time)

    # cumulate statistics
    data.arr += 1
    data.utq += (users-in_service) * (time - data.oldT)
    data.ut += users*(time-data.oldT)
    data.oldT = time

    # sample the time until the next event
    inter_arrival = random.expovariate(lambd=1.0/ARRIVAL)

    # schedule the next arrival
    FES.put((time + inter_arrival, "Arrival"))
    
    # create a record for the client
    # first 2 in the queue are receving service the remaining 5 are in waiting line
    if len(queue)<(Buffer_size + 1):
        users += 1
        client = Client(TYPE1, time)
        # insert the record in the queue
        queue.append(client)
        data.delayed.append(client.arrival_time)
    else:
        loss +=1
        # print ("Arrival no. ",data.arr, "dropped")
        
    # if the server is idle start the service
    if users>0 and users <= 2:
        data.count += 1
        
        #if the first server is idle then starts to serve
        if S1.status():
        # sample the service time
            service_time = random.expovariate(1.0/SERVICE)
            # service_time = random.uniform(0.1, SERVICE)
            FES.put((time + service_time, "Departed from Server 1"))
            S1.busy()
            data.st += service_time
            in_service += 1
            data.delayed.remove(client.arrival_time)
            
        #if the second server is idle then starts to serve
        elif S2.status():
            service_time = random.expovariate(1.0/SERVICE)
            # service_time = random.uniform(0.1, SERVICE)
            FES.put((time + service_time, "Departed from Server 2"))
            S2.busy()
            data.st2 += service_time
            data.delayed.remove(client.arrival_time)
            in_service += 1

# ******************************************************************************
# Departures
# *******************************************************************
def departure(time, FES, queue):
    global users
    global temp_st, in_service


    print("Departure no. ",data.dep+1," at time ",time," with ",users," users in queue" )

    # cumulate statistics
    data.dep += 1  
    data.ut += users*(time-data.oldT)
    data.utq += (users - in_service) * (time - data.oldT)
    data.oldT = time
    
    #if the system is not empty
    if len(queue)!=0:
        users -= 1
        in_service -= 1

    # get the first element from the queue
        client = queue.pop(0)

    # do whatever we need to do when clients go away
        data.delay += (time-client.arrival_time)
        data.delays.append(time-client.arrival_time)
    # see whether there are more clients to in the line
        if len(queue)>1:
            #if the first server is idle then starts to serve
            if S1.status():
                S1.busy()
                # sample the service time
                service_time = random.expovariate(1.0/SERVICE)
                # service_time = random.uniform(0.1, SERVICE)
                data.st += service_time
                temp_st.append(service_time)
            # schedule when the client will finish the server
                FES.put((time + service_time, "Departed from Server 1"))
                in_service += 1
                
            
            elif S2.status():
                S2.busy()
                service_time = random.expovariate(1.0/SERVICE)
                # service_time = random.uniform(0.1, SERVICE)
                data.st2 += service_time
                temp_st.append(service_time)
            # schedule when the client will finish the server
                FES.put((time + service_time, "Departed from Server 2"))
                in_service += 1

        #for those who experienced delay [waiting line]
        if client.arrival_time in data.delayed:
            data.delay_w += (time - client.arrival_time)
            data.dep_w += 1
            data.st_w += temp_st[0]
            temp_st.pop(0)
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

    elif event_type == "Departed from Server 1":
        S1.ready()
        departure(time, FES, MM1)
        
        
    elif event_type == "Departed from Server 2":
        S2.ready()
        departure(time, FES, MM1)

lambtda = round(1/ARRIVAL, 3)
mu = round(1/SERVICE, 3)
rho = round(lambtda/mu, 3)
# ******************************************************************************
# Print output data
# ******************************************************************************
print('\n ========= M/M/2 =========')
print("\n Number of arrivals:",data.arr)
print("\n Number of transmited packets:", data.dep)
print("\n Number of dropped packets:", loss)
print("\n Average number of packets:", round(data.ut/time, 3)) # obtained E[N]
print("\n Average system delay:",round(data.delay/data.dep, 3) ,"ms") # obtained E[T]

print("\n Average queue delay:", round(((data.delay - (data.st + data.st2)) /data.dep),3),"ms" ) # obtained E[Tw]
print("\n Average queue delay of packets experianced delay:", round(((data.delay_w - data.st_w)/data.dep_w),3),"ms" )      
print("\n Average number of packets in queue:", round(data.utq / time,3)) # obtained E[Nw]
print("\n Loss probability:",round((loss/data.arr)*100,3),"%")
print("\n Server 1 busy time percentage:", round(data.st / time * 100, 3),"%")
print("\n Server 1 busy time:", round(data.st / 1000, 3),"s")
print("\n Server 2 busy time percentage:", round(data.st2 / time * 100, 3),"%")
print("\n Server 2 busy time:", round(data.st2 / 1000, 3),"s")
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
