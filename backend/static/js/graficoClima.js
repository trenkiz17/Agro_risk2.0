// AgroRisk: gráfico de PREVISÃO climática da propriedade.
// A fonte de dados é a resposta existente de GET /api/clima/previsao.
// Nenhum dado artificial é gerado e previsões não são apresentadas como histórico.

window.AgroRiskGraficoClima = (() => {
    let grafico = null;

    function situacao(mensagem) {
        const aviso = document.getElementById("situacaoGraficoClima");
        if (aviso) aviso.textContent = mensagem;
    }

    function limpar(mensagem = "Previsão climática indisponível.") {
        if (grafico) {
            grafico.destroy();
            grafico = null;
        }
        const area = document.getElementById("areaGraficoClima");
        if (area) area.hidden = true;
        situacao(mensagem);
    }

    function valorNumerico(valor) {
        if (valor === undefined || valor === null || valor === "") return null;
        const numero = Number(valor);
        return Number.isFinite(numero) ? numero : null;
    }

    function rotuloData(data) {
        if (typeof data !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(data)) return "Data indisponível";
        const [ano, mes, dia] = data.split("-");
        return `${dia}/${mes}`;
    }

    function renderizar(dias) {
        const canvas = document.getElementById("graficoPrevisaoClimatica");
        const area = document.getElementById("areaGraficoClima");
        if (!canvas || !area) return;

        const registros = Array.isArray(dias)
            ? dias.filter(d => d && typeof d.data === "string" &&
                (valorNumerico(d.temperatura_maxima) !== null ||
                 valorNumerico(d.chuva_prevista_mm) !== null))
            : [];

        if (!registros.length) {
            limpar("Ainda não há previsão suficiente para construir o gráfico.");
            return;
        }
        if (typeof Chart === "undefined") {
            limpar("O componente gráfico não carregou. Verifique a conexão com a internet.");
            return;
        }

        if (grafico) grafico.destroy();
        area.hidden = false;
        const nomesDias = registros.map(d => rotuloData(d.data));
        const temperaturas = registros.map(d => valorNumerico(d.temperatura_maxima));
        const chuvas = registros.map(d => valorNumerico(d.chuva_prevista_mm));

        grafico = new Chart(canvas, {
            data: {
                labels: nomesDias,
                datasets: [
                    {
                        type: "line",
                        label: "Temperatura máxima (°C)",
                        data: temperaturas,
                        yAxisID: "temperatura",
                        borderColor: "#15803d",
                        backgroundColor: "#15803d",
                        borderWidth: 3,
                        pointRadius: 5,
                        tension: 0.25,
                        spanGaps: false
                    },
                    {
                        type: "bar",
                        label: "Chuva prevista (mm)",
                        data: chuvas,
                        yAxisID: "chuva",
                        backgroundColor: "rgba(37, 99, 235, 0.48)",
                        borderColor: "#2563eb",
                        borderWidth: 1,
                        borderRadius: 5,
                        maxBarThickness: 60
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: "index", intersect: false },
                plugins: {
                    legend: { position: "bottom" },
                    tooltip: { mode: "index", intersect: false }
                },
                scales: {
                    temperatura: {
                        type: "linear", position: "left",
                        title: { display: true, text: "Temperatura (°C)" }
                    },
                    chuva: {
                        type: "linear", position: "right", beginAtZero: true,
                        title: { display: true, text: "Chuva prevista (mm)" },
                        grid: { drawOnChartArea: false }
                    }
                }
            }
        });

        situacao("Fonte: OpenWeather • Previsão de curto prazo, sujeita a alterações. Não representa histórico de medições.");
    }

    return { renderizar, limpar };
})();
