# Git Metrics

Uma ferramenta poderosa para análise de métricas de repositórios Git, disponível tanto em interface de linha de comando (CLI) quanto em interface web.

## Descrição

O Git Metrics é uma ferramenta versátil que analisa repositórios Git e gera relatórios detalhados sobre as contribuições dos desenvolvedores. Oferece duas interfaces principais:

### Interface CLI
- Ferramenta de linha de comando para análises rápidas e automação
- Geração de relatórios em Excel
- Ideal para integração com scripts e pipelines

### Interface Web
- Dashboard interativo com gráficos dinâmicos
- Visualização em tempo real das métricas
- Filtros interativos sincronizados por autor e período
- Interface amigável para análise visual dos dados
- Sistema de cache para melhor performance

## Funcionalidades

### Funcionalidades Comuns (CLI e Web)
- Análise de commits por autor
- Estatísticas diárias e mensais
- Métricas por ambiente (PRD/HML)
- Análise de branches
- Suporte a múltiplos autores

### Funcionalidades Específicas CLI
- Relatórios em Excel com formatação profissional
- Exportação de dados em diferentes formatos
- Integração com ferramentas de linha de comando

### Funcionalidades Específicas Web
- Gráficos interativos e responsivos
- Filtros dinâmicos sincronizados por autor e período
- Visualização em tempo real
- Dashboard personalizado
- Exportação de gráficos
- Sistema de cache inteligente
- Tratamento avançado de dados vazios
- Feedback visual aprimorado

## Requisitos

- Python 3.8 ou superior
- Git instalado e configurado
- Acesso ao repositório que deseja analisar
- Navegador moderno (para interface web)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/git-metrics.git
cd git-metrics
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale o pacote em modo de desenvolvimento:
```bash
pip install -e .
```

## Uso

### Interface CLI

#### Comando Básico
```bash
git-metrics --path /caminho/do/repositorio --author email@exemplo.com
```

#### Análise de Múltiplos Autores
```bash
git-metrics --path /caminho/do/repositorio --author email1@exemplo.com --author email2@exemplo.com
```

#### Parâmetros CLI
- `--path, -p`: Caminho do repositório Git para análise (obrigatório)
- `--author, -a`: Email do(s) autor(es) para filtrar (opcional, pode ser usado múltiplas vezes)
- `--format`: Formato de saída (excel, json, csv) - padrão: excel
- `--output`: Diretório de saída para os relatórios

### Interface Web

#### Iniciando o Servidor
```bash
git-metrics-web --port 8000
```

#### Acessando a Interface
1. Abra seu navegador
2. Acesse `http://localhost:8000`
3. Selecione o repositório para análise
4. Use os filtros interativos para personalizar a visualização

#### Recursos Web
- Dashboard principal com visão geral
- Gráficos interativos de:
  - Métricas por Autor
  - Métricas por Ambiente
  - Totais Diários
  - Totais Mensais
- Tabela de autores com detalhes
- Filtros dinâmicos sincronizados:
  - Seleção de autor com atualização automática
  - Filtro de período com validação
  - Sincronização automática entre filtros
- Exportação de gráficos e dados
- Tratamento inteligente de dados ausentes
- Feedback visual para dados vazios

## Estrutura dos Relatórios

### Relatório Excel (CLI)

1. **Aba Resumo Geral**
   - Resumo por Autor e Ambiente (Azul)
   - Resumo por Ambiente (Verde)
   - Totais Diários (Vermelho)
   - Totais Mensais (Laranja)

2. **Aba Estatísticas por Branch**
   - Métricas detalhadas por branch
   - Filtros e totalizadores

3. **Aba Estatísticas Diárias**
   - Análise dia a dia
   - Tendências e padrões

4. **Aba Estatísticas Mensais**
   - Visão consolidada mensal
   - Evolução ao longo do tempo

5. **Aba Informações**
   - Metadados do relatório
   - Detalhes da execução

### Dashboard Web

1. **Visão Geral**
   - Gráficos interativos com animações suaves
   - Métricas em tempo real com cache
   - Filtros dinâmicos sincronizados
   - Feedback visual aprimorado

2. **Análise por Autor**
   - Contribuições individuais com histórico detalhado
   - Comparativo entre autores com métricas precisas
   - Histórico de commits com filtragem por período
   - Sincronização automática com outros filtros

3. **Análise por Ambiente**
   - Distribuição PRD/HML com dados filtrados
   - Impacto por ambiente com métricas atualizadas
   - Tendências com base no período selecionado
   - Visualização clara de dados ausentes

4. **Análise Temporal**
   - Visão diária e mensal sincronizada
   - Gráficos de tendência com dados filtrados
   - Períodos de maior atividade por autor
   - Tratamento inteligente de períodos sem dados

## Arquitetura

O projeto segue uma arquitetura limpa e moderna, baseada em:

- Clean Architecture
- Princípios SOLID
- Command Query Separation (CQS)
- Domain-Driven Design (DDD)

Para mais detalhes sobre a arquitetura, consulte [ARQUITETURA.md](docs/ARQUITETURA.md).

## Desenvolvimento

### Estrutura do Projeto

```
git-metrics/
├── src/
│   ├── application/     # Lógica de aplicação
│   ├── domain/         # Entidades e regras de negócio
│   ├── infrastructure/ # Implementações técnicas
│   ├── presentation/   # Interface com usuário
│   └── web/           # Interface web e assets
├── tests/             # Testes
├── docs/             # Documentação
└── requirements/     # Requisitos do projeto
```

### Executando Testes

```bash
pytest
```

### Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Boas Práticas

O projeto segue:

- Type hints para melhor documentação
- Docstrings em classes e métodos
- Tratamento adequado de erros
- Princípios de Clean Code
- Testes automatizados
- Documentação clara e atualizada

## Suporte

Para reportar bugs ou sugerir melhorias:

1. Abra uma issue no GitHub
2. Descreva o problema/sugestão detalhadamente
3. Inclua exemplos e logs relevantes

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

Michel Bueno Silva - [michelbueno01@gmail.com](mailto:michelbueno01@gmail.com)

## Agradecimentos

- Equipe de desenvolvimento
- Contribuidores
- Comunidade Python 
