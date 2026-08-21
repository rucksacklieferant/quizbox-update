from machine import Pin, PWM
import time

# Onboard-LED bei Pico W / Pico 2 WH einschalten
onboard_led = Pin("LED", Pin.OUT)
onboard_led.value(1) # 1 = an, 0 = aus

# ==========================================
# 1. HARDWARE-PINBELEGUNG
# ==========================================

# Taster (Eingänge mit internem Pull-Up, schalten gegen GND)
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

# Raum-RGB-Streifen (PWM über MOSFETs auf GP11, GP12, GP13)
pwm_red = PWM(Pin(11))
pwm_green = PWM(Pin(12))
pwm_blue = PWM(Pin(13))

# PWM-Frequenz auf 1000 Hz setzen (flackerfrei für das Auge)
pwm_red.freq(1000)
pwm_green.freq(1000)
pwm_blue.freq(1000)

# Alle Buzzer-LEDs in eine Liste packen
leds = [led1, led2, led3, led4]

# ==========================================
# 2. HILFSFUNKTIONEN FÜR DIE BELEUCHTUNG
# ==========================================

def set_raum_farbe(r_percent, g_percent, b_percent):
    """
    Setzt die Raumfarbe über PWM.
    Eingabe: Prozentwerte von 0 bis 100 für Rot, Grün und Blau.
    """
    pwm_red.duty_u16(int(r_percent / 100 * 65535))
    pwm_green.duty_u16(int(g_percent / 100 * 65535))
    pwm_blue.duty_u16(int(b_percent / 100 * 65535))

def alle_buzzer_lichter(status):
    """Schaltet alle 4 Buzzer-Lichter an (1) oder aus (0)"""
    for led in leds:
        led.value(status)

def reset_spiel():
    """Setzt das System in den Startzustand zurück"""
    alle_buzzer_lichter(0)
    # Raumlicht auf helles Neutrallicht/Weiß (z. B. 80% Rot, 80% Grün, 80% Blau)
    set_raum_farbe(80, 80, 80)

# ==========================================
# 3. HAUPTPROGRAMM (SPIELLOGIK)
# ==========================================

print("Quiz-Box gestartet und bereit (mit PWM-Licht)!")
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
        
        # Spieler 1: ROT
        if buzzer1.value() == 0:
            box_gesperrt = True
            led1.value(1)
            set_raum_farbe(100, 0, 0) # 100% Rot
            print("Spieler 1 hat gebuzzert!")
            time.sleep_ms(50)
            
        # Spieler 2: GRÜN
        elif buzzer2.value() == 0:
            box_gesperrt = True
            led2.value(1)
            set_raum_farbe(0, 100, 0) # 100% Grün
            print("Spieler 2 hat gebuzzert!")
            time.sleep_ms(50)
            
        # Spieler 3: BLAU
        elif buzzer3.value() == 0:
            box_gesperrt = True
            led3.value(1)
            set_raum_farbe(0, 0, 100) # 100% Blau
            print("Spieler 3 hat gebuzzert!")
            time.sleep_ms(50)
            
        # Spieler 4: GELB (Mischung aus Rot und Grün)
        elif buzzer4.value() == 0:
            box_gesperrt = True
            led4.value(1)
            set_raum_farbe(100, 60, 0) # 100% Rot + 60% Grün = Schönes Warmgelb
            print("Spieler 4 hat gebuzzert!")
            time.sleep_ms(50)

    time.sleep_ms(1) # Kurze Pause zur CPU-Entlastung
