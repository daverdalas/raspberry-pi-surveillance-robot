# Raspberry Pi Surveillance Robot a.k.a. Kerfuś

## Description
Software to control a Raspberry Pi-based robot from anywhere through a Internet using a PC or smartphone. It will provide camera viewing with minimal latency (using WebRTC) and real-time control.
An off-the-shelf G1-Tank platform from Yahboom (https://github.com/YahboomTechnology/Raspberry-pi-G1-Tank) was used as the base, but the code can be easily adapted under any other Raspberry Pi-based robot.

## Setup
The prepared project runs on docker compose so there is a need to install it for easy running.

Having docker composer installed the project can be installed using the command:

`make install`

## Running

Locally, we run the project using the command:

`make start`

## To do
- [ ] Complete the README.md
- [ ] Add smartphone control
- [ ] Charging station
- [ ] Web authentication