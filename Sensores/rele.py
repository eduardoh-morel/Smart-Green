import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
releIn1 = 2  # Define o número do pino do primeiro relé Usado para Irrigacao
releIn2 = 4  # Define o número do pino do segundo relé Usado para Ventilacao

GPIO.setup(releIn1, GPIO.OUT)
GPIO.setup(releIn2, GPIO.OUT)

def ligar_rele():
    GPIO.output(releIn1, GPIO.HIGH)
    print("Relé de Irrigacao ligado")

def ligar_rele():
    GPIO.output(releIn2, GPIO.HIGH)
    print("Relé de Ventilacao ligado")

def desligar_rele():
    GPIO.output(releIn1, GPIO.LOW)
    print("Relé de Irrigacao desligado")
    

def desligar_rele():
    GPIO.output(releIn2, GPIO.LOW)
    print("Relé de Ventilacao desligado")

def cleanup_gpio():
    GPIO.cleanup()
    print("Limpeza dos GPIOs realizada.")

try:
    ligar_rele()
    time.sleep(5)
    desligar_rele()

finally:
    GPIO.cleanup()
