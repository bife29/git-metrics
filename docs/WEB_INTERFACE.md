# Interface Web do Git Metrics

## Visão Geral

A interface web do Git Metrics oferece uma experiência interativa e visual para análise de métricas de repositórios Git. Com gráficos dinâmicos e filtros em tempo real, permite uma análise detalhada e intuitiva das contribuições do projeto.

## Funcionalidades

### 1. Dashboard Principal

#### Métricas por Autor
- Gráfico de barras com métricas por autor
- Filtros por período e ambiente
- Comparação entre autores

#### Métricas por Ambiente
- Distribuição de commits entre ambientes
- Análise de impacto por ambiente
- Tendências de desenvolvimento

#### Análise Temporal
- Gráficos de linha para métricas diárias
- Visualização de tendências mensais
- Períodos de maior atividade

### 2. Filtros Interativos

#### Filtro por Autor
- Seleção única ou múltipla de autores
- Atualização em tempo real dos gráficos
- Reset para visão geral

#### Filtro por Período
- Seleção de intervalo de datas
- Períodos predefinidos (último mês, trimestre, ano)
- Customização de período

#### Filtro por Ambiente
- Seleção de ambiente (PRD/HML)
- Comparação entre ambientes
- Análise isolada por ambiente

### 3. Tabelas de Dados

#### Tabela de Autores
- Lista completa de autores
- Métricas individuais
- Ordenação por diferentes critérios

#### Detalhes de Commits
- Histórico de commits
- Detalhes de alterações
- Links para o repositório

### 4. Exportação de Dados

#### Formatos Disponíveis
- Excel (.xlsx)
- CSV
- JSON
- Imagens dos gráficos (.png, .jpg)

#### Opções de Exportação
- Dados completos
- Dados filtrados
- Gráficos individuais

## Uso

### 1. Iniciando o Servidor

```bash
# Iniciar o servidor na porta padrão (8000)
git-metrics-web

# Iniciar em uma porta específica
git-metrics-web --port 3000

# Modo de desenvolvimento
git-metrics-web --debug
```

### 2. Acessando a Interface

1. Abra seu navegador
2. Acesse `http://localhost:8000` (ou a porta configurada)
3. Selecione um repositório para análise
4. Use os filtros para personalizar a visualização

### 3. Navegação

#### Menu Principal
- Dashboard
- Análise por Autor
- Análise por Ambiente
- Configurações

#### Barra de Ferramentas
- Filtros
- Exportação
- Atualizar dados
- Ajuda

## Personalização

### 1. Temas
- Claro/Escuro
- Cores personalizadas
- Fontes e tamanhos

### 2. Layout
- Organização de gráficos
- Visibilidade de elementos
- Tamanho dos componentes

### 3. Preferências
- Métricas padrão
- Filtros salvos
- Configurações de exibição

## Requisitos Técnicos

### 1. Navegador
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### 2. Sistema
- Conexão com internet
- JavaScript habilitado
- Cookies permitidos

### 3. Performance
- Mínimo de 2GB RAM
- Processador dual-core
- Resolução mínima: 1024x768

## Segurança

### 1. Autenticação
- Login opcional
- Integração com Git
- Tokens de acesso

### 2. Dados
- HTTPS
- Sanitização de entrada
- Proteção XSS

### 3. Permissões
- Leitura de repositório
- Exportação de dados
- Configurações

## Troubleshooting

### Problemas Comuns

1. **Servidor não inicia**
   - Verificar porta em uso
   - Checar permissões
   - Validar dependências

2. **Gráficos não carregam**
   - Limpar cache do navegador
   - Verificar JavaScript
   - Checar console de erros

3. **Dados desatualizados**
   - Usar botão de atualização
   - Verificar conexão Git
   - Limpar cache local

### Suporte

- Documentação online
- Issues no GitHub
- Email de suporte

## Integração

### 1. API REST
- Endpoints documentados
- Autenticação via token
- Formato JSON

### 2. WebSocket
- Atualizações em tempo real
- Eventos de progresso
- Notificações

### 3. Webhooks
- Integração com CI/CD
- Notificações de commit
- Automações

## Roadmap

### Próximas Features
1. Comparação entre branches
2. Análise de código-fonte
3. Integração com CI/CD
4. Métricas de qualidade
5. Relatórios automáticos

### Melhorias Planejadas
1. Performance em grandes repos
2. Mais opções de visualização
3. Análise preditiva
4. Integração com IDEs
5. Mobile app 