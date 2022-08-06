# Summary

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
