import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

def ligar_rele():
    GPIO.output(2, GPIO.HIGH)
    print("Relé ligado")


def desligar_rele():
    GPIO.output(2, GPIO.LOW)
    print("Relé desligado")

try:
    ligar_rele()
    time.sleep(5)
    desligar_rele()

finally:
    GPIO.cleanup()
