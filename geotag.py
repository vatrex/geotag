####Dependencies###################
from dronekit import connect, VehicleMode, LocationGlobalRelative
from time import sleep
import picamera
import math
import os
import shutil
import cv2
import picamera.array
from exif import Image


#### Functions ####

# returns amount of blurriness
def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()
    
# decimal degrees to DMS (degrees minutes seconds)
def dd2dms (f):
	f=math.fabs(f)
	deg_mod = math.modf(f);
	fdeg = deg_mod[1]
	fmin = deg_mod[0]
	min_mod = math.modf(fmin * 60)
	fmin = min_mod[1]
	fsec = min_mod[0] * 60
	return fdeg, fmin, fsec
       
#### Mission################################

vehicle = connect('127.0.0.1:14550', wait_ready=True) # connect to the vehicle

with picamera.PiCamera() as camera:
    camera.exposure_mode='sports'
    camera.shutter_speed=1000
    camera.resolution = (1280, 720)
    with picamera.array.PiRGBArray(camera) as output:
        i=0
        while True:
            while vehicle.location.global_relative_frame.alt<1:
                print('alt is too low: ' + str(vehicle.location.global_relative_frame.alt))
                sleep(1)
            i+=1
            print('target alt reached: ' + str(vehicle.location.global_relative_frame.alt))
            directory='/home/pi/Pictures/Flight'+str(i)
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.mkdir(directory)
            x=0
            while vehicle.location.global_relative_frame.alt>1:
                lat=dd2dms(vehicle.location.global_relative_frame.lat)
                lon=dd2dms(vehicle.location.global_relative_frame.lon)
                alt=vehicle.location.global_relative_frame.alt
                if vehicle.location.global_relative_frame.lat > 0:
                    lat_ref = 'N'
                else:
                    lat_ref = 'S'
                if vehicle.location.global_relative_frame.lon > 0:
                    lon_ref = 'E'
                else:
                    lon_ref = 'W'
                camera.capture(output, 'bgr')
                img = output.array
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                fm = variance_of_laplacian(gray)
                if fm > 50:
                    cv2.imwrite('/home/pi/Pictures/Flight%d' % i + '/img%d.jpg' % x, img)
                    my_image = Image('/home/pi/Pictures/Flight%d' % i + '/img%d.jpg' % x)
                    my_image['gps_latitude'] = lat
                    my_image['gps_latitude_ref'] = lat_ref
                    my_image['gps_longitude'] = lon
                    my_image['gps_longitude_ref'] = lon_ref
                    my_image['gps_altitude'] = alt
                    with open('/home/pi/Pictures/Flight%d' % i + '/img%d.jpg' % x, 'wb') as new_image_file:
                        new_image_file.write(my_image.get_file())
                        print('success')                
                    x+=1
                output.truncate(0)
                sleep(1)
                
### End of script
