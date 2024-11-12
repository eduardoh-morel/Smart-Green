// Exemplo de inicialização do gráfico de histórico (com dados fictícios)
const ctx = document.getElementById('graficoUmidadeSolo').getContext('2d');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1h', '2h', '3h', '4h', '5h', '6h'],
        datasets: [{
            label: 'Umidade do Solo (%)',
            data: [45, 50, 55, 60, 65, 70],
            backgroundColor: 'rgba(0, 123, 255, 0.2)',
            borderColor: 'rgba(0, 123, 255, 1)',
            borderWidth: 2,
            fill: true
        }]
    },
    options: {
        scales: {
            x: { title: { display: true, text: 'Tempo' } },
            y: { title: { display: true, text: 'Umidade (%)' } }
        }
    }
});