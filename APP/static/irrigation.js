// Função para atualizar o nível de umidade no display
function atualizarUmidadeValor(valor) {
    document.getElementById('umidadeValor').textContent = valor;
}

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
});