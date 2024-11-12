// Funções para controle manual da irrigação
document.getElementById('btnLigarIrrigacao').addEventListener('click', function() {
    const status = 'Ligado';  // Status a ser enviado
    postAtualizarStatusIrrigacao(status);  // Chama a função para atualizar o status
});

document.getElementById('btnDesligarIrrigacao').addEventListener('click', function() {
    const status = 'Desligado';  // Status a ser enviado
    postAtualizarStatusIrrigacao(status);  // Chama a função para atualizar o status
});

function getatualizarStatusIrrigacao() {
    $.ajax({
        url: '/irrigationStatus',
        method: 'GET',
        success: function(data) {
            const status = data.status;  // Status vindo do backend
            const color = status === 'Ligado' ? 'green' : 'red';  // Determina a cor baseada no status
            document.getElementById('statusIndicator').style.backgroundColor = color;
            document.getElementById('statusIrrigacao').style.color = color;
            document.getElementById('statusIrrigacao').textContent = status;
        },
        error: function(error) {
            console.error('Erro ao buscar o status de irrigação:', error);
        }
    });
}

function postAtualizarStatusIrrigacao(status) {
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

document.addEventListener('DOMContentLoaded', function() {
    getatualizarStatusIrrigacao();
    atualizarListaAgendamentosIrrigacao();
    verificarExistenciaDeAgendamentos();
    fetchSensorData();
    updateDesiredValues();
    statusIrrigacaoPorNecessidade();
});

document.getElementById('btnAgendarIrrigacao').addEventListener('click', function() {
    const horario = document.getElementById('horarioIrrigacao').value;
    const duracao = document.getElementById('duracaoIrrigacao').value;
    
    if (!horario || !duracao) {
        alert('Por favor, preencha o horário e a duração.');
        return;
    }

    $.ajax({
        url: '/agendarIrrigacao',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ horario: horario, duracao: parseInt(duracao) }),
        success: function(response) {
            atualizarListaAgendamentosIrrigacao();
            verificarExistenciaDeAgendamentos();
            document.getElementById('horarioIrrigacao').value = '';
            document.getElementById('duracaoIrrigacao').value = '';
        },
        error: function(xhr, status, error) {
            console.error("Erro ao agendar irrigação:", error);
        }
    });
});

function atualizarListaAgendamentosIrrigacao() {
    $.ajax({
        url: '/listarAgendamentos',
        method: 'GET',
        success: function(data) {
            const lista = document.getElementById('listaAgendamentos');
            lista.innerHTML = '';

            data.agendamentos.forEach((agendamento, index) => {
                const item = document.createElement('li');
                item.className = 'list-group-item d-flex justify-content-between align-items-center';

                item.textContent = `Horário: ${agendamento.horario}, Duração: ${agendamento.duracao} minutos`;

                // Botão de lixeira
                const deleteButton = document.createElement('button');
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
                deleteButton.onclick = function() {
                    removerAgendamento(index);
                };

                item.appendChild(deleteButton);
                lista.appendChild(item);
            });
        },
        error: function(error) {
            console.error('Erro ao listar agendamentos:', error);
        }
    });
}

function removerAgendamento(index) {
    $.ajax({
        url: `/removerAgendamento/${index}`,
        method: 'DELETE',
        success: function(response) {
            atualizarListaAgendamentosIrrigacao();
        },
        error: function(error) {
            console.error('Erro ao remover agendamento:', error);
        }
    });
}

function atualizarStatusPeriodicamente() {
    setInterval(function() {
        $.ajax({
            url: '/irrigationStatus',
            method: 'GET',
            success: function(data) {
                const status = data.status;
                const color = status === 'Ligado' ? 'green' : 'red';
                
                document.getElementById('statusIndicator').style.backgroundColor = color;
                document.getElementById('statusIrrigacao').textContent = status;
                document.getElementById('statusIrrigacao').style.color = color;
            },
            error: function(error) {
                console.error('Erro ao atualizar status de irrigação:', error);
            }
        });
    }, 60000);
}

function verificarExistenciaDeAgendamentos() {
    $.ajax({
        url: '/hasSchedule',
        method: 'GET',
        success: function(response) {
            if (response.has_schedule) {
                atualizarStatusPeriodicamente();
            }
        },
        error: function(error) {
            console.error('Erro ao verificar agendamentos:', error);
        }
    });
}

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

function statusIrrigacaoPorNecessidade() {
    $.ajax({
        url: '/IrrigationByNeed',
        method: 'GET',
        success: function(data) {
            const status = data.status;  // Status vindo do backend
            const color = status === 'Ligado' ? 'green' : 'red';  // Determina a cor baseada no status
            document.getElementById('statusIndicatorByNeed').style.backgroundColor = color;
            document.getElementById('statusIrrigacaoByNeed').style.color = color;
            document.getElementById('statusIrrigacaoByNeed').textContent = status;
        },
        error: function(error) {
            console.error('Erro ao buscar o status de irrigação:', error);
        }
    });
}