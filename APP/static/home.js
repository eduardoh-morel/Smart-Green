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
// Carregar os dados inicialmente
fetchSensorData();

document.getElementById('refreshSensorData').addEventListener('click', async function(event) {
    event.preventDefault();
    fetchSensorData();
});

function validarNumero(event) {
    let valor = event.target.value;
    // Substitui qualquer coisa que não seja número
    event.target.value = valor.replace(/[^0-9]/g, '');
}

document.getElementById('sensorForm').addEventListener('click', function() {
    var temperatura = document.getElementById('tempDesirable').value;
    var umidade = document.getElementById('airHumidityDesirable').value;
    var co2 = document.getElementById('co2Desirable').value;
    var umidadeSolo = document.getElementById('soilMoistureDesirable').value;

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
            console.log("Dados enviados com sucesso!");
            console.log(response);
        },
        error: function(xhr, status, error) {
            console.log("Erro ao enviar dados:", error);
        }
    });
});