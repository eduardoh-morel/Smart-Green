from flask import Flask, render_template, jsonify
import serial

app = Flask(__name__)

serial_port = '/dev/ttyACM0'
baud_rate = 9600

temperatura = None
umidade = None
co2 = None
umidade_solo = None

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print("Conexão estabelecida com o Arduino!")
except serial.SerialException:
    print("Não foi possível conectar ao Arduino.")
    ser = None

def read_sensor_data():
    global temperatura, umidade, co2, umidade_solo
    if ser and ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        
        if "Temperatura:" in data:
            temperatura = int(data.split(":")[1].strip())
            temperatura= str(temperatura) + " °C"
        elif "Umidade:" in data:
            umidade = int(data.split(":")[1].strip())
            umidade= str(umidade) + " %"
        elif "CO2:" in data:
            co2 = int(data.split(":")[1].strip())
            co2= str(co2) + " ppm"
        elif "Umidade do Solo:" in data:
            umidade_solo = int(data.split(":")[1].strip())

@app.route("/")
def home():
    return render_template('GreenTech.html')

@app.route("/sensorData")
def sensor_data():
    # Atualizar os dados do sensor antes de enviá-los
    read_sensor_data()
    
    # Retornar os dados como JSON
    return jsonify({
        "temperatura": temperatura,
        "umidade": umidade,
        "co2": co2,
        "umidade_solo": umidade_solo
    })

if __name__ == '__main__':
    app.run(host='10.1.24.200', port=8080)
