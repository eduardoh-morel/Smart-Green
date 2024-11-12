from flask import Flask, render_template, jsonify, request
import serial

app = Flask(__name__)

serial_port = '/dev/ttyACM0'
baud_rate = 9600

temperatura = None
umidade = None
co2 = None
umidade_solo = None

valores_desejaveis = {
    "temperatura": "",
    "umidade": "",
    "co2": "",
    "umidadeSolo": ""   
}

statusIrrigation = {
    "status": "Desligado",
}

@app.route('/irrigationStatus', methods=['GET'])
def get_irrigation_status():
    print(f"Estado atual da irrigação: {statusIrrigation}")
    return jsonify(statusIrrigation), 200

@app.route('/irrigationStatus', methods=['POST'])
def update_irrigation_status():
    data = request.get_json()
    
    # Verifica se o status foi enviado corretamente
    if 'status' in data:
        statusIrrigation['status'] = data['status']
        return jsonify({"message": "Status da irrigação atualizado com sucesso!"}), 200
    else:
        return jsonify({"message": "Status não fornecido!"}), 400

@app.route('/getValuesDesirable', methods=['GET'])
def get_initial_values():
    return jsonify(valores_desejaveis), 200

@app.route('/sendDesiredData', methods=['POST'])
def send_desired_data():
    # Receber valores enviados pelo AJAX
    valores_desejaveis["temperatura"] = request.form.get('temperatura')
    valores_desejaveis["umidade"] = request.form.get('umidade')
    valores_desejaveis["co2"] = request.form.get('co2')
    valores_desejaveis["umidadeSolo"] = request.form.get('umidadeSolo')

    print("Valores atualizados:", valores_desejaveis)

    return jsonify({"message": "Dados recebidos com sucesso!"}), 200

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
    return render_template('index.html')

@app.route("/irrigation.html")
def irrigation():
    return render_template('irrigation.html')

@app.route("/GreenTech.html")
def home1():
    return render_template('index.html')

@app.route("/statistics.html")
def statistics():
    return render_template('statistics.html')

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
    app.run(host='10.1.24.200', port=8888)
    
