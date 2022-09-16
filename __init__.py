import badge
import display
import buttons
import system
import math
from random import randint, random
import time

# Initialize the badge
badge.init()
badge.eink_init()
badge.leds_init()

# NVS variables
brightness = badge.nvs_get_u8("rainbowleds", "brightness", 20)
offset = badge.nvs_get_u8("rainbowleds", "offset", 0)
speed = badge.nvs_get_u8("rainbowleds", "speed", 20)
mode = badge.nvs_get_u8("rainbowleds", "mode", 0)

# Global variables
loop = True

# Functions
def save():
    badge.nvs_set_u8("rainbowleds", "brightness", brightness)
    badge.nvs_set_u8("rainbowleds", "offset", offset)
    badge.nvs_set_u8("rainbowleds", "speed", speed)
    badge.nvs_set_u8("rainbowleds", "mode", mode)

def wheel(WheelPos):
    WheelPos = 255 - WheelPos
    if(WheelPos < 85):
        return bytes([255 - WheelPos * 3, 0, WheelPos * 3, 0])
    
    if(WheelPos < 170):
        WheelPos -= 85
        return  bytes([0, WheelPos * 3, 255 - WheelPos * 3, 0])

    WheelPos -= 170
    return  bytes([WheelPos * 3, 255 - WheelPos * 3, 0, 0])

    
def centerText(text, y, color, font):
    textwidth = display.getTextWidth(text, "roboto_blackitalic24")
    display.drawText(math.ceil((display.width()-textwidth)/2), y, text, color, font)


# Button functions
def onStart(pushed):
    if(pushed):
        global brightness
        global offset
        save()
        system.home()

def onSelect(pushed):
    if(pushed):
        global loop
        save()
        loop = False

def onA(pushed):
    if(pushed):
        global mode
        mode = mode+1
        if mode > 3:
            mode = 0

def onB(pushed):
    if(pushed):
        pass

def onUp(pushed):
    if(pushed):
        global brightness
        brightness += 20
        if brightness > 255:
            brightness = 255

def onDown(pushed):
    if(pushed):
        global brightness
        brightness -= 20
        if brightness < 5:
            brightness = 5

def onRight(pushed):
    if(pushed):
        global offset
        global speed
        if mode != 0:
            speed -= 1
            if speed < 1:
                speed = 1
        else:
            offset += 1
            if offset > 5:
                offset = 0

def onLeft(pushed):
    if(pushed):
        global offset
        global speed
        if mode != 0:
            speed += 1
            if speed > 200:
                speed = 200
        else:
            offset -= 1
            if offset < 0:
                offset = 5



display.drawFill(0x000000)
display.flush() 
display.drawFill(0xFFFFFF) 
display.flush() 


centerText("HACK", 15, 0x000000, "roboto_blackitalic24")
centerText("THE", 35, 0x000000, "roboto_blackitalic24")
centerText("BADGE", 55, 0x000000, "roboto_blackitalic24")

display.drawText(0, 90, "START: exit", 0x000000, "roboto_regular12")
display.drawText(0, 100, "UP/DOWN: brightness", 0x000000, "roboto_regular12")
display.drawText(0, 110, "LEFT/RIGHT: move", 0x000000, "roboto_regular12")
display.flush() 

badge.leds_enable()

buttons.attach(buttons.BTN_A, onA)
buttons.attach(buttons.BTN_B, onB)
buttons.attach(buttons.BTN_UP, onUp)
buttons.attach(buttons.BTN_DOWN, onDown)
buttons.attach(buttons.BTN_LEFT, onLeft)
buttons.attach(buttons.BTN_RIGHT, onRight)
buttons.attach(buttons.BTN_START, onStart)
buttons.attach(buttons.BTN_SELECT, onSelect)

j = 0

while loop:
    # create_colors()
    if(mode == 0):
        blue = bytes([0, 0, brightness, 0])
        cyan = bytes([brightness, 0, brightness, 0])
        green = bytes([brightness, 0, 0, 0])
        yellow = bytes([brightness, brightness, 0, 0])
        red = bytes([0, brightness, 0, 0])
        magenta = bytes([0, brightness, brightness, 0])
        rainbow = [blue, cyan, green, yellow, red, magenta]
        values = bytes()
        for i in range(6):
            i += offset
            if i > 5:
                i -= 6
            values += rainbow[i]
        badge.leds_send_data(values)

    elif(mode == 1):
        ledData = b""
        for i in range(6):
            ledData += wheel((i+j) & 255)

        badge.leds_send_data(ledData)
        time.sleep_us(speed*100)
        j = j+1
        if j > 255:
            j = 0

    elif(mode == 2):
        ledData = b""
        for i in range(6):
            ledData += wheel((math.ceil(i * 256 / 6) + j) & 255)

        badge.leds_send_data(ledData)
        time.sleep_us(speed*100)

        j = j+1
        if j > 256*5:
            j = 0

    else:
        badge.leds_send_data(bytes([0, 0, 0, brightness, 0, 0, 0, brightness, 0, 0, 0, brightness, 0, 0, 0, brightness, 0, 0, 0, brightness, 0, 0, 0, brightness]))



# badge.leds_send_data(leds_array)
# time.sleep_ms(100)

# leds_array = leds_array[4:] + bytes([randint(0, 128), randint(0, 255), randint(128, 255), 0])

# # First test
# display.drawFill(0x000000) # Fill the screen with black
# display.drawText(10, 10, "Hello world!", 0xFFFFFF, "permanentmarker22") # Draw the text "Hello world!" at (10,10) in white with the PermanentMarker font with size 22
# display.flush() # Write the contents of the buffer to the display

# def message(text):
# 	print(text)
# 	display.drawFill(0xFFFFFF)
# 	display.drawText(0,0, text, 0x000000, "7x5")
# 	display.flush()

# def myCallback(pressed):
# 	if pressed:
# 		message("Pressed!")
# 	else:
# 		message("Released!")

# buttons.attach(buttons.BTN_A, myCallback)
# buttons.attach(buttons.BTN_A, myCallback)
# buttons.attach(buttons.BTN_A, myCallback)
# buttons.attach(buttons.BTN_A, myCallback)
# buttons.attach(buttons.BTN_A, myCallback)
# buttons.attach(buttons.BTN_A, myCallback)

# message("Press the A button!")

# # # Set the button callback
# # def on_action_btn(pressed): # Defines a function on_action_btn with the required parameter pressed
# #     if pressed: # Uses an if statement to check if the button has been pressed
# #         display.drawFill(display.BLACK) # If the button is pressed, sets the screen to black
# #         display.drawText(10,10,"Hack The Planet!!!", 0xFFFFFF, "permanentmarker22") # Draws text if the button is pressed
# #         display.flush() # Flushes the screen to draw the text and color onto the screen

# # buttons.attach(buttons.BTN_A, on_action_btn) # Assigns the function on_action_btn to the A button

# # badge.leds_enable()

# # leds_array = bytes(24)

# # while True:
# #     badge.leds_send_data(leds_array)
# #     time.sleep(0.1)
# #     leds_array = leds_array[4:] + bytes([randint(128, 255), randint(0, 255), randint(0, 128), 0])
# #     badge.leds_send_data(leds_array)
# #     time.sleep(0.1)
# #     leds_array = leds_array[4:] + bytes([randint(0, 128), randint(0, 255), randint(128, 255), 0])