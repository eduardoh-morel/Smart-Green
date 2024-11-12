async function fetchSensorData() {
    try {
        const response = await fetch("/sensorData");
        const data = await response.json();
        
        document.getElementById("temp").textContent = data.temperatura || "N/A";
        document.getElementById("humidity").textContent = data.umidade || "N/A";
        document.getElementById("co2").textContent = data.co2 || "N/A";
        document.getElementById("soil_humidity").textContent = data.umidade_solo || "N/A";
    } catch (error) {
        console.error("Erro ao buscar dados do sensor:", error);
    }
}

function updateDesiredValues() {
    fetch('/getValuesDesirable')
        .then(response => response.json())
        .then(data => {
            document.getElementById('tempDesirableCurrent').textContent = data.temperatura || "N/A";
            document.getElementById('airHumidityDesirableCurrent').textContent = data.umidade || "N/A";
            document.getElementById('co2Current').textContent = data.co2 || "N/A";
            document.getElementById('soilMoistureDesirableCurrent').textContent = data.umidadeSolo || "N/A";
        })
        .catch(error => console.error('Erro ao carregar valores iniciais:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    getatualizarStatusIrrigacao();
    updateDesiredValues();
    fetchSensorData();
});

document.getElementById('refreshSensorData').addEventListener('click', async function(event) {
    event.preventDefault();
    fetchSensorData();
});

function validarNumero(event) {
    let valor = event.target.value;
    // Substitui qualquer coisa que não seja número
    event.target.value = valor.replace(/[^0-9]/g, '');
}

document.getElementById('sendFormData').addEventListener('click', function() {
    var temperatura = document.getElementById('tempDesirable').value;
    var umidade = document.getElementById('airHumidityDesirable').value;
    var co2 = document.getElementById('co2Desirable').value;
    var umidadeSolo = document.getElementById('soilMoistureDesirable').value;

    if (!temperatura || !umidade || !co2 || !umidadeSolo) {
        alert("Por favor, preencha todos os campos antes de enviar.");
        return; // Interrompe o envio se algum campo estiver vazio
    }

    $.ajax({
        url: '/sendDesiredData',
        method: 'POST',
        data: {
            temperatura: temperatura,
            umidade: umidade,
            co2: co2,
            umidadeSolo: umidadeSolo
        },
        success: function(response) {
            document.getElementById('tempDesirable').value = '';
            document.getElementById('airHumidityDesirable').value = '';
            document.getElementById('co2Desirable').value = '';
            document.getElementById('soilMoistureDesirable').value = '';

            updateDesiredValues();
        },
        error: function(xhr, status, error) {
            console.log("Erro ao enviar dados:", error);
        }
    });
});

function getatualizarStatusIrrigacao() {
    $.ajax({
        url: '/irrigationStatus',
        method: 'GET',
        success: function(data) {
            const status = data.status;
            const color = status === 'Ligado' ? 'green' : 'red';
            document.getElementById('statusIndicatorHome').style.backgroundColor = color;
            document.getElementById('statusIrrigacaoHome').style.color = color;
            document.getElementById('statusIrrigacaoHome').textContent = status;
        },
        error: function(error) {
            console.error('Erro ao buscar o status de irrigação:', error);
        }
    });
}