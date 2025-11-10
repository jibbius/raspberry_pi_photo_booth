# Raspberry Pi Photo Booth
The code for my Raspberry Pi Photo Booth (Version 3.0 - Updated for Modern Raspberry Pi OS)

<p align="center"><img alt="Raspberry Pi Photo Booth" src="https://github.com/jibbius/raspberry_pi_photo_booth/blob/master/promo_image.jpg?raw=true" /></p>

## What's New in Version 3.0

✅ **Updated for Modern Raspberry Pi OS**: Now works with Raspberry Pi OS Bullseye and later  
✅ **PiCamera2 Support**: Uses the new libcamera-based PiCamera2 library  
✅ **Enhanced GPIO Support**: Support for both RPi.GPIO and gpiozero libraries  
✅ **Better Error Handling**: Robust error handling and graceful degradation  
✅ **Improved Configuration**: Enhanced configuration validation and error reporting  
✅ **Conditional Dependencies**: Dropbox integration only loads when needed  
✅ **Test Mode**: Built-in test suite for development and debugging  

## Hardware Requirements

- Raspberry Pi (3B+ or newer recommended)
- Raspberry Pi Camera Module (v1, v2, or HQ Camera)
- Button connected to GPIO21 (and optionally GPIO13 for exit)
- Display (optional but recommended)

## Quick Start Instructions

### Option 1: Automated Setup (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jibbius/raspberry_pi_photo_booth.git
   cd raspberry_pi_photo_booth
   ```

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

The script will automatically create a virtual environment, install dependencies, and run tests.

### Option 2: Manual Setup

### For Raspberry Pi OS (Bullseye/Bookworm or later)

1. **Update your system**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install system dependencies**:
   ```bash
   sudo apt install -y git python3-pip python3-pil libcamera-apps python3-libcamera python3-kms++
   ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/jibbius/raspberry_pi_photo_booth.git
   cd raspberry_pi_photo_booth
   ```

4. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **Install Python dependencies**:
   
   For Raspberry Pi:
   ```bash
   pip install -r requirements-pi.txt
   ```
   
   For development/testing (non-Pi systems):
   ```bash
   pip install -r requirements.txt
   ```

6. **Enable camera interface**:
   ```bash
   sudo raspi-config
   ```
   Navigate to: `Interface Options` → `Camera` → `Enable`
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

7. **Test the installation**:
   ```bash
   python test_photobooth.py
   ```

8. **Connect your hardware**:
   - Connect button to GPIO21 and Ground
   - Connect camera module to camera port
   - Optional: Connect exit button to GPIO13 and Ground

9. **Run the photo booth**:
   ```bash
   python camera.py
   ```

10. **Optional: Run post-processing**:
    ```bash
    python photo-processor.py
    ```

## Important: Virtual Environment

Remember to activate your virtual environment each time you work on the project:

```bash
cd raspberry_pi_photo_booth
source .venv/bin/activate
```

When you're done, you can deactivate it:

```bash
deactivate
```

## Testing Without Hardware

For development and testing without a Raspberry Pi, you can:

1. **Run the test suite**:
   ```bash
   python3 test_photobooth.py
   ```

2. **Enable test mode** in `camera-config.yaml`:
   ```yaml
   TESTMODE_AUTOPRESS_BUTTON: True
   ```

This will simulate button presses and camera functionality.

More detailed instructions available on the blog:

[jackbarker.com.au/photo-booth/](http://jackbarker.com.au/photo-booth/)

# Contributing
I am happy for anyone to submit issues and pull requests.

A special thank you to all those who have submitted issues, and pull requests.

# Version History

- 3.0 (2025-11-10)
  - **MAJOR UPDATE**: Full compatibility with modern Raspberry Pi OS (Bullseye/Bookworm)
  - Replaced deprecated PiCamera with PiCamera2/libcamera
  - Enhanced GPIO support with both RPi.GPIO and gpiozero
  - Improved error handling and graceful degradation
  - Added comprehensive test suite
  - Enhanced configuration validation
  - Conditional Dropbox integration (no longer required)
  - Better development support without hardware
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
