# Drone Assisted Communication Network Management

Nowadays, we are witnessing a staggering and rapid growth of mobile traffic volumes, featuring increasingly tighter Quality of Service constraints. Extensive densification of Radio Access Networks (RANs) is hence required to satisfy this huge and exacting service demand, especially in urban environments. Nevertheless, besides raising remarkable sustainability concerns due to the consequent energy consumption growth, the boundless expansion of terrestrial networks in smart city ecosystems may be limited by physical and regulatory constraints. In this context, aerial network nodes powered by renewable energy represent a promising solution to offer additional bandwidth capacity in locations where additional on-ground Base Stations cannot be installed, without increasing the energy demand from the power grid.

## Objectives

### Part A

**- 1)** We're investigating the case that a single drone, featuring a single antenna and no buffer, is sent to provide additional capacity during peak time.

**- 2)** The case in which that a single drone has been equipped with two antennas with a finite buffer.

**- 3)** Assuming an infinite buffer size, simulating the case in which two drones, each equipped with a single antenna are providing service to the area.

**- 4)** Considering all the above cases with General Distributions.

### Part B

In this part, we assume that the drones can be powered either by a battery unit or by a battery unit plus an additional small photovoltaic (PV) panel:

• If the drone is equipped with a battery unit only, its autonomy is 25 minutes, after which the drone must reach the charging station where its battery must be fully recharged before the drone becomes operational again. 60 minutes are required to fully recharge the drone battery.

• If the drone is equipped with a battery unit and a PV panel, its autonomy depends on the size of the photovoltaic (PV) panel capacity (that corresponds to the power that can be produced by the panel from the conversion of solar radiation under standard test conditions), according to the following table:


| PV panel capacity [W]*  | Drone autonomy [Min] |
| :---: | :---: |
| 40  | 30  |
| 60  | 35  |
| 70  | 40  |

**Note!** These values of autonomy only hold during daytime hours in which significant levels of renewable energy are produced, that we assume corresponding to the period from 8 a.m. to 4 p.m. During the rest of the day, the drone autonomy is 25 minutes. In any case, once the drone battery is empty, 60 minutes are required to fully recharge it.

The process including the full charging of the battery from an empty state and the progressive discharge of the battery during the drone activity until it becomes empty again represents a complete charging/discharging cycle of the battery. The deterioration of the battery is typically proportional to the number of complete charging/discharging cycles, and, after the number of cycles that the battery undergoes achieves a given threshold (typically of the order of several hundreds of cycles), the battery needs to be replaced.

Here we consider a realistic scenario in which the mobile traffic varies over time during the day. In the simulation area, the traffic typically features two peak
periods, one in the morning and one in the afternoon after lunchtime, whereas as the evening approaches the traffic rate tends to decrease.

There are several strategies provided in this part:

**- 1)** Considering a drone hosting a Base Station and equipped with a battery unit as power supply.

<p align="center">
  <img width="50%" height="50%" src="https://user-images.githubusercontent.com/63496218/183425964-7e1243f4-027f-489d-8d55-d2f704f3e740.png">
</p>

<p align="center">
  <img width="50%" height="50%" src="https://user-images.githubusercontent.com/63496218/183426386-df1eb33c-15de-4318-ac02-0fe4e173e135.png">
</p>

<p align="center">
  <img width="50%" height="50%" src="https://user-images.githubusercontent.com/63496218/183426415-0d2b891c-1f68-4662-9901-8f4fae455f99.png">
</p>

<p align="center">
  <img width="50%" height="50%" src="https://user-images.githubusercontent.com/63496218/183426433-4272c7d1-345c-4ede-8f9f-8109336d71bb.png">
</p>

<p align="center">
  <img width="50%" height="50%" src="https://user-images.githubusercontent.com/63496218/183426447-647c514b-c821-4c08-9bd7-33158da15461.png">
</p>

**- 2)** A scenario in which up to three drones are used in a business area, assuming they are powered by a battery only.

<p align="center">
  <img width="50%" height="50%" src="https://user-images.githubusercontent.com/63496218/183427844-d4454a27-b4f1-41e7-b0df-80f2ac33b20f.png">
</p>

<p align="center">
  <img width="50%" height="50%" src="https://user-images.githubusercontent.com/63496218/183428113-bb26009a-4e13-4c80-9a28-e4a4246b864a.png">
</p>


**- 3)** A scenario with N available drones, that can be of three types, like, for example:

| Specifications For Each Drone  | Type A | Type B | Type C |
| :---: | :---: | :---: | :---: |
| PV Type |  -  |  40W  |  70W  |
| Service Rate |  Mu  |  2Mu  |  Mu  |
| Buffer Size |  S  |  S  |  2S  |


Considering N=2, there will be 6 different strategies to send the drones to the service area. All of these strategies and their following test results could be observed through the following table which are pairs of (A,A), (B,B), (C,C), (B,C), (A,C), and (A,B):

<p align="center">
  <img width="50%" height="50%" src="https://user-images.githubusercontent.com/63496218/183430839-bff53ace-5d7a-46b2-a724-78548b61405c.png">
</p>

## Requirements

Find the `requirements.txt` in each folder and install them using `pip install requirements.txt` command in the abovementioned directories.
