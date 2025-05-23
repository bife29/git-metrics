# Git Metrics

Uma ferramenta poderosa para análise de métricas de repositórios Git, com geração de relatórios em Excel.

## Descrição

O Git Metrics é uma ferramenta de linha de comando que analisa repositórios Git e gera relatórios detalhados sobre as contribuições dos desenvolvedores. Ele oferece análises por autor, ambiente (PRD/HML), período e branch, apresentando os dados em um formato organizado e fácil de entender.

## Funcionalidades

- Análise de commits por autor
- Estatísticas diárias e mensais
- Métricas por ambiente (PRD/HML)
- Análise de branches
- Relatórios em Excel com formatação profissional
- Suporte a múltiplos autores
- Interface de linha de comando intuitiva

## Requisitos

- Python 3.8 ou superior
- Git instalado e configurado
- Acesso ao repositório que deseja analisar

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

### Comando Básico

```bash
git-metrics --path /caminho/do/repositorio --author email@exemplo.com
```

### Análise de Múltiplos Autores

```bash
git-metrics --path /caminho/do/repositorio --author email1@exemplo.com --author email2@exemplo.com
```

### Parâmetros

- `--path, -p`: Caminho do repositório Git para análise (obrigatório)
- `--author, -a`: Email do(s) autor(es) para filtrar (opcional, pode ser usado múltiplas vezes)

## Estrutura dos Relatórios

### Relatório Excel

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
│   └── presentation/   # Interface com usuário
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

Michel Bueno Silva - [michelbueno01@gmail.com](mailto:michelbueno01@gmail.comr)

## Agradecimentos

- Equipe de desenvolvimento
- Contribuidores
- Comunidade Python 
