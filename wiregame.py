from gpiozero import LightSensor, Buzzer    # Importiere die LightSensor-Klasse von der gpiozero-Bibliothek
import requests                             # um HTTP-Anfragen zu senden
import RPi.GPIO as GPIO                     # um die GPIO-Pins des Raspberry Pi zu steuern
from mfrc522 import SimpleMFRC522           # um das Arbeiten mit RFID-Lesegeräten zu ermöglichen

reader = SimpleMFRC522()     # Objekt der Klasse FRC522 wird instanziiert
try:
    id, text = reader.read() # read() Methode des reader-Objektes wird ausgeführt
    if id == 842313244175:   # Eindeutige ID der von uns verwendeten RFID-Karte
        print('Richtige Karte')
        url = 'hhtp://192.168.213.6:5000/set-game/Anleitung-Lichtergame' # Request um die Anleitung auf der Webiste erscheinen zu lassen
        try:
            response = requests.post(url, timeout=5) # Request an die API wird gesendet
            print("Gesendet!")
        except requests.exceptions.Timeout:
            print("Die Anfrage hat zu lange gedauert und wurde abgebrochen.")
finally:
    GPIO.cleanup()          # GPIO-Pins zurücksetzen
    ldr = LightSensor(4)    # Instanz der Klasse LightSensor erstellen

    bedingung = True
    while bedingung:            # Durchgängige überprüfung ob die LED an ist oder nicht

        if ldr.value > 0.2: # 0.2 => zuverlässiger Wert, ldr.value ist nur dann größer als 0.2, wenn die LED an ist
            url = 'http://192.168.213.6:5000/set-game/Lichtergame' # wenn LED an ist wird der Request für die Tür gesendet
            try:
                response = requests.post(url, timeout=5)
                print("Tür auf!")
                bedingung = False   # Schleife wird beendet wenn der Request erfolgreich war
            except requests.exceptions.Timeout:
                print("Die Anfrage hat zu lange gedauer und wurde abgebrochen.")