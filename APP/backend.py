from flask import Flask, render_template, jsonify, request
import serial
import threading
import time
import discord
import asyncio
from discord.ext import commands
from botKey import *
from datetime import datetime, timedelta
import RPi.GPIO as GPIO


app = Flask(__name__)

serial_port = '/dev/ttyACM0'
baud_rate = 9600

#Configuracao de Pin 

GPIO.setmode(GPIO.BCM)
releIn1 = 2  # Define o número do pino do primeiro relé Usado para Irrigacao
releIn2 = 4  # Define o número do pino do segundo relé Usado para Ventilacao
GPIO.setup(releIn1, GPIO.OUT)
GPIO.setup(releIn2, GPIO.OUT)


# Configuração do Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def ligarReleIrrigacao():
    GPIO.output(releIn1, GPIO.HIGH)
    print("Relé de Irrigacao ligado")

def ligarReleVentilacao():
    GPIO.output(releIn2, GPIO.HIGH)
    print("Relé de Ventilacao ligado")

def desligarReleIrrigacao():
    GPIO.output(releIn1, GPIO.LOW)
    print("Relé de Irrigacao desligado")
    
def desligarReleVentilacao():
    GPIO.output(releIn2, GPIO.LOW)
    print("Relé de Ventilacao desligado")

def cleanup_gpio():
    GPIO.cleanup()
    print("Limpeza dos GPIOs realizada.")
    
# Variaveis dos sensores
temperatura = None
umidade = None
co2 = None
umidade_solo = None

# Variaveis dos sensores
temperaturaReal = None
umidadeReal = None
co2Real = None
umidadeSoloReal = None

# Variaveis recebidas para desejaveis
valores_desejaveis = {
    "temperatura": "",
    "umidade": "",
    "co2": "",
    "umidadeSolo": ""   
}

#Variaveis convertidas para numeros Int
def safe_int(valor):
    return int(valor) if valor not in (None, "") else 0

# Status variam de Ligado / Desligado
statusIrrigation = {
    "status": "Desligado",
}

statusIrrigationByNeed = {
    "status": "Desligado",
}

statusVentilation = {
    "status": "Desligado",
}

statusVentilationByNeed = {
    "status": "Desligado",
}

agendamentosIrrigacao = []

@app.route('/agendarIrrigacao', methods=['POST'])
def agendar_irrigacao():
    data = request.get_json()
    horario = data.get('horario')
    duracao = data.get('duracao')

    if not horario or not duracao:
        return jsonify({"message": "Horário ou duração não fornecidos!"}), 400

    agendamento = {
        "horario": horario,
        "duracao": duracao,
        "status": "Agendado"
    }
    agendamentosIrrigacao.append(agendamento)
    return jsonify({"message": "Irrigação agendada com sucesso!"}), 200

@app.route('/listarAgendamentos', methods=['GET'])
def listar_agendamentos():
    return jsonify({"agendamentos": agendamentosIrrigacao}), 200

@app.route('/removerAgendamento/<int:index>', methods=['DELETE'])
def remover_agendamento(index):
    if 0 <= index < len(agendamentosIrrigacao):
        agendamentosIrrigacao.pop(index)
        return jsonify({"message": "Agendamento removido com sucesso!"}), 200
    else:
        return jsonify({"message": "Agendamento não encontrado!"}), 404

lock = threading.Lock()

def verificar_agendamentos():
    print("###Iniciando verificação de Agendamentos###")
    while True:
        agora = datetime.now()
        for agendamento in agendamentosIrrigacao:
            horario_agendamento = datetime.strptime(agendamento['horario'], '%H:%M')
            horario_agendamento = horario_agendamento.replace(year=agora.year, month=agora.month, day=agora.day)
            
            if horario_agendamento <= agora < horario_agendamento + timedelta(minutes=1) and agendamento['status'] == "Agendado":
                with lock:
                    statusIrrigation['status'] = "Ligado"
                    agendamento['status'] = "Em execução"
                print(f"Irrigação ligada para o agendamento: {agendamento['horario']}")
                ligarReleIrrigacao()
                
                threading.Timer(agendamento['duracao'] * 60, desligar_irrigacao).start()

        time.sleep(60)

def desligar_irrigacao():
    with lock:
        statusIrrigation['status'] = "Desligado"
    desligarReleIrrigacao()
    cleanup_gpio()
    print("Irrigação desligada.")

threading.Thread(target=verificar_agendamentos, daemon=True).start()

@app.route('/hasSchedule', methods=['GET'])
def has_schedule():
    return jsonify({"has_schedule": len(agendamentosIrrigacao) > 0}), 200

@app.route('/ventilationStatus', methods=['GET'])
def get_ventilation_status():
    print(f"Estado atual da Ventilação: {statusVentilation}")
    return jsonify(statusVentilation), 200

@app.route('/ventilationStatus', methods=['POST'])
def update_ventilation_status():
    data = request.get_json()
    
    if 'status' in data:
        statusVentilation['status'] = data['status']
        return jsonify({"message": "Status da ventilação atualizado com sucesso!"}), 200
    else:
        return jsonify({"message": "Status não fornecido!"}), 400

@app.route('/ventilationByNeed', methods=['GET'])
def get_ventilation_by_need():
    return jsonify(statusVentilationByNeed), 200

@app.route('/IrrigationByNeed', methods=['GET'])
def get_irrigation_by_need():
    return jsonify(statusIrrigationByNeed), 200

@app.route('/irrigationStatus', methods=['GET'])
def get_irrigation_status():
    print(f"Estado atual da irrigação: {statusIrrigation}")
    return jsonify(statusIrrigation), 200

@app.route('/irrigationStatus', methods=['POST'])
def update_irrigation_status():
    data = request.get_json()
    
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

sensor_lock = threading.Lock()

def read_sensor_data():
    global temperatura, umidade, co2, umidade_solo

    with sensor_lock:
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
                umidade_solo= str(umidade_solo) + " %"

#Dados reais para consumo de verificação
def read_sensor_data_real():
    global temperaturaReal, umidadeReal, co2Real, umidadeSoloReal

    with sensor_lock:
        if ser and ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            
            if "Temperatura:" in data:
                temperaturaReal = int(data.split(":")[1].strip())
            elif "Umidade:" in data:
                umidadeReal = int(data.split(":")[1].strip())
            elif "CO2:" in data:
                co2Real = int(data.split(":")[1].strip())
            elif "Umidade do Solo:" in data:
                umidadeSoloReal = int(data.split(":")[1].strip())

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

@app.route("/ventilation.html")
def ventilation():
    return render_template('ventilation.html')

#read_sensor_data_real()

@app.route("/sensorData")
def sensor_data():
    read_sensor_data()
    
    return jsonify({
        "temperatura": temperatura,
        "umidade": umidade,
        "co2": co2,
        "umidade_solo": umidade_solo
    })

def monitor_sensors():
    while True:
        read_sensor_data_real()
        print("###Lendo sensores com dados reais###")
        time.sleep(5)

def start_monitoring():
    monitor_thread = threading.Thread(target=monitor_sensors, daemon=True)
    monitor_thread.start()
 
 
@bot.event
async def on_ready():
    print("--------------------------------------------")
    print('Bot Online')
    print(bot.user.name, bot.user.id)
    print("--------------------------------------------")
    # Iniciar as verificações de todas as condições Desejaveis
    bot.loop.create_task(verificacaoTemp())
    bot.loop.create_task(verificacaoUmidadeSolo())
    bot.loop.create_task(verificacaoCO2())
    bot.loop.create_task(verificacaoUmidadeAr())
 

# Função de verificação de temperatura
async def verificacaoTemp():
    channel = bot.get_channel(1300961217845792820)  # ID do canal onde o bot deve enviar a mensagem

    try:
        while True: 
            # Verificação de Temperatura
            tempDesejavelInt = safe_int(valores_desejaveis.get("temperatura", 0))
            temperaturaRealInt = safe_int(temperaturaReal) if temperaturaReal is not None else 0

            if tempDesejavelInt != 0 and temperaturaRealInt > tempDesejavelInt:
                # Liga o relé se a temperatura exceder o limite
                ligarReleVentilacao()
                #Status
                statusVentilation['status'] = "Ligado"
                statusVentilationByNeed['status'] = "Ligado"
                
                # Envio de Mensagem do Bot
                embed = discord.Embed(
                    title="⚠️ Alerta de Temperatura",
                    description="A temperatura atual excedeu o limite desejado.",
                    color=discord.Color.red()
                )
                embed.add_field(name="Temperatura Atual", value=f"{temperaturaRealInt}°C", inline=True)
                embed.add_field(name="Temperatura Desejada", value=f"{tempDesejavelInt}°C", inline=True)
                embed.set_footer(text="Monitoramento de Temperatura")
            
                await channel.send(embed=embed)
            
            else:
                # Desliga o relé se a temperatura estiver dentro do limite
                desligarReleVentilacao()
                #Status
                statusVentilation['status'] = "Desligado"
                statusVentilationByNeed['status'] = "Desligado"
                
            await asyncio.sleep(60)

    finally:
        GPIO.cleanup()  # Limpeza do GPIO
        

# Função de verificação da umidade do solo
async def verificacaoUmidadeSolo():
    channel = bot.get_channel(1300961217845792820)  # ID do canal onde o bot enviará a mensagem

    try:
        while True:
            # Umidade do Solo
            umidadeSoloRealInt = safe_int(umidadeSoloReal) if umidadeSoloReal is not None else 0
            umidadeSoloDesejavelInt = safe_int(valores_desejaveis.get("umidadeSolo", 0))

            # Verificação: Umidade do Solo Atual menor que o valor desejável
            if umidadeSoloDesejavelInt != 0 and umidadeSoloRealInt < umidadeSoloDesejavelInt:
                # Liga o relé de irrigação se a umidade do solo estiver abaixo do limite
                ligarReleIrrigacao()  # Liga o relé de irrigação
                #Status
                statusIrrigation['status'] = "Ligado"
                statusIrrigationByNeed['status'] = "Ligado"
                

                embed = discord.Embed(
                    title="⚠️ Alerta de Umidade do Solo",
                    description="A umidade do solo atual está abaixo do limite desejado.",
                    color=discord.Color.gold()
                )
                embed.add_field(name="Umidade do Solo Atual", value=f"{umidadeSoloRealInt}%", inline=True)
                embed.add_field(name="Umidade do Solo Desejada", value=f"{umidadeSoloDesejavelInt}%", inline=True)
                embed.set_footer(text="Monitoramento de Umidade do Solo")
                
                await channel.send(embed=embed)
            else:
                # Desliga o relé de irrigação se a umidade do solo estiver no limite desejado
                desligarReleIrrigacao()  # Desliga o relé de irrigação
                #Status
                statusIrrigation['status'] = "Desligado"
                statusIrrigationByNeed['status'] = "Desligado"
                

            await asyncio.sleep(60)  # Verificação a cada 60 segundos

    finally:
        GPIO.cleanup()  # Limpeza do GPIO 
    
# Verificação de CO2
async def verificacaoCO2():
    channel = bot.get_channel(1300961217845792820)

    while True:
        # Co2
        # Verificacao sendo Feita = Co2 Atual maior que Desejavel
        co2RealInt = safe_int(co2Real) if co2Real is not None else 0
        co2DesejavelInt = safe_int(valores_desejaveis.get("co2", 0))
        
        if co2DesejavelInt != 0 and co2RealInt > co2DesejavelInt: # Co2 Atual maior que Desejavel
            embed = discord.Embed(
                title="⚠️ Alerta de CO2",
                description="O nível de CO2 atual está acima do limite desejado.",
                color=discord.Color.purple()
            )
            embed.add_field(name="CO2 Atual", value=f"{co2RealInt} ppm", inline=True)
            embed.add_field(name="CO2 Desejado", value=f"{co2DesejavelInt} ppm", inline=True)
            embed.set_footer(text="Monitoramento de CO2")
        
            await channel.send(embed=embed)
        await asyncio.sleep(60)

# Verificação de Umidade do Ar
async def verificacaoUmidadeAr():
    channel = bot.get_channel(1300961217845792820)

    while True:
        # Umidade do Ar
        # Verificacao sendo Feita = Umidade do Ar Atual Maior que Desejavel
        umidadeRealInt = safe_int(umidadeReal) if umidadeReal is not None else 0
        umidadeDesejavelInt = safe_int(valores_desejaveis.get("umidade", 0))

        if umidadeDesejavelInt != 0 and umidadeRealInt > umidadeDesejavelInt: # Umidade Atual Maior que Desejavel
            embed = discord.Embed(
                title="⚠️ Alerta de Umidade do Ar",
                description="A umidade do ar atual está acima do limite desejado.",
                color=discord.Color.green()
            )
            embed.add_field(name="Umidade do Ar Atual", value=f"{umidadeRealInt}%", inline=True)
            embed.add_field(name="Umidade do Ar Desejada", value=f"{umidadeDesejavelInt}%", inline=True)
            embed.set_footer(text="Monitoramento de Umidade do Ar")
        
            await channel.send(embed=embed)
        await asyncio.sleep(60)
        
# Comando de limpeza com divisão em blocos
@bot.command(name='limpar')
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int):
    if quantidade > 2000:
        await ctx.send("Só posso deletar até 2000 mensagens de uma vez!")
    else:
        total_deletadas = 0  # Variável para contar as mensagens deletadas
        while quantidade > 0:
            bloco = min(quantidade, 50)  # Define o tamanho do bloco
            deletadas = await ctx.channel.purge(limit=bloco)
            total_deletadas += len(deletadas)
            quantidade -= bloco
            await asyncio.sleep(1)  # 1 segundo entre os blocos
        await ctx.send(f"{total_deletadas} mensagens foram apagadas!", delete_after=15)  # Mensagem temporária

# Inicializar o Bot em uma thread separada
def iniciar_bot():
    bot.run(bot_token)

# Iniciar o bot do Discord em uma thread
bot_thread = threading.Thread(target=iniciar_bot, daemon=True)
bot_thread.start()
start_monitoring()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)