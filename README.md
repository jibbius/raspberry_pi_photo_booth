# Raspberry Pi Photo Booth
The code for my Raspberry Pi Photo Booth (Version 2)

<p align="center"><img alt="Raspberry Pi Photo Booth" src="https://github.com/jibbius/raspberry_pi_photo_booth/blob/master/promo_image.jpg?raw=true" /></p>

# Instructions
1. Build a photo booth (see below)
2. Connect your Pi and PiCamera
3. Connect a button to the Pi's GPIO21 and Ground pins.
4. Download the code
5. Run:
`python camera.py`
5. Photos will get saved to photos directory where you can elect to publish them later.

More detailed instructions available on my blog:

[jackbarker.com.au/photo-booth/](http://jackbarker.com.au/photo-booth/)

# Contributing
I am happy for anyone to submit issues and pull requests.

A special thank you to all those who have submitted issues, and pull requests.

# Version History
- 2.0 (2018-04-10)
  - Move all config into a separate file.
  - Introduce YAML dependency.
  - Introduce version history.
  - Updated readme with additional installation instructions (Special thanks: ).
- 1.2 (2018-01)
  - Add debounce timer functionality, to prevent accidental button presses due to EM interference (Special thanks: ).
- 1.1 (2018-01)
  - Correction to Python header (Credit: ).
- 1.0 (2017-05)
  - Initial version.

# License
This code is free to be used and modified in any manner that you would like.

Attribution is encouraged, but not required.
