# main.py (version 2)
# OhmMeter with Big FONT, using Pico2040 and a sh1106 - ensure the sh1106.py script is saved to pico
# now with OTA ability from my GitHub (alpha6321)
#
# Phil J Aug 23

#
# Pin's for I2C can be set almost arbitrary, just ensure in same I2C(group)
#
from machine import Pin, I2C
import sh1106, time
from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

firmware_url = "https://raw.githubusercontent.com/alpha6321/Ota/"
ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
ota_updater.download_and_install_update_if_available()

i2c = I2C(0,scl=Pin(17), sda=Pin(16), freq=400000) # used 2 x 4K7 pull-ups
display = sh1106.SH1106_I2C(128, 64, i2c)
display.sleep(False)
display.flip(1)

potentiometer = machine.ADC(26)
conversion_factor = 3.3 / (65535)
sw = Pin(15, Pin.IN, Pin.PULL_UP)

while sw():
    sum = 0
    for i in range(5):
        sum = sum + potentiometer.read_u16()
    Vmean = sum/5*conversion_factor
    Ref_Voltage = 3.26 # Check with DVM
    resistor1 = 10000
    resistor2 = ((Vmean*resistor1)/(Ref_Voltage-Vmean))
    Rstr = str(resistor2)
    display.fill(0)
    display.text("'RUT' = ", 0, 0, 1)  #character size default = 8x8 pixels
    display.text(Rstr + ' OHMS', 6, 12, 1)   #second line in this case starts as row 12 (pixel from top)
    display.show()
    time.sleep(0.75)
    
print("done")
