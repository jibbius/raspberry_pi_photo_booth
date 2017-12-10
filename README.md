# Raspberry Pi Photo Booth
The code for my Raspberry Pi Photo Booth

<p align="center"><img alt="Raspberry Pi Photo Booth" src="https://github.com/jibbius/raspberry_pi_photo_booth/blob/master/promo_image.jpg?raw=true" /></p>

# Instructions
1. Build a photo booth (see below)

2. Connect your Pi and PiCamera

3. Connect a button to the Pi's GPIO21 and Ground pins.

4. Install git & pip & PIL (pillow instead as PIL is almost dead)
`apt update && apt install git python-pip python-imaging`

5. Clone the code:
`git clone https://github.com/jibbius/raspberry_pi_photo_booth.git`

6. Install dependencies:
`pip install -r requirements.txt`

7. Activate picamera in raspi-config:
`sudo raspi-config`
<p align="center"><img alt="Raspberry Pi Photo Booth" src="https://github.com/ieguiguren/raspberry_pi_photo_booth/blob/master/raspiconfig1.png?raw=true" /></p>
<p align="center"><img alt="Raspberry Pi Photo Booth" src="https://github.com/ieguiguren/raspberry_pi_photo_booth/blob/master/raspiconfig2.png?raw=true" /></p>
<p align="center"><img alt="Raspberry Pi Photo Booth" src="https://github.com/ieguiguren/raspberry_pi_photo_booth/blob/master/raspiconfig3.png?raw=true" /></p>
You must have camera connected to avoid the error:
`mmal: mmal_vc_component_create: failed to create component 'vc.ril.camera' (1:ENOMEM)
mmal: mmal_component_create_core: could not create component 'vc.ril.camera' (1)
Traceback (most recent call last):
  File "./camera.py", line 45, in <module>
    camera = picamera.PiCamera()
  File "/usr/local/lib/python2.7/dist-packages/picamera/camera.py", line 431, in __init__
    self._init_camera(camera_num, stereo_mode, stereo_decimate)
  File "/usr/local/lib/python2.7/dist-packages/picamera/camera.py", line 460, in _init_camera
    "Camera is not enabled. Try running 'sudo raspi-config' "
picamera.exc.PiCameraError: Camera is not enabled. Try running 'sudo raspi-config' and ensure that the camera has been enabled.
`
8. Run:
`./camera.py`

9. Photos will get saved to photos directory where you can elect to publish them later.

More detailed instructions available on the blog:

[jackbarker.com.au/photo-booth/](http://jackbarker.com.au/photo-booth/)
