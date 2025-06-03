let originalData = null;
let charts = {};
let defaultDateRange = {
    start: new Date(new Date().setMonth(new Date().getMonth() - 3)),
    end: new Date()
};

// Cache de dados para otimização
const dataCache = new Map();

// Variável global para o timeout de redimensionamento
let resizeTimeout;

// Configurações comuns atualizadas para todos os gráficos
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 8,
                boxWidth: 27,
                font: {
                    size: 11
                },
                // Limita o tamanho do texto da legenda
                generateLabels: function(chart) {
                    const original = Chart.defaults.plugins.legend.labels.generateLabels(chart);
                    return original.map(label => {
                        label.text = label.text.length > 25 ? 
                            label.text.substring(0, 22) + '...' : 
                            label.text;
                        return label;
                    });
                }
            }
        },
        title: {
            display: true,
            font: {
                size: 12
            }
        },
        tooltip: {
            enabled: true,
            mode: 'index',
            intersect: false,
            callbacks: {
                label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                        label += ': ';
                    }
                    if (context.parsed.y !== null) {
                        label += context.parsed.y.toLocaleString();
                    }
                    return label;
                },
                title: function(tooltipItems) {
                    // Formata o título do tooltip para nomes longos
                    const title = tooltipItems[0].label;
                    if (title.length > 30) {
                        return title.match(/.{1,30}/g); // Quebra em linhas de 30 caracteres
                    }
                    return title;
                }
            },
            padding: 10,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleFont: {
                size: 12
            },
            bodyFont: {
                size: 11
            }
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                font: {
                    size: 10
                },
                callback: function(value) {
                    return value.toLocaleString();
                }
            },
            grid: {
                color: 'rgba(0, 0, 0, 0.05)'
            }
        },
        x: {
            ticks: {
                font: {
                    size: 10
                },
                maxRotation: 45,
                minRotation: 45
            },
            grid: {
                color: 'rgba(0, 0, 0, 0.05)'
            }
        }
    },
    layout: {
        padding: {
            top: 2,
            right: 2,
            bottom: 2,
            left: 2
        }
    },
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderColor: 'rgba(0, 0, 0, 0.1)',
    barThickness: 'flex',
    maxBarThickness: 36,
    barPercentage: 1,
    categoryPercentage: 0.9,
    hover: {
        mode: 'index',
        intersect: false
    },
    resizeDelay: 0,
    animation: {
        duration: 0 // Desativa animações para evitar problemas de redimensionamento
    }
};

// Cores atualizadas para os gráficos com transparência
const colors = {
    commits: 'rgba(54, 162, 235, 0.8)',
    arquivos: 'rgba(255, 99, 132, 0.8)',
    linhas_adicionadas: 'rgba(75, 192, 192, 0.8)',
    linhas_removidas: 'rgba(255, 159, 64, 0.8)',
    total_linhas: 'rgba(153, 102, 255, 0.8)'
};

// Configurações específicas por tipo de gráfico
const chartConfigs = {
    authorEnv: {
        type: 'bar',
        legendPosition: 'bottom',
        needsDateFilter: false
    },
    environment: {
        type: 'bar',
        legendPosition: 'bottom',
        needsDateFilter: false
    },
    daily: {
        type: 'line',
        legendPosition: 'top',
        needsDateFilter: true
    },
    monthly: {
        type: 'bar',
        legendPosition: 'top',
        needsDateFilter: true
    }
};

function formatAuthorName(name, maxLength = 20) {
    if (!name) return '';
    if (name.length <= maxLength) return name;
    
    // Se o nome contiver espaços, tenta abreviar os nomes do meio
    if (name.includes(' ')) {
        const parts = name.split(' ');
        const firstName = parts[0];
        const lastName = parts[parts.length - 1];
        const middleInitials = parts.slice(1, -1)
            .map(part => part[0] + '.')
            .join(' ');
        
        const formatted = `${firstName} ${middleInitials} ${lastName}`.trim();
        return formatted.length > maxLength ? 
            formatted.substring(0, maxLength - 3) + '...' : 
            formatted;
    }
    
    // Se for uma string única, trunca com ellipsis
    return name.substring(0, maxLength - 3) + '...';
}

function filterDataByAuthor(data, author, chartType) {
    if (!data || !author) return data;

    const filtered = JSON.parse(JSON.stringify(data));
    console.log('Filtrando por autor:', author, 'Tipo:', chartType);

    try {
        switch(chartType) {
            case 'authorEnv':
                filtered.resumo_autor_ambiente = data.resumo_autor_ambiente.filter(item => 
                    item.nome_autor === author
                );
                break;

            case 'environment':
                filtered.resumo_ambiente = data.resumo_ambiente.map(env => {
                    const authorData = data.resumo_autor_ambiente.find(item => 
                        item.nome_autor === author && item.ambiente === env.ambiente
                    );
                    
                    return {
                        ambiente: env.ambiente,
                        commits: authorData ? authorData.commits : 0,
                        arquivos: authorData ? authorData.arquivos : 0,
                        linhas_adicionadas: authorData ? authorData.linhas_adicionadas : 0,
                        linhas_removidas: authorData ? authorData.linhas_removidas : 0,
                        total_linhas: authorData ? authorData.total_linhas : 0
                    };
                });
                break;

            case 'daily':
            case 'monthly':
                // Filtra primeiro por autor
                const authorData = data.resumo_autor_ambiente.filter(item => 
                    item.nome_autor === author
                );

                if (chartType === 'daily') {
                    // Agrupa dados diários
                    const dailyData = new Map();
                    
                    authorData.forEach(item => {
                        const date = item.data;
                        if (!dailyData.has(date)) {
                            dailyData.set(date, {
                                data: date,
                                commits: 0,
                                arquivos: 0,
                                linhas_adicionadas: 0,
                                linhas_removidas: 0,
                                total_linhas: 0
                            });
                        }
                        
                        const current = dailyData.get(date);
                        current.commits += item.commits;
                        current.arquivos += item.arquivos;
                        current.linhas_adicionadas += item.linhas_adicionadas;
                        current.linhas_removidas += item.linhas_removidas;
                        current.total_linhas += item.total_linhas;
                    });

                    filtered.totais_diarios = Array.from(dailyData.values())
                        .filter(day => 
                            day.commits > 0 || 
                            day.arquivos > 0 || 
                            day.linhas_adicionadas > 0 || 
                            day.linhas_removidas > 0 || 
                            day.total_linhas > 0
                        )
                        .sort((a, b) => new Date(a.data) - new Date(b.data));
                } else {
                    // Agrupa dados mensais
                    const monthlyData = new Map();
                    
                    authorData.forEach(item => {
                        const date = new Date(item.data);
                        const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
                        
                        if (!monthlyData.has(monthKey)) {
                            monthlyData.set(monthKey, {
                                mes: monthKey,
                                commits: 0,
                                arquivos: 0,
                                linhas_adicionadas: 0,
                                linhas_removidas: 0,
                                total_linhas: 0
                            });
                        }
                        
                        const current = monthlyData.get(monthKey);
                        current.commits += item.commits;
                        current.arquivos += item.arquivos;
                        current.linhas_adicionadas += item.linhas_adicionadas;
                        current.linhas_removidas += item.linhas_removidas;
                        current.total_linhas += item.total_linhas;
                    });

                    filtered.totais_mensais = Array.from(monthlyData.values())
                        .filter(month => 
                            month.commits > 0 || 
                            month.arquivos > 0 || 
                            month.linhas_adicionadas > 0 || 
                            month.linhas_removidas > 0 || 
                            month.total_linhas > 0
                        )
                        .sort((a, b) => a.mes.localeCompare(b.mes));
                }
                break;
        }

        return filtered;
    } catch (error) {
        console.error('Erro ao filtrar dados por autor:', error);
        return data;
    }
}

function populateAuthorFilters(data) {
    const authors = [...new Set(data.resumo_autor_ambiente.map(item => item.nome_autor))];
    const filterConfigs = [
        { id: 'authorFilter', type: 'authorEnv' },
        { id: 'envAuthorFilter', type: 'environment' },
        { id: 'dailyAuthorFilter', type: 'daily' },
        { id: 'monthlyAuthorFilter', type: 'monthly' }
    ];
    
    filterConfigs.forEach(config => {
        const select = document.getElementById(config.id);
        if (!select) return;

        select.innerHTML = '<option value="">Todos os Autores</option>';
        
        authors.forEach(author => {
            const option = document.createElement('option');
            option.value = author;
            option.textContent = formatAuthorName(author);
            select.appendChild(option);
        });
        
        select.addEventListener('change', function() {
            const chartWrapper = this.closest('.chart-wrapper');
            const dateFilter = chartWrapper?.querySelector('.date-filter');
            let filteredData = filterDataByAuthor(originalData, this.value, config.type);
            
            // Se houver filtro de data e o gráfico precisar dele, aplica o filtro de data também
            if (dateFilter && chartConfigs[config.type].needsDateFilter) {
                const startDate = new Date(dateFilter.querySelector('input[type="date"]:first-of-type').value);
                const endDate = new Date(dateFilter.querySelector('input[type="date"]:last-of-type').value);
                filteredData = filterDataByDateRange(filteredData, startDate, endDate, config.type);
            }
            
            updateChart(config.type, filteredData);
        });
    });
}

function updateChart(chartType, data) {
    if (!data) {
        console.error('Dados não fornecidos para atualização do gráfico');
        return;
    }

    const chartId = `${chartType}Chart`;
    
    // Verifica se há dados válidos antes de atualizar
    let hasValidData = false;
    switch(chartType) {
        case 'authorEnv':
            hasValidData = data.resumo_autor_ambiente && data.resumo_autor_ambiente.length > 0;
            break;
        case 'environment':
            hasValidData = data.resumo_ambiente && data.resumo_ambiente.length > 0;
            break;
        case 'daily':
            hasValidData = data.totais_diarios && data.totais_diarios.length > 0;
            break;
        case 'monthly':
            hasValidData = data.totais_mensais && data.totais_mensais.length > 0;
            break;
    }

    if (!hasValidData) {
        console.log(`Sem dados válidos para o gráfico ${chartType}`);
        showNoDataMessage(chartId);
        return;
    }

    requestAnimationFrame(() => {
        try {
            switch(chartType) {
                case 'authorEnv':
                    createAuthorEnvChart(data);
                    break;
                case 'environment':
                    createEnvironmentChart(data);
                    break;
                case 'daily':
                    createDailyTotalsChart(data);
                    break;
                case 'monthly':
                    createMonthlyTotalsChart(data);
                    break;
            }
        } catch (error) {
            console.error(`Erro ao atualizar gráfico ${chartType}:`, error);
            showNoDataMessage(chartId);
        }
    });
}

// Função para criar o loader com tamanho reduzido
function createLoader(chartId) {
    const canvas = document.getElementById(chartId);
    const parent = canvas.parentElement;
    
    const loaderContainer = document.createElement('div');
    loaderContainer.className = 'chart-loader';
    loaderContainer.id = `${chartId}-loader`;
    loaderContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.2s ease;
        pointer-events: none;
    `;

    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.style.cssText = `
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    `;

    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    loaderContainer.appendChild(spinner);
    parent.style.position = 'relative';
    parent.appendChild(loaderContainer);
}

function toggleLoader(chartId, show) {
    const loader = document.getElementById(`${chartId}-loader`);
    if (loader) {
        loader.style.opacity = show ? '1' : '0';
        loader.style.pointerEvents = show ? 'auto' : 'none';
    }
}

// Função para verificar se há dados no período
function hasDataInPeriod(data, startDate, endDate, chartType) {
    if (!data) return false;

    switch(chartType) {
        case 'daily':
            return data.totais_diarios.some(item => {
                const itemDate = new Date(item.data);
                return itemDate >= startDate && itemDate <= endDate;
            });
        case 'monthly':
            return data.totais_mensais.some(item => {
                const [year, month] = item.mes.split('-').map(Number);
                const itemDate = new Date(year, month - 1);
                return itemDate >= startDate && itemDate <= endDate;
            });
        case 'authorEnv':
            return data.resumo_autor_ambiente && data.resumo_autor_ambiente.length > 0;
        case 'environment':
            return data.resumo_ambiente && data.resumo_ambiente.length > 0;
        default:
            return false;
    }
}

// Função para mostrar mensagem de sem dados
function showNoDataMessage(chartId) {
    const canvas = document.getElementById(chartId);
    const ctx = canvas.getContext('2d');
    
    // Limpar o canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Configurar estilo do texto
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = '14px Arial';
    ctx.fillStyle = '#666';
    
    // Desenhar mensagem
    ctx.fillText('Nenhum dado encontrado para o período selecionado', canvas.width / 2, canvas.height / 2);
    
    // Adicionar sugestão
    ctx.font = '12px Arial';
    ctx.fillText('Tente ajustar o período de busca ou clique em Reset', canvas.width / 2, (canvas.height / 2) + 25);
}

// Função para criar o filtro de data com tamanho reduzido
function createDateFilter(chartId, chartType) {
    if (!chartConfigs[chartType].needsDateFilter) return;
    
    const chartWrapper = document.querySelector(`#${chartId}`).closest('.chart-wrapper');
    const dateFilter = chartWrapper.querySelector('.date-filter');
    if (!dateFilter) return;
    
    const startDate = dateFilter.querySelector('input[type="date"]:first-of-type');
    const endDate = dateFilter.querySelector('input[type="date"]:last-of-type');
    const applyButton = dateFilter.querySelector('.btn-primary');
    const resetButton = dateFilter.querySelector('.btn-outline-secondary');

    // Configurar datas iniciais
    startDate.value = defaultDateRange.start.toISOString().split('T')[0];
    endDate.value = defaultDateRange.end.toISOString().split('T')[0];

    // Handler para o botão Aplicar
    applyButton.addEventListener('click', () => {
        const start = new Date(startDate.value);
        const end = new Date(endDate.value);
        
        if (start > end) {
            alert('Data inicial deve ser anterior à data final');
            return;
        }

        // Obtém o autor selecionado, se houver
        const authorSelect = chartWrapper.querySelector(`[id$="AuthorFilter"]`);
        const selectedAuthor = authorSelect ? authorSelect.value : '';
        
        // Aplica os filtros na ordem correta
        let filteredData = originalData;
        if (selectedAuthor) {
            filteredData = filterDataByAuthor(filteredData, selectedAuthor, chartType);
        }
        filteredData = filterDataByDateRange(filteredData, start, end, chartType);

        if (!hasDataInPeriod(filteredData, start, end, chartType)) {
            showNoDataMessage(chartId);
            return;
        }

        updateChart(chartType, filteredData);
    });

    // Handler para o botão Reset
    resetButton.addEventListener('click', () => {
        startDate.value = defaultDateRange.start.toISOString().split('T')[0];
        endDate.value = defaultDateRange.end.toISOString().split('T')[0];
        
        // Obtém o autor selecionado, se houver
        const authorSelect = chartWrapper.querySelector(`[id$="AuthorFilter"]`);
        const selectedAuthor = authorSelect ? authorSelect.value : '';
        
        // Aplica os filtros na ordem correta
        let filteredData = originalData;
        if (selectedAuthor) {
            filteredData = filterDataByAuthor(filteredData, selectedAuthor, chartType);
        }
        filteredData = filterDataByDateRange(
            filteredData,
            defaultDateRange.start,
            defaultDateRange.end,
            chartType
        );
        
        updateChart(chartType, filteredData);
    });
}

function filterDataByDateRange(data, startDate, endDate, chartType) {
    if (!data) return null;

    const filtered = JSON.parse(JSON.stringify(data));
    startDate.setHours(0, 0, 0, 0);
    endDate.setHours(23, 59, 59, 999);

    // Filtrar dados por data para todos os tipos de gráficos
    if (data.resumo_autor_ambiente) {
        filtered.resumo_autor_ambiente = data.resumo_autor_ambiente.filter(item => {
            const itemDate = new Date(item.data);
            return itemDate >= startDate && itemDate <= endDate;
        });
    }

    if (data.resumo_ambiente) {
        filtered.resumo_ambiente = data.resumo_ambiente.filter(item => {
            const itemDate = new Date(item.data);
            return itemDate >= startDate && itemDate <= endDate;
        });
    }

    if (data.totais_diarios) {
        filtered.totais_diarios = data.totais_diarios.filter(item => {
            const itemDate = new Date(item.data);
            return itemDate >= startDate && itemDate <= endDate;
        });
    }

    if (data.totais_mensais) {
        filtered.totais_mensais = data.totais_mensais.filter(item => {
            const [year, month] = item.mes.split('-').map(Number);
            const itemDate = new Date(year, month - 1);
            return itemDate >= startDate && itemDate <= endDate;
        });
    }

    return filtered;
}

// Função para ajustar altura do gráfico baseado na quantidade de dados
function adjustChartHeight(chartId) {
    const canvas = document.getElementById(chartId);
    if (!canvas) return;

    const chartContainer = canvas.closest('.chart-container');
    if (!chartContainer) return;

    // Definir altura fixa baseada no tamanho da tela
    const height = window.innerWidth <= 768 ? 120 : 140;
    chartContainer.style.height = `${height}px`;
    canvas.style.height = `${height}px`;

    // Forçar atualização do gráfico se existir
    if (charts[chartId]) {
        charts[chartId].resize();
    }
}

// Função otimizada para criar/atualizar gráfico com performance melhorada
function createOrUpdateChart(chartId, type, data, options) {
    const canvas = document.getElementById(chartId);
    const ctx = canvas.getContext('2d');
    
    if (charts[chartId]) {
        charts[chartId].destroy();
        charts[chartId] = null;
    }

    const chartContainer = canvas.closest('.chart-container');
    if (chartContainer) {
        const height = window.innerWidth <= 768 ? 320 : 380;
        chartContainer.style.height = `${height}px`;
        canvas.style.height = `${height}px`;
    }

    // Configurações específicas do tipo de gráfico
    const chartConfig = chartConfigs[type] || {};
    const finalOptions = {
        ...commonOptions,
        ...options,
        plugins: {
            ...commonOptions.plugins,
            ...options.plugins,
            legend: {
                ...commonOptions.plugins.legend,
                position: chartConfig.legendPosition || 'top'
            }
        }
    };

    charts[chartId] = new Chart(ctx, {
        type: chartConfig.type || type,
        data: data,
        options: finalOptions
    });

    // Aplicar estado inicial dos filtros de métricas
    updateMetricsVisibility(chartId);
}

function createAuthorEnvChart(data) {
    if (!data.resumo_autor_ambiente || data.resumo_autor_ambiente.length === 0) {
        console.log('Sem dados de autor/ambiente para exibir');
        showNoDataMessage('authorEnvChart');
        return;
    }

    const chartId = 'authorEnvChart';
    const metrics = ['commits', 'arquivos', 'linhas_adicionadas', 'linhas_removidas', 'total_linhas'];
    
    // Agrupa dados por autor
    const authorData = {};
    data.resumo_autor_ambiente.forEach(item => {
        if (!authorData[item.nome_autor]) {
            authorData[item.nome_autor] = {
                commits: 0,
                arquivos: 0,
                linhas_adicionadas: 0,
                linhas_removidas: 0,
                total_linhas: 0
            };
        }
        authorData[item.nome_autor].commits += item.commits;
        authorData[item.nome_autor].arquivos += item.arquivos;
        authorData[item.nome_autor].linhas_adicionadas += item.linhas_adicionadas;
        authorData[item.nome_autor].linhas_removidas += item.linhas_removidas;
        authorData[item.nome_autor].total_linhas += item.total_linhas;
    });

    const authors = Object.keys(authorData);
    console.log('Autores encontrados:', authors);
    console.log('Dados agrupados:', authorData);

    const chartData = {
        labels: authors,
        datasets: metrics.map(metric => ({
            label: metric.replace('_', ' ').toUpperCase(),
            data: authors.map(author => authorData[author][metric]),
            backgroundColor: colors[metric],
            borderColor: colors[metric].replace('0.8', '1'),
            borderWidth: 1
        }))
    };

    const options = {
        plugins: {
            title: {
                text: 'Métricas por Autor'
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return value.toLocaleString();
                    }
                }
            }
        }
    };

    createOrUpdateChart(chartId, 'bar', chartData, options);
}

function createEnvironmentChart(data) {
    if (!data.resumo_ambiente || data.resumo_ambiente.length === 0) return;

    const chartId = 'environmentChart';
    const metrics = ['commits', 'arquivos', 'linhas_adicionadas', 'linhas_removidas', 'total_linhas'];
    const chartData = {
        labels: metrics.map(m => m.replace('_', ' ').toUpperCase()),
        datasets: data.resumo_ambiente.map(env => ({
            label: env.ambiente,
            data: metrics.map(m => env[m]),
            backgroundColor: Object.values(colors)[data.resumo_ambiente.indexOf(env)],
            borderColor: Object.values(colors)[data.resumo_ambiente.indexOf(env)].replace('0.8', '1'),
            borderWidth: 1
        }))
    };

    adjustChartHeight(chartId);

    const options = {
        plugins: {
            title: {
                text: 'Métricas por Ambiente'
            }
        }
    };

    createOrUpdateChart(chartId, 'environment', chartData, options);
}

function createDailyTotalsChart(data) {
    if (!data.totais_diarios || data.totais_diarios.length === 0) {
        console.log('Sem dados diários para exibir');
        showNoDataMessage('dailyTotalsChart');
        return;
    }

    const chartId = 'dailyTotalsChart';
    const metrics = ['commits', 'arquivos', 'linhas_adicionadas', 'linhas_removidas', 'total_linhas'];
    
    // Ordenar dados por data
    const sortedData = data.totais_diarios
        .filter(item => item.data) // Garante que só dados com data válida sejam incluídos
        .sort((a, b) => new Date(a.data) - new Date(b.data));
    
    if (sortedData.length === 0) {
        console.log('Sem dados diários válidos para exibir');
        showNoDataMessage('dailyTotalsChart');
        return;
    }

    const chartData = {
        labels: sortedData.map(item => {
            const date = new Date(item.data);
            return date.toLocaleDateString('pt-BR');
        }),
        datasets: metrics.map(metric => ({
            label: metric.replace('_', ' ').toUpperCase(),
            data: sortedData.map(item => item[metric] || 0),
            borderColor: colors[metric].replace('0.8', '1'),
            backgroundColor: colors[metric].replace('0.8', '0.2'),
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 3,
            pointHoverRadius: 5
        }))
    };

    const options = {
        plugins: {
            title: {
                text: 'Totais Diários'
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    maxRotation: 45,
                    minRotation: 45,
                    callback: function(value, index) {
                        return index % Math.ceil(sortedData.length / 15) === 0 ? 
                            this.getLabelForValue(value) : '';
                    }
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return value.toLocaleString();
                    }
                }
            }
        }
    };

    createOrUpdateChart(chartId, 'line', chartData, options);
}

function createMonthlyTotalsChart(data) {
    if (!data.totais_mensais || data.totais_mensais.length === 0) {
        console.log('Sem dados mensais para exibir');
        showNoDataMessage('monthlyTotalsChart');
        return;
    }

    const chartId = 'monthlyTotalsChart';
    const metrics = ['commits', 'arquivos', 'linhas_adicionadas', 'linhas_removidas', 'total_linhas'];
    
    // Ordenar dados por mês
    const sortedData = data.totais_mensais.sort((a, b) => a.mes.localeCompare(b.mes));
    
    if (sortedData.length === 0) {
        console.log('Sem dados mensais válidos para exibir');
        showNoDataMessage('monthlyTotalsChart');
        return;
    }

    const chartData = {
        labels: sortedData.map(item => {
            const [year, month] = item.mes.split('-');
            return new Date(year, month - 1).toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
        }),
        datasets: metrics.map(metric => ({
            label: metric.replace('_', ' ').toUpperCase(),
            data: sortedData.map(item => item[metric] || 0),
            backgroundColor: colors[metric],
            borderColor: colors[metric].replace('0.8', '1'),
            borderWidth: 1
        }))
    };

    const options = {
        plugins: {
            title: {
                text: 'Totais Mensais'
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return value.toLocaleString();
                    }
                }
            }
        }
    };

    createOrUpdateChart(chartId, 'bar', chartData, options);
}

function createPlots(data) {
    if (!data) {
        console.error('Dados não recebidos');
        return;
    }

    try {
        // Armazena os dados originais na primeira vez
        if (!originalData) {
            originalData = JSON.parse(JSON.stringify(data));
            populateAuthorFilters(data);
        }

        // Define o período padrão de 3 meses
        const threeMonthsAgo = new Date();
        threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
        const today = new Date();

        // Filtra os dados para o período padrão
        const filteredData = {
            ...data,
            totais_diarios: data.totais_diarios?.filter(item => {
                const itemDate = new Date(item.data);
                return itemDate >= threeMonthsAgo && itemDate <= today;
            }) || [],
            totais_mensais: data.totais_mensais?.filter(item => {
                const [year, month] = item.mes.split('-').map(Number);
                const itemDate = new Date(year, month - 1);
                return itemDate >= threeMonthsAgo && itemDate <= today;
            }) || []
        };

        // Configura as datas nos filtros
        document.querySelectorAll('.date-filter').forEach(filter => {
            const startInput = filter.querySelector('input[type="date"]:first-of-type');
            const endInput = filter.querySelector('input[type="date"]:last-of-type');
            if (startInput && endInput) {
                startInput.value = threeMonthsAgo.toISOString().split('T')[0];
                endInput.value = today.toISOString().split('T')[0];
            }
        });

        // Cria tabela de autores
        if (data.resumo_autor_ambiente && data.resumo_autor_ambiente.length > 0) {
            const uniqueAuthors = [...new Set(data.resumo_autor_ambiente.map(item => item.nome_autor))];
            const authorsTableHtml = `
                <div class="table-responsive">
                    <table class="table table-sm table-striped table-bordered mb-0">
                        <thead>
                            <tr>
                                <th>Autor</th>
                                <th>Email</th>
                                <th class="text-center">Commits</th>
                                <th class="text-center">Arquivos</th>
                                <th class="text-center">Linhas Totais</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${uniqueAuthors.map(author => {
                                const authorData = data.resumo_autor_ambiente
                                    .filter(item => item.nome_autor === author)
                                    .reduce((acc, curr) => ({
                                        email_autor: curr.email_autor,
                                        commits: (acc.commits || 0) + curr.commits,
                                        arquivos: (acc.arquivos || 0) + curr.arquivos,
                                        total_linhas: (acc.total_linhas || 0) + curr.total_linhas
                                    }), {});
                                
                                return `
                                    <tr>
                                        <td>${author}</td>
                                        <td>${authorData.email_autor}</td>
                                        <td class="text-center">${authorData.commits.toLocaleString()}</td>
                                        <td class="text-center">${authorData.arquivos.toLocaleString()}</td>
                                        <td class="text-center">${authorData.total_linhas.toLocaleString()}</td>
                                    </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
            `;
            document.getElementById('authorsTable').innerHTML = authorsTableHtml;
        }

        // Criar gráficos em sequência otimizada usando requestAnimationFrame
        requestAnimationFrame(() => {
            if (data.resumo_autor_ambiente && data.resumo_autor_ambiente.length > 0) {
                createAuthorEnvChart(data);
            }
            requestAnimationFrame(() => {
                if (data.resumo_ambiente && data.resumo_ambiente.length > 0) {
                    createEnvironmentChart(data);
                }
                requestAnimationFrame(() => {
                    if (filteredData.totais_diarios && filteredData.totais_diarios.length > 0) {
                        createDailyTotalsChart(filteredData);
                    }
                    requestAnimationFrame(() => {
                        if (filteredData.totais_mensais && filteredData.totais_mensais.length > 0) {
                            createMonthlyTotalsChart(filteredData);
                        }
                    });
                });
            });
        });

    } catch (error) {
        console.error('Erro ao criar gráficos:', error);
    }
}

// Atualizar o evento de resize
window.addEventListener('resize', function() {
    if (resizeTimeout) clearTimeout(resizeTimeout);
    
    resizeTimeout = setTimeout(() => {
        Object.keys(charts).forEach(chartId => {
            if (charts[chartId]) {
                const container = document.getElementById(chartId).closest('.chart-container');
                if (container) {
                    const height = window.innerWidth <= 768 ? 320 : 380;
                    container.style.height = `${height}px`;
                    document.getElementById(chartId).style.height = `${height}px`;
                    charts[chartId].resize();
                }
            }
        });
    }, 100);
});

// Função para atualizar visibilidade das métricas
function updateMetricsVisibility(chartId) {
    const chart = charts[chartId];
    if (!chart) return;

    const chartCanvas = document.getElementById(chartId);
    if (!chartCanvas) return;

    const chartWrapper = chartCanvas.closest('.chart-wrapper');
    if (!chartWrapper) return;

    const metricsFilter = chartWrapper.querySelector('.metrics-filter');
    if (!metricsFilter) return;

    const activeMetrics = Array.from(metricsFilter.querySelectorAll('.metric-item.active')).map(item => 
        item.dataset.metric
    );

    chart.data.datasets.forEach(dataset => {
        const metric = dataset.label.toLowerCase().replace(/ /g, '_');
        dataset.hidden = !activeMetrics.includes(metric);
    });

    chart.update('none');
}

// Atualizar os estilos dos filtros de métricas quando ativos/inativos
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .metric-item {
            font-size: 0.8rem;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s ease;
            color: white;
        }
        
        .metric-item:not(.active) {
            background-color: #f8f9fa !important;
            color: #666;
            border-color: #dee2e6;
        }
        
        .metric-item:hover {
            opacity: 0.8;
        }
    `;
    document.head.appendChild(style);

    document.querySelectorAll('.metrics-filter .metric-item').forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('active');
            const chartId = this.closest('.chart-wrapper').querySelector('canvas').id;
            updateMetricsVisibility(chartId);
        });
    });
}); 