# Raspberry Pi Photo Booth
The code for my Raspberry Pi Photo Booth

<p align="center"><img alt="Raspberry Pi Photo Booth" src="https://github.com/jibbius/raspberry_pi_photo_booth/blob/master/promo_image.jpg?raw=true" /></p>

# Instructions
1. Build a photo booth (see below)
2. Connect your Pi and PiCamera
3. Connect a button to the Pi's GPIO21 and Ground pins.
4. Install git & pip
`apt update && apt install git python-pip`
5. Clone the code:
`git clone https://github.com/jibbius/raspberry_pi_photo_booth.git`
6. Install dependencies:
`pip install -r requirements.txt`
7. Run:
`python camera.py`
8. Photos will get saved to photos directory where you can elect to publish them later.

More detailed instructions available on my blog:

[jackbarker.com.au/photo-booth/](http://jackbarker.com.au/photo-booth/)
