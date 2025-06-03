# Interface CLI do Git Metrics

## Visão Geral

A interface de linha de comando (CLI) do Git Metrics é uma ferramenta poderosa para análise automatizada de métricas de repositórios Git. Projetada para ser eficiente e fácil de usar, permite a geração rápida de relatórios e integração com scripts e pipelines.

## Comandos

### Comando Básico
```bash
git-metrics --path /caminho/do/repositorio
```

### Análise com Filtros
```bash
git-metrics --path /caminho/do/repositorio --author email@exemplo.com --since 2024-01-01 --until 2024-03-31
```

### Formatos de Saída
```bash
# Gerar relatório Excel (padrão)
git-metrics --path /repo --format excel

# Exportar como JSON
git-metrics --path /repo --format json

# Exportar como CSV
git-metrics --path /repo --format csv
```

## Parâmetros

### Parâmetros Obrigatórios

| Parâmetro | Descrição |
|-----------|-----------|
| --path, -p | Caminho do repositório Git para análise |

### Parâmetros de Filtro

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| --author, -a | Email do autor (múltiplos permitidos) | --author dev1@email.com |
| --since | Data inicial para análise | --since 2024-01-01 |
| --until | Data final para análise | --until 2024-12-31 |
| --branch | Branch específica para análise | --branch main |
| --env | Ambiente específico (PRD/HML) | --env PRD |

### Parâmetros de Saída

| Parâmetro | Descrição | Valores |
|-----------|-----------|---------|
| --format | Formato do relatório | excel, json, csv |
| --output | Diretório de saída | --output ./reports |
| --template | Template personalizado | --template custom.xlsx |

### Parâmetros Avançados

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| --threads | Número de threads para processamento | 4 |
| --cache | Usar cache de dados | true |
| --verbose | Nível de detalhamento do log | info |

## Exemplos de Uso

### 1. Análise Básica
```bash
git-metrics --path /repo
```

### 2. Filtro por Autor e Período
```bash
git-metrics --path /repo \
           --author dev1@email.com \
           --author dev2@email.com \
           --since 2024-01-01 \
           --until 2024-03-31
```

### 3. Análise de Branch Específica
```bash
git-metrics --path /repo \
           --branch feature/nova-funcionalidade \
           --format json
```

### 4. Relatório Personalizado
```bash
git-metrics --path /repo \
           --template custom_template.xlsx \
           --output ./reports/custom
```

### 5. Modo Verbose com Cache Desabilitado
```bash
git-metrics --path /repo \
           --verbose debug \
           --no-cache
```

## Saída do Relatório

### Excel (Padrão)

1. **Aba Resumo Geral**
   - Resumo por Autor e Ambiente
   - Resumo por Ambiente
   - Totais Diários
   - Totais Mensais

2. **Aba Estatísticas por Branch**
   - Métricas por branch
   - Comparativos

3. **Aba Estatísticas Diárias**
   - Análise dia a dia
   - Gráficos de tendência

4. **Aba Estatísticas Mensais**
   - Consolidado mensal
   - Evolução temporal

### JSON

```json
{
  "summary": {
    "total_commits": 1234,
    "total_files": 567,
    "total_lines": 89012
  },
  "authors": [...],
  "daily_stats": [...],
  "monthly_stats": [...]
}
```

### CSV
```csv
data,autor,commits,arquivos,linhas_adicionadas,linhas_removidas
2024-01-01,dev@email.com,5,10,100,50
...
```

## Integração

### 1. Scripts Shell
```bash
#!/bin/bash
REPOS=(/repo1 /repo2 /repo3)
for repo in "${REPOS[@]}"; do
    git-metrics --path "$repo" --output "./reports/$(basename $repo)"
done
```

### 2. Pipeline CI/CD
```yaml
metrics:
  script:
    - git-metrics --path . --format json --output metrics.json
  artifacts:
    reports:
      metrics: metrics.json
```

### 3. Automação
```python
import subprocess

def generate_metrics(repo_path):
    subprocess.run(['git-metrics', '--path', repo_path, '--format', 'json'])
```

## Configuração

### 1. Arquivo de Configuração
```yaml
# .git-metrics.yml
default_format: excel
output_dir: ./reports
cache_enabled: true
threads: 4
template: default.xlsx
```

### 2. Variáveis de Ambiente
```bash
export GIT_METRICS_OUTPUT_DIR=./reports
export GIT_METRICS_FORMAT=json
export GIT_METRICS_THREADS=8
```

## Troubleshooting

### Problemas Comuns

1. **Erro de Permissão**
   ```bash
   sudo chown -R user:group /repo
   git-metrics --path /repo
   ```

2. **Cache Corrompido**
   ```bash
   git-metrics --path /repo --clear-cache
   ```

3. **Memória Insuficiente**
   ```bash
   git-metrics --path /repo --low-memory
   ```

### Logs e Debug

```bash
# Modo debug
git-metrics --path /repo --verbose debug

# Salvar logs
git-metrics --path /repo --log-file metrics.log
```

## Performance

### Otimizações

1. **Cache**
   - Habilitar cache para repositórios grandes
   - Usar `--no-cache` apenas quando necessário

2. **Threads**
   - Ajustar número de threads conforme CPU
   - Usar modo low-memory para sistemas limitados

3. **Filtros**
   - Usar filtros de data para limitar escopo
   - Filtrar por autor quando possível

## Segurança

### Boas Práticas

1. **Permissões**
   - Usar usuário com acesso mínimo necessário
   - Verificar permissões do diretório de saída

2. **Dados Sensíveis**
   - Não incluir tokens em comandos
   - Usar variáveis de ambiente para credenciais

3. **Validação**
   - Validar caminhos de entrada
   - Sanitizar parâmetros

## Suporte

### Canais

1. **Documentação**
   - Manual online
   - Exemplos práticos
   - FAQs

2. **Comunidade**
   - Issues no GitHub
   - Fórum de discussão
   - Canal Discord

3. **Comercial**
   - Suporte por email
   - Consultoria
   - Treinamento 