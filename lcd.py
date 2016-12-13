#!/usr/bin/python

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
from pyA20.gpio import gpio
from pyA20.gpio import port
import time

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
LCD_KEY = 22 

lcd_key     = 0
adc_key_in  = 0

btnRIGHT  = 0
btnUP     = 1
btnDOWN   = 2
btnLEFT   = 3
btnSELECT = 4
btnNONE   = 5

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


gpio.init()

def read_LCD_buttons():
	adc_key_in = gpio.setcfg(LCD_KEY, gpio.OUTPUT)  
	if (adc_key_in > 1000): return btnNONE
	if (adc_key_in < 50):   return btnRIGHT  
	if (adc_key_in < 250):  return btnUP
	if (adc_key_in < 450):  return btnDOWN 
	if (adc_key_in < 650):  return btnLEFT 
	if (adc_key_in < 850):  return btnSELECT  

def main():
  # Main program block
  gpio.setcfg(LCD_E, gpio.OUTPUT)  # E
  gpio.setcfg(LCD_RS, gpio.OUTPUT) # RS
  gpio.setcfg(LCD_D4, gpio.OUTPUT) # DB4
  gpio.setcfg(LCD_D5, gpio.OUTPUT) # DB5
  gpio.setcfg(LCD_D6, gpio.OUTPUT) # DB6
  gpio.setcfg(LCD_D7, gpio.OUTPUT) # DB7
 
  # Initialise display
  while True:
    # Send some test
    lcd_string("Rasbperry Pi",LCD_LINE_1)
    lcd_string("16x2 LCD Test",LCD_LINE_2)
    time.sleep(3) # 3 second delay
    lcd_key = read_LCD_buttons()
    print (lcd_key)
    if lcd_key == btnRIGHT: print ('key')

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
  gpio.output(LCD_RS, mode) # RS
  # High bits
  gpio.output(LCD_D4, False)
  gpio.output(LCD_D5, False)
  gpio.output(LCD_D6, False)
  gpio.output(LCD_D7, False)
  if bits&0x10==0x10:
    gpio.output(LCD_D4, True)
  if bits&0x20==0x20:
    gpio.output(LCD_D5, True)
  if bits&0x40==0x40:
    gpio.output(LCD_D6, True)
  if bits&0x80==0x80:
    gpio.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  gpio.output(LCD_D4, False)
  gpio.output(LCD_D5, False)
  gpio.output(LCD_D6, False)
  gpio.output(LCD_D7, False)
  if bits&0x01==0x01:
    gpio.output(LCD_D4, True)
  if bits&0x02==0x02:
    gpio.output(LCD_D5, True)
  if bits&0x04==0x04:
    gpio.output(LCD_D6, True)
  if bits&0x08==0x08:
    gpio.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  gpio.output(LCD_E, True)
  time.sleep(E_PULSE)
  gpio.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

main()
lcd_byte(0x01, LCD_CMD)
lcd_string("Goodbye!",LCD_LINE_1)
gpio.cleanup()
