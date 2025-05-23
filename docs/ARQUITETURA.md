# Arquitetura do Git Metrics

## Visão Geral

O Git Metrics é estruturado seguindo os princípios de Clean Architecture, SOLID e Command Query Separation (CQS). A arquitetura é dividida em camadas bem definidas, cada uma com sua responsabilidade específica.

## Estrutura do Projeto

```
git-metrics/
├── src/
│   ├── application/      # Camada de aplicação
│   ├── domain/          # Camada de domínio
│   ├── infrastructure/  # Camada de infraestrutura
│   └── presentation/    # Camada de apresentação
├── tests/              # Testes
└── docs/              # Documentação
```

## Camadas da Arquitetura

### 1. Camada de Domínio (Domain Layer)

A camada mais interna da aplicação, contendo as regras de negócio centrais.

#### Estrutura:
```
domain/
├── entities/        # Entidades de domínio
├── enums/          # Enumerações
└── value_objects/  # Objetos de valor
```

#### Componentes Principais:
- **Entities**: Classes que representam os objetos principais do domínio
  - `Author`: Representa um autor de commits
  - `Commit`: Representa um commit no repositório

- **Enums**: Enumerações que definem tipos específicos do domínio
  - `EnvironmentType`: Define os tipos de ambiente (PRD/HML)

### 2. Camada de Aplicação (Application Layer)

Contém a lógica de aplicação e implementa os casos de uso.

#### Estrutura:
```
application/
├── commands/      # Comandos (modificam estado)
├── queries/       # Consultas (apenas leitura)
└── interfaces/    # Interfaces e contratos
```

#### Padrão CQS (Command Query Separation):
- **Commands**: Operações que modificam estado
  - `GenerateExcelReportCommand`: Gera relatório Excel

- **Queries**: Operações de leitura
  - `CommitStatisticsQuery`: Obtém estatísticas de commits

### 3. Camada de Infraestrutura (Infrastructure Layer)

Implementa as interfaces definidas nas camadas superiores e fornece recursos técnicos.

#### Estrutura:
```
infrastructure/
├── repositories/   # Implementações de repositórios
└── config/        # Configurações
```

#### Componentes:
- **Repositories**: Implementações concretas dos repositórios
  - `GitRepository`: Implementa acesso ao repositório Git

### 4. Camada de Apresentação (Presentation Layer)

Interface com o usuário e formatação de dados.

#### Estrutura:
```
presentation/
├── cli/           # Interface de linha de comando
└── console/       # Formatação de saída no console
```

## Princípios SOLID Aplicados

1. **Single Responsibility (SRP)**
   - Cada classe tem uma única responsabilidade
   - Exemplo: `GitRepository` lida apenas com operações Git

2. **Open/Closed (OCP)**
   - Classes são abertas para extensão, fechadas para modificação
   - Uso de interfaces permite adicionar novas implementações

3. **Liskov Substitution (LSP)**
   - Implementações podem substituir suas interfaces
   - `GitRepository` implementa `GitRepositoryInterface`

4. **Interface Segregation (ISP)**
   - Interfaces específicas para cada necessidade
   - Separação entre comandos e consultas

5. **Dependency Inversion (DIP)**
   - Dependências através de abstrações
   - Uso de injeção de dependência

## Padrão CQS (Command Query Separation)

### Queries (Consultas)
- Retornam dados
- Não modificam estado
- Exemplo: `CommitStatisticsQuery`

### Commands (Comandos)
- Executam ações
- Podem modificar estado
- Exemplo: `GenerateExcelReportCommand`

## Fluxo de Dados

1. **Entrada**
   - CLI recebe parâmetros
   - Validação inicial

2. **Processamento**
   - Query obtém dados do repositório
   - Command gera relatório

3. **Saída**
   - Geração de relatório Excel
   - Feedback no console

## Boas Práticas Implementadas

1. **Type Hints**
   - Uso consistente de tipagem
   - Melhor documentação do código

2. **Documentação**
   - Docstrings em classes e métodos
   - Comentários explicativos

3. **Tratamento de Erros**
   - Exceções específicas
   - Mensagens claras

4. **Clean Code**
   - Nomes descritivos
   - Funções pequenas e focadas
   - Código organizado

## Extensibilidade

O projeto foi projetado para ser facilmente extensível:

1. **Novos Relatórios**
   - Criar novo Command
   - Implementar geração

2. **Novas Análises**
   - Adicionar nova Query
   - Implementar lógica

3. **Novos Formatos**
   - Implementar novo Command
   - Reutilizar queries existentes 