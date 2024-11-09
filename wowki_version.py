from machine import Pin, I2C, ADC, Timer
from nec import NEC_16
from neopixel import NeoPixel
from time import sleep
import random

ldr = ADC(Pin(26))

rgb_led_num =   22
rgb_led_pin =   Pin(rgb_led_num, Pin.OUT)
rgb_led     =   NeoPixel(rgb_led_pin, 1) 


led = Pin(25,Pin.OUT)

isLDRActive = False

ldr_timer = Timer()

def remoteSwitch(data, addr, ctrl):
    global readCount, isLDRActive
    if data > 0:
        if data == 0xa2:
            if  rgb_led[0]==(0,0,0):
                LightSwitchOn()
            else:
                LightSwitchOff()

        if data == 0xa8:
            if led.value() == 1:
                led.value(0)
                print("LDR OFF")
                isLDRActive = False
            else:
                led.value(1)
                print("LDR ON")
                isLDRActive = True
                # Start the timer to periodically check LDR conditions
                ldr_timer.init(period=2000, mode=Timer.PERIODIC, callback=readLDR)

        print('data {:02x}'.format(data))



ir = NEC_16(Pin(15,Pin.IN),remoteSwitch)



def LightSwitchOff():
  rgb_led[0]=(0,0,0)
  rgb_led.write()


def LightSwitchOn():
     
    r= random.randint(0, 255)
    g = random.randint(0, 255)
    b =random.randint(0, 255)

    print("r", r)
    print("g", g)
    print("b", b)

    rgb_led[0]=(r,g,b) 
    rgb_led.write() 
    r=0
    g=0
    b=0


def getLedValue():
    return led.value()
voltage     = ldr.read_u16()*3.3/65535
#resistance  = ((10*3.3)/voltage)-10
print(voltage)

def readLDR(timer):
    global isLDRActive
    if isLDRActive:
        voltage = ldr.read_u16() * 3.3 / 65535
        x = int(voltage)
        if x > 0:
            LightSwitchOn()
            print("reading ", ":", "night")
        else:
            LightSwitchOff()
            print("reading ", ":", "Day")
    else:
        # Turn off LDR and stop the timer after exiting the loop
        led.value(0)
        ldr_timer.deinit()
        print("LDR Switch OFF")
        

    


