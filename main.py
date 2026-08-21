from machine import Pin
import time

# 1. Onboard-LED zur Statusanzeige einschalten
pico_led = Pin("LED", Pin.OUT)
pico_led.value(1)

# 2. Pins für den RGB-Streifen definieren
rgb_red = Pin(11, Pin.OUT)
rgb_green = Pin(12, Pin.OUT)
rgb_blue = Pin(13, Pin.OUT)

# 3. Reset-Taster definieren (Pull-Up: schaltet gegen GND)
reset_button = Pin(6, Pin.IN, Pin.PULL_UP)

# --- STARTZUSTAND: BLAU EINSCHALTEN ---
rgb_red.value(0)
rgb_green.value(0)
rgb_blue.value(1) # Blau einschalten
print("Pico gestartet: LED-Streifen leuchtet BLAU!")

# --- WARTEN AUF RESET-KNOPF ---
while True:
    # Wenn Reset-Knopf gedrückt wird (GP6 geht auf 0/GND)
    if reset_button.value() == 0:
        # Alles ausschalten
        rgb_blue.value(0)
        pico_led.value(0)
        print("Reset gedrückt: Blau ausgeschaltet!")
        
        # Schleife beenden / Programm stoppen
        break
    
    time.sleep_ms(10)
