####Dependencies###################
from dronekit import connect, VehicleMode, LocationGlobalRelative
from time import sleep
from picamera import PiCamera
import math
#### Functions ####
def deg_to_str (f):

	f=math.fabs(f)

	deg_mod = math.modf(f);
	fdeg = deg_mod[1]
	fmin = deg_mod[0]
	min_mod = math.modf(fmin * 60)
	fmin = min_mod[1]
	fsec = min_mod[0] * 60

	return "{:03.0f}/1,{:02.0f}/1,{:05.0f}/1000".format(fdeg, fmin, fsec*1000)
def dist_to_str (f):
	return "{:.0f}/10".format (f * 10)
#### Mission################################

camera = PiCamera()
camera.start_preview()
sleep(2)
camera.exposure_mode='sports'
camera.shutter_speed=1000
vehicle = connect('127.0.0.1:14550', wait_ready=True)

lat=deg_to_str(vehicle.location.global_relative_frame.lat)
lon=deg_to_str(vehicle.location.global_relative_frame.lon)
alt=dist_to_str(vehicle.location.global_relative_frame.alt)
if vehicle.location.global_relative_frame.lat > 0:
	camera.exif_tags['GPS.GPSLatitudeRef'] = 'N'
else:
	camera.exif_tags['GPS.GPSLatitudeRef'] = 'S'
if vehicle.location.global_relative_frame.lon > 0:
        camera.exif_tags['GPS.GPSLongitudeRef'] = 'E'
else:
        camera.exif_tags['GPS.GPSLongitudeRef'] = 'W'
camera.exif_tags['GPS.GPSLatitude'], camera.exif_tags['GPS.GPSLongitude'] = lat, lon

try:
	for i, filename in enumerate(camera.capture_continuous('/home/pi/Pictures/img{counter:03d}.jpg')):
        	lat=deg_to_str(vehicle.location.global_relative_frame.lat)
		lon=deg_to_str(vehicle.location.global_relative_frame.lon)
		alt=dist_to_str(vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.lat > 0:
        		camera.exif_tags['GPS.GPSLatitudeRef'] = 'N'
		else:
        		camera.exif_tags['GPS.GPSLatitudeRef'] = 'S'
		if vehicle.location.global_relative_frame.lon > 0:
        		camera.exif_tags['GPS.GPSLongitudeRef'] = 'E'
		else:
        		camera.exif_tags['GPS.GPSLongitudeRef'] = 'W'
		camera.exif_tags['GPS.GPSLatitude'] = lat
        	camera.exif_tags['GPS.GPSLongitude'] = lon
        	camera.exif_tags['GPS.GPSAltitude'] = alt
	 	print(filename)
        	sleep(1)
		if i==9:
			break
finally:
	camera.stop_preview()
vehicle.close()
### End of script
