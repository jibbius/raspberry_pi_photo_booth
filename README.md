# Raspberry Pi Photo Booth
The code for my Raspberry Pi Photo Booth (Version 2)

<p align="center"><img alt="Raspberry Pi Photo Booth" src="https://github.com/jibbius/raspberry_pi_photo_booth/blob/master/promo_image.jpg?raw=true" /></p>

# Instructions
1. Build a photo booth (see below)

2. Connect your Pi and PiCamera

3. Connect a button to the Pi's GPIO21 and Ground pins.

4. Install git & pip & pillow (which replaces PIL)
`apt update && apt install git python-pip python-imaging`

5. Clone the code:
`git clone https://github.com/jibbius/raspberry_pi_photo_booth.git`

6. Install dependencies:
`pip install -r requirements.txt`

(Or, if you are using python3: `python3 -m pip install -r requirements.txt`)

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
picamera.exc.PiCameraError: Camera is not enabled. Try running 'sudo raspi-config' and ensure that the camera has been enabled.`

8. Run:
`python ./camera.py`

9. Photos will get saved to photos directory where you can elect to publish them later.

More detailed instructions available on the blog:

[jackbarker.com.au/photo-booth/](http://jackbarker.com.au/photo-booth/)

# Contributing
I am happy for anyone to submit issues and pull requests.

A special thank you to all those who have submitted issues, and pull requests.

# Version History
- 2.1 (2018-04-30)
  - Allow "get ready" overlay images, to contain transparent sections.
  - Previously, when photo resolution was increased an "out of memory" error would occur during playback. Now fixed. (Special thanks: Daniel).
  - Config moved to `camera-config.yaml`, in anticipation of new functionality ("coming soon").
- 2.0 (2018-04-10)
  - Move all config into a separate file.
  - Introduce YAML dependency.
  - Introduce version history.
  - Updated readme with additional installation instructions (Special thanks: ieguiguren).
- 1.2 (2018-02-28)
  - Add debounce timer functionality to prevent accidental button presses due to EM interference (Special thanks: Andre).
- 1.1 (2018-01)
  - Correction to Python header (Credit: ieguiguren).
- 1.0 (2017-05)
  - Initial version.

# License
This code is free to be used and modified in any manner that you would like.

Attribution is encouraged, but not required.
