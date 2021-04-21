# geotag
This python script is intended to assist with geotagging images taken from drones for the purposes of photogrammetry.

This project was originally written for a  quadcopter drone that uses ArduPilot flight controller firmware on a Raspberry Pi 4 (RPi) paired with Navio2.
It uses dronekit-python API to establish connection to the vehicle and get/set parameters such as gps location.
Pictures are taken using HQ Pi Camera which is connected to the RPi and uses the gps location gotten from dronekit to set the EXIF tags on the JPEG images.
