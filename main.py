from machine import Pin
import time

# ==========================================
# 1. HARDWARE-PINBELEGUNG (Am Expander)
# ==========================================

# Taster (Eingänge mit internem Pull-Up)
buzzer1 = Pin(2, Pin.IN, Pin.PULL_UP)
buzzer2 = Pin(3, Pin.IN, Pin.PULL_UP)
buzzer3 = Pin(4, Pin.IN, Pin.PULL_UP)
buzzer4 = Pin(5, Pin.IN, Pin.PULL_UP)
reset_button = Pin(6, Pin.IN, Pin.PULL_UP)

# Buzzer-Lichter (Ausgänge über ULN2003A)
led1 = Pin(7, Pin.OUT)
led2 = Pin(8, Pin.OUT)
led3 = Pin(9, Pin.OUT)
led4 = Pin(10, Pin.OUT)

# Raum-RGB-Streifen (Ausgänge über MOSFETs)
rgb_red = Pin(11, Pin.OUT)
rgb_green = Pin(12, Pin.OUT)
rgb_blue = Pin(13, Pin.OUT)

# Alle Lampen-Objekte in Listen packen für einfache Ansteuerung
leds = [led1, led2, led3, led4]

# ==========================================
# 2. HILFSFUNKTIONEN FÜR DIE BELEUCHTUNG
# ==========================================

def set_raum_farbe(r, g, b):
    """Setzt die Farbe des großen Raum-RGB-Streifens (1 = an, 0 = aus)"""
    rgb_red.value(r)
    rgb_green.value(g)
    rgb_blue.value(b)

def alle_buzzer_lichter(status):
    """Schaltet alle 4 Buzzer-Lichter an (1) oder aus (0)"""
    for led in leds:
        led.value(status)

def reset_spiel():
    """Setzt das System in den Startzustand zurück"""
    alle_buzzer_lichter(0)
    # Raumlicht auf Standard (z. B. Weiß: Rot+Grün+Blau)
    set_raum_farbe(1, 1, 1)

# ==========================================
# 3. HAUPTPROGRAMM (SPIELLOGIK)
# ==========================================

print("Quiz-Box gestartet und bereit!")
reset_spiel()

box_gesperrt = False

while True:
    # --- RESET-PRÜFUNG ---
    if reset_button.value() == 0:
        box_gesperrt = False
        reset_spiel()
        print("Spiel zurückgesetzt!")
        time.sleep_ms(300) # Entprellen

    # --- BUZZER-ABFRAGE ---
    if not box_gesperrt:
        
        # Spieler 1
        if buzzer1.value() == 0:
            box_gesperrt = True
            led1.value(1)
            set_raum_farbe(1, 0, 0) # Raum leuchtet z. B. Rot auf
            print("Spieler 1 hat gebuzzert!")
            
        # Spieler 2
        elif buzzer2.value() == 0:
            box_gesperrt = True
            led2.value(1)
            set_raum_farbe(0, 1, 0) # Raum leuchtet Grün
            print("Spieler 2 hat gebuzzert!")
            
        # Spieler 3
        elif buzzer3.value() == 0:
            box_gesperrt = True
            led3.value(1)
            set_raum_farbe(0, 0, 1) # Raum leuchtet Blau
            print("Spieler 3 hat gebuzzert!")
            
        # Spieler 4
        elif buzzer4.value() == 0:
            box_gesperrt = True
            led4.value(1)
            set_raum_farbe(1, 1, 0) # Raum leuchtet Gelb
            print("Spieler 4 hat gebuzzert!")

    time.sleep_ms(1) # Kurze Pause zur CPU-Entlastung
