from picamera import PiCamera
from time import sleep
camera = PiCamera()
# camera.resolution = (416, 416)
camera.start_preview()
sleep(60)
camera.capture('/home/pi/Desktop/image%s.jpg' % 1)
camera.stop_preview()
