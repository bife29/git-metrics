# Análise de Métricas Git com Power BI

## Estrutura dos Arquivos
- `git_metrics_*.json`: Arquivo principal com os dados das métricas
- `power_bi_config.json`: Arquivo de configuração do painel
- `medidas_dax.txt`: Modelo de medidas DAX para análises

## Como Utilizar
1. Abra o Power BI Desktop
2. Importe o arquivo JSON mais recente:
   - Clique em 'Obter Dados'
   - Selecione 'JSON'
   - Navegue até a pasta 'power_bi_data'
   - Escolha o arquivo mais recente
3. Copie e cole as medidas DAX do arquivo template
4. Monte as visualizações conforme instruções abaixo

## Estrutura do Painel

### 1. Página Inicial (Visão Geral)
- Cartões com métricas principais:
  * Total de Commits
  * Total de Linhas de Código
  * Número de Autores
  * Quantidade de Branches
- Gráfico de rosca: Distribuição PRD vs HML
- Linha do tempo de commits (gráfico de área)
- Principais contribuidores (gráfico de barras)

### 2. Análise Detalhada
- Métricas por branch (mapa de árvore)
- Evolução temporal (gráfico de linha)
- Mapa de calor de atividades
- Filtros personalizados:
  * Por período
  * Por autor
  * Por ambiente (PRD/HML)

### 3. Produtividade
- Métricas por desenvolvedor
- Tendências de commits
- Análise comparativa
- Indicadores de desempenho:
  * Média de commits por dia
  * Linhas de código por commit
  * Atividade por ambiente

## Atualização de Dados
1. Execute o script Python para gerar novos dados
2. No Power BI Desktop:
   - Clique em 'Atualizar' para dados mais recentes
   - Configure atualização automática se necessário

## Medidas DAX Disponíveis
- Contagem total de commits
- Commits por ambiente (PRD/HML)
- Médias e tendências
- Métricas de produtividade
- Análises temporais

## Filtros Globais Disponíveis
1. Período:
   - Diário
   - Semanal
   - Mensal
2. Ambiente:
   - Produção (PRD)
   - Homologação (HML)
3. Autor:
   - Individual
   - Múltiplos autores
4. Branch:
   - Principal
   - Específica

## Dicas de Utilização
1. Use os filtros globais para análises específicas
2. Explore diferentes visualizações dos dados
3. Exporte relatórios quando necessário
4. Configure alertas para métricas importantes
5. Salve visualizações personalizadas

## Manutenção e Suporte
1. Documentação:
   - Consulte este guia para referência
   - Verifique atualizações periódicas
2. Logs:
   - Monitore os logs de execução
   - Verifique erros e avisos
3. Suporte:
   - Entre em contato com a equipe de desenvolvimento
   - Reporte problemas encontrados

## Boas Práticas
1. Atualize os dados regularmente
2. Mantenha backups das configurações personalizadas
3. Documente alterações realizadas
4. Compartilhe insights relevantes
5. Utilize os filtros adequadamente

## Resolução de Problemas
1. Dados não atualizados:
   - Verifique a execução do script
   - Confira a conexão com o repositório
2. Visualizações incorretas:
   - Revise as medidas DAX
   - Verifique os filtros aplicados
3. Erros de carregamento:
   - Confirme o formato do arquivo JSON
   - Verifique permissões de acesso

## Recursos Adicionais
- Documentação do projeto
- Guias de análise
- Exemplos de uso
- Modelos de relatório

Para mais informações ou suporte:
- Consulte a documentação completa do projeto
- Entre em contato com a equipe de desenvolvimento
- Verifique atualizações e novidades