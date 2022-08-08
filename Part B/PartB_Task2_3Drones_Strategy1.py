#!/usr/bin/python3

import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt
import numpy as np
import datetime
import math
from scipy import stats
import seaborn as sns

# ******************************************************************************
# Read Drone Names List (Note! It could be also generated using "names" python package. Here is the list generated before!)
# ******************************************************************************

file = open("drone_names.txt", "r")
file_lines = file.read()
drone_names = file_lines.split("\n")
TYPE1=1
delay=[]
busy_time=0


# ******************************************************************************
# To take the measurements
# ******************************************************************************
class Measure:
    def __init__(self):
        self.arr = 0
        self.dep = 0
        self.ut = []
        self.oldT = 0
        self.delay = 0
        self.utq = [] # data.ut = number of average users in waiting line
        self.st = 0 # Service Time
        self.delays = []
        self.delay_w = 0
        self.dep_w = 0
        
        self.users = 0
        self.in_service = 0
# ******************************************************************************
# Client
# ******************************************************************************
class Client:
    def __init__(self, type, arrival_time):
        self.type = type
        self.arrival_time = arrival_time
        
# ******************************************************************************
# Drones
# *********************************************************************

class Drone(object):
    
    def __init__(self, name, nQ, buffer_size, charge_time_threshold=0, MaxAutonomyLevel=1500, PVType="None", start_job=0, end_job=86400):

        self.name = name
        self.FES = PriorityQueue()
        self.users = 0
        self.in_service = 0
        self.delayed = []
        self.temp_st = []
        self.count = 0
        self.queue = []
        self.nQ = nQ
        self.buffersize = buffer_size
        self.loss = 0
        self.loss_outofactivity = 0
        self.st_w = 0
        
        #Self Drone Measurements
        self.n_arrival = 0
        self.n_departure = 0
        self.oTime = 0
        self.utq = 0
        self.ut = 0
        self.delay = 0
        self.delays = []
        self.st = 0
        self.log = []
        
        #Charge Staff
        self.cycle = 0
        self.charged_seconds = 0
        self.charge_level = 1500
        self.max_autonomy_level = MaxAutonomyLevel
        self.status = "Online"
        self.charge_timestamp = 0
        self.charge_time_threshold = charge_time_threshold
        self.start_job = start_job
        self.end_job = end_job
        
        #PV Panel
        self.PVType = PVType
        
        if self.PVType== "40W":
            self.charge_increase=300
        elif self.PVType== "60W":
            self.charge_increase=600
        elif self.PVType== "70W":
            self.charge_increase=900
        elif self.PVType== "None":
            self.charge_increase=0        
        
        
    def charge_consume(self, serve_time):
        self.charge_level -= serve_time
        
    def charge(self, live_time):
        self.charge_level = ((live_time - old_time)/3600)*1500 + self.charge_level
        if live_time - self.charge_timestamp >= 3600:
            self.charge_level = 1500
            print(f"Drone {str(self.nQ)} - {self.name} Fully Charged !!! LET'S GET BACK TO THE MISSION!")
            self.charge_time = 0
            self.status = "Online"
            
        

# ******************************************************************************
# Arrivals
# *********************************************************************

def time_converter(time, mode='print'):
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)
    if mode=='print':
        return str("%d:%02d:%02d" % (hours, minutes, seconds))
    if mode=='num':
        return hours, minutes, seconds
    

def arrival(time, drone, my_drones, service_time, inter_arrival):
    global in_service
    global n_drone
            
    
    data.arr += 1
    data.oldT = time
    drone.n_arrival += 1
    drone.utq += ((drone.users) - (drone.in_service)) * (time - drone.oTime)
    drone.ut += (drone.users)*(time - drone.oTime)
    drone.oTime = time
    
    rand_choice = random.randint(0, len(My_Drones)-1)
    while my_drones[rand_choice].status!="Online":
        rand_choice = random.randint(0, len(My_Drones)-1)
    my_drones[rand_choice].FES.put((time + inter_arrival, "Arrival"))
    
    if (len(drone.queue) < (drone.buffersize)) and (drone.service_condition == "At Service"):
        print(f"ARR Drone {str(drone.nQ)} - {drone.name} {drone.status} ({drone.charge_level}): Arrival No. {data.arr} ({drone.n_arrival}) at time {time_converter(time, mode='print')} with {drone.users} users in queue!")      
        drone.users += 1
        data.users += 1
        client = Client(TYPE1, time)
        drone.queue.append(client)
        drone.delayed.append(client.arrival_time)
        
        if drone.users==1:
            drone.delayed.remove(client.arrival_time)
            drone.count += 1
            drone.FES.put((time + service_time, "Departure from Server"))
            drone.charge_consume(service_time)
            drone.in_service += 1
            data.in_service += 1
        
    else:
        drone.loss += 1
        if drone.status=="In Charge":
            drone.loss_outofactivity += 1
        print(f"B-ARR Drone {str(drone.nQ)} - {drone.name} {drone.status} ({drone.charge_level}): Bypassed Arrival No. {data.arr} ({drone.n_arrival}) at time {time_converter(time, mode='print')} with {drone.users} users in queue!")
    
# ******************************************************************************
# Departures
# *******************************************************************
def departure(time, drone, my_drones, service_time):
    global delay 
    global in_service
    global busy_time       


    # For those who experienced delay [Waiting line]
    if drone.status=="In Charge":
        while drone.users>0:
            print(f"B-DEP Drone {str(My_Drones[i].nQ)} - {My_Drones[i].name} {My_Drones[i].status} ({My_Drones[i].charge_level}): Departure Canceled at time {time_converter(time, mode='print')} with {My_Drones[i].users-1} users in queue!")
            client = drone.queue.pop(0) 
            My_Drones[i].in_service -= 1
            My_Drones[i].users -= 1
            data.users -= 1
            My_Drones[i].loss += 1
            My_Drones[i].loss_outofactivity += 1
            
    
    else:
        if len(drone.queue) != 0 :
        # Get the first element from the queue
            client = drone.queue.pop(0)
            print(f"DEP Drone {str(drone.nQ)} - {drone.name} {drone.status} ({drone.charge_level}): Departure No. {data.dep+1} ({drone.n_departure+1}) at time {time_converter(time, mode='print')} with {drone.users-1} users in queue!")
            drone.delay += (time-client.arrival_time)
            data.delay += (time-client.arrival_time)
            drone.delays.append(time-client.arrival_time)
            data.delays.append(time-client.arrival_time)
            data.dep += 1
            data.oldT = time
            drone.n_departure += 1
            drone.ut += (drone.users)*(time - drone.oTime)
            drone.utq += ((drone.users) - (drone.in_service)) * (time - drone.oTime)
            drone.oTime = time
            drone.in_service -= 1
            drone.users -= 1

        # See whether there are more clients to in the line

            if drone.users > 0:   
                drone.st += service_time
                data.st += service_time
                drone.FES.put((time + service_time, "Departure from Server"))
                drone.charge_consume(service_time)
                delay.append(time - client.arrival_time)
                busy_time += service_time 
                drone.in_service += 1
                data.in_service += 1
        

# ******************************************************************************
# The "main" of the simulation
# ******************************************************************************


results_list = []

random.seed(50)

data = Measure()

# Buffer_size
buffer_size = 5

#Threshold for going to charge
charge_time_threshold = 0

#The Simulation Time 

Simulation_Results = []

time = 28800
initial = time
SIM_TIME = 57600

# Define The Traffic Distribution

Min_load = 0.5
Max_load_factor = 5.5
load_data = np.linspace(0, 86500, 86500) # Timeline
load_data2 = np.concatenate((load_data, load_data), axis=0) # Timeline
M1 = 36000 # First Peak at 10 O'Clock
V1 = 86500
S1 = math.sqrt(V1)
M2 = 50400 # Second Peak at 14 O'Clock
V2 = 86500
S2 = math.sqrt(V2)
Load_dist = (stats.norm.pdf(load_data, M1, 15*S1) + stats.norm.pdf(load_data, M2, 15*S2))*Max_load_factor*1000 + Min_load
Load_dist2 = np.concatenate((Load_dist, Load_dist), axis=0)

#Define Number of Drones

My_Drones = []

My_Drones.append(Drone(name=drone_names[0], nQ=1, buffer_size=buffer_size, charge_time_threshold=charge_time_threshold))
My_Drones.append(Drone(name=drone_names[1], nQ=2, buffer_size=buffer_size, charge_time_threshold=charge_time_threshold))
My_Drones.append(Drone(name=drone_names[2], nQ=3, buffer_size=buffer_size, charge_time_threshold=charge_time_threshold))

# Schedule the first arrival at T=0

rand_choice = random.randint(0, len(My_Drones)-1)
My_Drones[rand_choice].FES.put((time, "Arrival"))

# simulate until the simulated time reaches a constant
drone_joined=0
while time < SIM_TIME:

    for i in range(len(My_Drones)):
        if len(My_Drones[i].FES.queue):
            (time, event_type) = My_Drones[i].FES.get()
            LOAD = round(Load_dist2[round(time)], 2)
            SERVICE = 10.0 # Average Service Time
            ARRIVAL = SERVICE/LOAD # Average Interarrival Time
            inter_arrival = random.expovariate(lambd=1.0/ARRIVAL)
            service_time = random.expovariate(lambd=1.0/SERVICE)
            if event_type == "Arrival":
                if (My_Drones[i].charge_level<(inter_arrival+My_Drones[i].charge_time_threshold)) and (My_Drones[i].status=="Online"):
                    My_Drones[i].status="In Charge"
                    My_Drones[i].FES.put((time + (3600-(My_Drones[i].charge_level*2.4)), "Full Charge"))
                    My_Drones[i].charged_seconds += (3600-(My_Drones[i].charge_level*2.4))
                    print(f"CHARGE CODE1: Drone {My_Drones[i].nQ} - {My_Drones[i].name} is Taking a Break to Charge!")

                elif (My_Drones[i].charge_level<service_time+charge_time_threshold) and (My_Drones[i].status=="Online"):
                    My_Drones[i].status="In Charge"
                    My_Drones[i].FES.put((time + (3600-(My_Drones[i].charge_level*2.4)), "Full Charge"))
                    My_Drones[i].charged_seconds += (3600-(My_Drones[i].charge_level*2.4))
                    print(f"CHARGE CODE2: Drone {My_Drones[i].nQ} - {My_Drones[i].name} is Taking a Break to Charge!")

                else:
                    My_Drones[i].service_condition = "At Service"
                    My_Drones[i].st += service_time
                    arrival(time, My_Drones[i], My_Drones, service_time, inter_arrival)

            elif event_type == "Departure from Server":
                My_Drones[i].st += service_time
                departure(time, My_Drones[i], My_Drones, service_time)

            elif event_type == "Full Charge":
                print(f"CHARGE: Drone {My_Drones[i].nQ} - {My_Drones[i].name} Has Been Fully Charged! Number of Recharge Cycles: {My_Drones[i].cycle+1}")
                My_Drones[i].status = "Online"
                My_Drones[i].service_condition = "At Service"
                My_Drones[i].charge_level = My_Drones[i].max_autonomy_level
                My_Drones[i].cycle += 1
                while My_Drones[rand_choice].status!="Online":
                    rand_choice = random.randint(0, len(My_Drones)-1)
                My_Drones[rand_choice].FES.put((time + inter_arrival, "Arrival"))

        results = (My_Drones[i].nQ, time, (My_Drones[i].end_job-My_Drones[i].start_job), My_Drones[i].n_arrival, My_Drones[i].n_departure, My_Drones[i].loss,
               My_Drones[i].cycle, My_Drones[i].status, My_Drones[i].charge_level)
        My_Drones[i].log.append(results)

        
for i in range(len(My_Drones)):
    lambtda = round(1/ARRIVAL, 3)
    mu = round(1/SERVICE, 3)
    rho = round(lambtda/mu, 3)

    # ******************************************************************************
    # Print output data
    # ******************************************************************************
    print('\n ========= STATS - Task 1 =========')
    print("\n Number of arrivals:", My_Drones[i].n_arrival)
    print("\n Number of transmitted packets:", My_Drones[i].n_departure)
    print("\n Number of dropped packets:", My_Drones[i].loss)
    print("\n Average number of packets:", round(My_Drones[i].ut/time, 3)) # obtained E[N]\
    print("\n Expected average number of packets:", round(rho/(1-rho), 3)) # expected E[N]
    print("\n Average system delay:", round(My_Drones[i].delay/My_Drones[0].n_departure, 3) ,"ms") # obtained E[T]
    print("\n Expected average system delay:", round(1/(mu - lambtda),3) ,"ms") # expected E[T]
    print("\n Average queue delay:", round(((My_Drones[i].delay - My_Drones[i].st)/My_Drones[i].n_departure),3),"ms" ) #Obtained E[Tw]
    print("\n Expected average queue delay:", round(rho / (mu - lambtda),3),"ms") # expected E[Tw]
    print("\n Average number of packets in queue:", round(My_Drones[i].utq / time,3)) #obtained E[Nw] 
    print("\n Expected average number of packets in queue:", round((rho * rho) / (1 - rho),3)) #expected E[Nw]
    print("\n Loss probability:",round((My_Drones[i].loss/My_Drones[i].n_arrival)*100,3),"%")
    print("\n Busy time:", round(My_Drones[i].st, 3),"%")
    print("\n Expected busy time:", round(rho * 100, 3),"%")
    print("\n Number of Cycles:", My_Drones[i].cycle)
    print("\n Remaining Charge:", My_Drones[i].charge_level)
    print("\n")



    # ******************************************************************************
    # Plot
    # ******************************************************************************

    sns.set_style("white", {"grid.color": ".6", "grid.linestyle": ":",
          'axes.spines.left': True,
          'axes.spines.right': True,
          'axes.spines.bottom': True,
          'axes.spines.top': True,
          'xtick.color':'black',
          'ytick.color':'black',
          'xtick.bottom': False,
          'xtick.top': False,
          'ytick.right': False,
          'ytick.left': False})

    hours_t, minutes_t, seconds_t = time_converter(initial, mode='num')
    hours_s, minutes_S, seconds_s = time_converter(SIM_TIME, mode='num')

    fig = plt.figure()
    sns.histplot(data=My_Drones[i].delays, stat='count', kde=True, color='blue')
    plt.xlabel("Queue Delay (ms)")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of the Queuing Delay Between {hours_t} and {hours_s} Hours")
    plt.xlim(0.1000)
    plt.grid()
    plt.savefig(f"dist_queing_delay_{My_Drones[i].name}.png", dpi=300)
    plt.show()


fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(load_data, Load_dist, 'b-')
ax.vlines([36000, 50400], 0.5, 1, linestyles='dashed', colors='grey', label='Peak Traffic')
ax.set_xlabel("24h Time [S]")
ax.set_ylabel("Load")
ax.set_title("Distribution of the Load During the Day")
plt.legend()
plt.show()

for i in range(len(My_Drones)):
    Simulation_Results.append(My_Drones[i].log)
    

times = [Simulation_Results[0][i][1] for i in range(0, len(Simulation_Results[0]))]
charge = [Simulation_Results[0][i][-1] for i in range(0, len(Simulation_Results[0]))]

strategy=0
for simulation in Simulation_Results:
    fig, ax = plt.subplots(figsize=(14, 4))
    times = [simulation[i][1] for i in range(0, len(simulation))]
    charge = [simulation[i][-1] for i in range(0, len(simulation))]
    ax.plot(load_data, Load_dist*1500, 'b--', label="Load Distribution")
    ax.vlines([36000, 50400], 0, 1500, linestyles='dashed', colors='grey', label='Traffic Peaks')
    ax.plot(times, charge, alpha=0.8, c=np.random.rand(3,))
    online_charge = []
    online_time = []
    offline_charge = []
    offline_time = []
    for i in range(1, len(charge)):
        if charge[i] < charge[i-1]:
            online_charge.append(charge[i])
            online_time.append(times[i])
        elif charge[i] > charge[i-1]:
            offline_charge.append(charge[i-1])
            offline_charge.append(charge[i])
            offline_time.append(times[i-1])
            offline_time.append(times[i])
    
    strategy+=1
    ax.scatter(online_time, online_charge, color='black', s=4, alpha=1, label='Drone Online') 
    ax.scatter(offline_time, offline_charge, color='red', s=20, alpha=1, label='Drone Offline')
    ax.set_xticks(np.arange(0,88400,4000), rotation=90)
    ax.set_yticks(np.arange(0,1600,100))
    ax.set_xlabel("Time [S]")
    fr_h, fr_m, fr_s = time_converter(initial, mode='num')
    to_h, to_m, to_s = time_converter(SIM_TIME, mode='num')
    ax.set_ylabel(f"Drone Charge Level")
    ax.set_title(f"Drone Working Status Between {fr_h}:{fr_m}:{fr_s} - {to_h}:{to_m}:{to_s} / Strategy {strategy}")
    plt.grid()
    plt.legend()
    plt.savefig(f"Task1_Strategy{strategy}.png", dpi=300)
    plt.show()