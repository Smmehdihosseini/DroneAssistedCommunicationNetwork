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
users = [0, 0]
BusyServer = False # True: server is currently busy; False: server is currently idle
in_service = [0, 0]

MM1A = []
MM1B = []

temp_st1 = []
temp_st2 = []

busy_time = 0
delay = []
server_n = 2
loss = 0

# Buffer_size = 5
Buffer_size = np.inf
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
        self.delayed1 = []
        self.delayed2 = []
        self.delay_w = 0
        self.st_w1 = 0
        self.st_w2 = 0
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
def arrival(time, FES, queue, Q):
    global users
    global in_service
    global loss
    
    print("Q" + str(Q) + ": Arrival no. ", data.arr+1," at time ", time, " with ", users[Q-1]," users" )
        
    # cumulate statistics
    data.arr += 1
    data.utq += ((users[0]+users[1])-(in_service[0]+in_service[1])) * (time - data.oldT)
    data.ut += (users[0]+users[1])*(time-data.oldT)
    data.oldT = time

    
    
    inter_arrival = random.expovariate(lambd=1.0/ARRIVAL)
    
    rand_choice = random.choice([1, 2])
    
    if rand_choice==1:
        FES1.put((time + inter_arrival, "Arrival"))
        
    elif rand_choice==2:
        FES2.put((time + inter_arrival, "Arrival"))

        
    if len(queue)<(Buffer_size + 1):
        if Q==1:
            users[0] += 1
            client = Client(TYPE1, time)
            queue.append(client)
            data.delayed1.append(client.arrival_time)
            
            if users[0]==1:
                data.delayed1.remove(client.arrival_time)
                data.count += 1
    
            # sample the service time
                service_time = random.expovariate(1.0/SERVICE)
                # service_time = 1 + random.uniform(0.1, SERVICE)
    
            # schedule when the client will finish the server
                FES1.put((time + service_time, "Departure from Server"))
    
                in_service[0] += 1
        
        if Q==2:   
            users[1] += 1
            client = Client(TYPE1, time)
            queue.append(client)
            data.delayed2.append(client.arrival_time)
            
            if users[1]==1:
                data.delayed2.remove(client.arrival_time)
                data.count += 1
    
            # sample the service time
                service_time = random.expovariate(1.0/SERVICE)
                # service_time = 1 + random.uniform(0.1, SERVICE)
    
            # schedule when the client will finish the server
                FES2.put((time + service_time, "Departure from Server"))
    
                in_service[1] += 1
        
    else:
        loss +=1
        
        # print("Last arrival bypassed!")
    # if the server is idle start the service
    
# ******************************************************************************
# Departures
# *******************************************************************
def departure(time, FES, queue, Q):
    global users
    global delay 
    global in_service
    global busy_time
    
    print("Q"+ str(Q) + " Departure no. ", data.dep+1," at time ", time, " with ", users[Q-1], " users")
        
    # cumulate statistics
    data.dep += 1
    data.ut += (users[0]+users[1])*(time - data.oldT)
    data.utq += ((users[0]+users[1]) - (in_service[0]+in_service[1])) * (time - data.oldT)
    data.oldT = time
    
    if Q==1:
        in_service[0] -= 1
        users[0] -= 1
    if Q==2:
        in_service[1] -= 1
        users[1] -= 1

    #for those who experienced delay [waiting line]

         
    if len(queue) !=0 :
    # get the first element from the queue
        client = queue.pop(0)
    
    # do whatever we need to do when clients go away
    
        data.delay += (time-client.arrival_time)
        data.delays.append(time-client.arrival_time)
            
    # see whether there are more clients to in the line
    
        if Q==1:
            if client.arrival_time in data.delayed1:
                data.st_w1 += temp_st1[0]
                temp_st1.pop(0)
            if users[0] > 0:
            # sample the service time
                service_time = random.expovariate(1.0/SERVICE)
                #service_time = random.uniform(0.1, SERVICE)

                data.st += service_time
                temp_st1.append(service_time)

            # schedule when the client will finish the server
                FES.put((time + service_time, "Departure from Server"))

                delay.append(time - client.arrival_time)
                busy_time += service_time

                in_service[0] += 1
                
        if Q==2:
            
            if client.arrival_time in data.delayed2:
                data.st_w2 += temp_st2[0]
                temp_st2.pop(0)
                
            if users[1] > 0:
            # sample the service time
                service_time = random.expovariate(1.0/SERVICE)
                #service_time = random.uniform(0.1, SERVICE)

                data.st += service_time
                temp_st2.append(service_time)

            # schedule when the client will finish the server
                FES.put((time + service_time, "Departure from Server"))

                delay.append(time - client.arrival_time)
                busy_time += service_time

                in_service[1] += 1
                
# ******************************************************************************
# The "main" of the simulation
# ******************************************************************************
random.seed(50)

data = Measure(0,0,0,0,0)

# the simulation time 
time = 0

# the list of events in the form: (time, type)
FES1 = PriorityQueue()
FES2 = PriorityQueue()



# schedule the first arrival at t=0

rand_choice = random.choice([1, 2])
if rand_choice==1:
    FES1.put((0, "Arrival"))
if rand_choice==2:
    FES2.put((0, "Arrival"))

# simulate until the simulated time reaches a constant
while time < SIM_TIME:
    
    if len(FES1.queue):
        (time, event_type) = FES1.get()
        if event_type == "Arrival":
            arrival(time, FES1, MM1A, Q = 1)
        elif event_type == "Departure from Server":
            departure(time, FES1, MM1A, Q = 1)
            
    if len(FES2.queue):
        (time, event_type) = FES2.get()
        if event_type == "Arrival":
            arrival(time, FES2, MM1B, Q = 2)
        elif event_type == "Departure from Server":
            departure(time, FES2, MM1B, Q = 2)

lambtda = round(1/ARRIVAL, 3)
mu = round(1/SERVICE, 3)
rho = round(lambtda/mu, 3)
# ******************************************************************************
# Print output data
# ******************************************************************************
print('\n ========= 2 M/M/1 =========')
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
print("\n Busy time:", round(data.st/ time * 100, 3),"%")
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