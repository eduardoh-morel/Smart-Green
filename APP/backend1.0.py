import serial
import time

serial_port = '/dev/ttyACM0'
baud_rate = 9600

ser = None

# Variáveis para armazenar os dados
temperatura = None
umidade = None
co2 = None
umidade_solo = None

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print("Conexão estabelecida com o Arduino!")

    while True:
        if ser.in_waiting > 0:
            time.sleep(5)
            data = ser.readline().decode('utf-8').strip()

            if "Temperatura:" in data:
                temperatura = int(data.split(":")[1].strip())
            elif "Umidade:" in data:
                umidade = int(data.split(":")[1].strip())
            elif "CO2:" in data:
                co2 = int(data.split(":")[1].strip())
            elif "Umidade do Solo:" in data:
                umidade_solo = int(data.split(":")[1].strip())

            print(f"Temperatura: {temperatura}")
            print(f"Umidade: {umidade}")
            print(f"CO2: {co2}")
            print(f"Umidade do Solo: {umidade_solo}")

except serial.SerialException:
    print("Não foi possível conectar ao Arduino.")
finally:
    if ser and ser.is_open:
        ser.close()
        print("Conexão serial fechada.")
