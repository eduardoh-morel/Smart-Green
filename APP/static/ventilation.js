document.getElementById('btnLigarVentilacao').addEventListener('click', function() {
    const status = 'Ligado';
    postAtualizarStatusVentilacao(status);
});

document.getElementById('btnDesligarVentilacao').addEventListener('click', function() {
    const status = 'Desligado';
    postAtualizarStatusVentilacao(status);
});

function getatualizarStatusVentilacao() {
    $.ajax({
        url: '/ventilationStatus',
        method: 'GET',
        success: function(data) {
            const status = data.status;  // Status vindo do backend
            const color = status === 'Ligado' ? 'green' : 'red';  // Determina a cor baseada no status
            document.getElementById('statusIndicatorVentilation').style.backgroundColor = color;
            document.getElementById('statusVentilation').style.color = color;
            document.getElementById('statusVentilation').textContent = status;
        },
        error: function(error) {
            console.error('Erro ao buscar o status da ventilação:', error);
        }
    });
}

function postAtualizarStatusVentilacao(status) {
    $.ajax({
        url: '/ventilationStatus',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ status: status }),
        success: function(response) {
            const color = status === 'Ligado' ? 'green' : 'red';
            document.getElementById('statusIndicatorVentilation').style.backgroundColor = color;
            document.getElementById('statusVentilation').style.color = color;
            document.getElementById('statusVentilation').textContent = status;
        },
        error: function(xhr, status, error) {
            console.log("Erro ao atualizar status:", error);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    getatualizarStatusVentilacao();
    statusVentilacaoPorNecessidade();
    fetchSensorData();
    updateDesiredValues();
});

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


function statusVentilacaoPorNecessidade() {
    $.ajax({
        url: '/ventilationByNeed',
        method: 'GET',
        success: function(data) {
            const status = data.status;  // Status vindo do backend
            const color = status === 'Ligado' ? 'green' : 'red';  // Determina a cor baseada no status
            document.getElementById('statusIndicatorByNeedVentilation').style.backgroundColor = color;
            document.getElementById('statusVentilationByNeed').style.color = color;
            document.getElementById('statusVentilationByNeed').textContent = status;
            postAtualizarStatusVentilacao(status);

        },
        error: function(error) {
            console.error('Erro ao buscar o status da ventilação:', error);
        }
    });
}

document.getElementById("refreshStatusVentilationNeedBy").addEventListener("click", function() {
    statusVentilacaoPorNecessidade();
});