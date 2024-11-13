function postAtualizarStatusVentilacao(status) {
    $.ajax({
        url: '/irrigationStatus',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ status: status }),
        success: function(response) {
            console.log("Status da irrigação atualizado:", response);
            const color = status === 'Ligado' ? 'green' : 'red';
            document.getElementById('statusIndicator').style.backgroundColor = color;
            document.getElementById('statusIrrigacao').style.color = color;
            document.getElementById('statusIrrigacao').textContent = status;
        },
        error: function(xhr, status, error) {
            console.log("Erro ao atualizar status:", error);
        }
    });
}

document.getElementById('btnLigarVentilacao').addEventListener('click', function() {
    const status = 'Ligado';
    postAtualizarStatusVentilacao(status);
});

document.getElementById('btnDesligarVentilacao').addEventListener('click', function() {
    const status = 'Desligado';
    postAtualizarStatusVentilacao(status);
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
        url: '/IrrigationByNeed',
        method: 'GET',
        success: function(data) {
            const status = data.status;  // Status vindo do backend
            const color = status === 'Ligado' ? 'green' : 'red';  // Determina a cor baseada no status
            document.getElementById('statusIndicatorByNeed').style.backgroundColor = color;
            document.getElementById('statusIrrigacaoByNeed').style.color = color;
            document.getElementById('statusIrrigacaoByNeed').textContent = status;
            postAtualizarStatusIrrigacao(status);

        },
        error: function(error) {
            console.error('Erro ao buscar o status de irrigação:', error);
        }
    });
}

document.getElementById("refreshStatusVentilationNeedBy").addEventListener("click", function() {
    statusVentilacaoPorNecessidade();
});