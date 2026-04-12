# Sistema de Controle de Perdas na Colheita de Cana-de-Açúcar

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Oracle](https://img.shields.io/badge/Oracle-Database-red?logo=oracle)
![pytest](https://img.shields.io/badge/tested%20with-pytest-yellowgreen?logo=pytest)

---

## O problema

O Brasil é o maior produtor mundial de cana-de-açúcar, e o estado de São Paulo concentra a maior parte dessa produção. Com a mecanização acelerada da colheita, as perdas de biomassa no campo tornaram-se um problema econômico relevante: enquanto a colheita manual apresenta perdas de aproximadamente **5%**, a colheita mecânica pode gerar perdas de **até 15%** da produção.

Segundo dados da **SOCICANA** (Associação dos Fornecedores de Cana de Guariba), esse diferencial representa um impacto financeiro estimado em **cerca de R$ 20 milhões por ano** apenas no estado de São Paulo. Fatores como regulagem inadequada das colhedoras, perfil do operador e condições do talhão influenciam diretamente o nível de perda em cada operação.

Sem uma ferramenta que centralize e analise esses dados operacionais, os gestores de usinas e fornecedores de cana dependem de registros manuais fragmentados, o que dificulta a identificação de colhedoras ou operadores com desempenho abaixo do esperado e impede ações corretivas em tempo hábil.

---

## A solução

Este sistema é uma aplicação de linha de comando desenvolvida em Python que permite registrar, monitorar e analisar as perdas na colheita de cana-de-açúcar por talhão e por colhedora. Os dados são persistidos em um banco Oracle e também exportados em JSON para análise externa.

O sistema emite alertas automáticos quando a perda medida em uma colheita supera **10%**, permitindo intervenção imediata — como verificação da regulagem da colhedora. Relatórios analíticos agrupados por colhedora, por talhão e por operador facilitam a identificação de padrões recorrentes de perda e apoiam decisões de manutenção preventiva e treinamento de equipes.

Toda a lógica de negócio (cálculo de perdas em toneladas e em reais, alertas, agrupamentos) é coberta por testes unitários com `pytest`, garantindo confiabilidade das métricas apresentadas.

---

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.11+ | Linguagem principal |
| Oracle Database | Persistência relacional (tabelas `field`, `harvester`, `harvest_record`) |
| `oracledb` | Driver Python para conexão com Oracle |
| `python-dotenv` | Carregamento de variáveis de ambiente a partir do arquivo `.env` |
| `tabulate` | Formatação de tabelas no terminal |
| `pytest` | Suíte de testes unitários |

---

## Conteúdo técnico coberto (cap. 3–6)

| Requisito | Onde está implementado |
|---|---|
| Tipos de dados primitivos e compostos | `src/models/` — atributos tipados em `Field`, `Harvester`, `HarvestRecord` |
| Estruturas condicionais | `src/utils/validation.py` — validação de intervalos e formatos |
| Estruturas de repetição | `src/utils/validation.py` — laços `while True` com rejeição de entrada inválida |
| Funções e escopo | `src/services/`, `src/reports/report.py` — funções puras com retorno explícito |
| Classes e orientação a objetos | `src/models/field.py`, `src/models/harvester.py`, `src/models/harvest_record.py` |
| Manipulação de arquivos | `src/utils/file_io.py` — leitura/gravação de JSON e exportação de `.txt` |
| Banco de dados relacional | `src/db/schema.sql` + `src/db/connection.py` + `src/services/` |
| Testes unitários | `tests/` — cobertura de models, services, reports, validação e file I/O |

---

## Pré-requisitos

- Python **3.11** ou superior
- Oracle Database acessível (local ou remoto)
- Variáveis de ambiente configuradas (ver seção abaixo)

---

## Como executar

### 1. Criar e ativar o ambiente virtual (venv)

**Windows (cmd ou PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> Para desativar o ambiente virtual em qualquer plataforma: `deactivate`

---

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

```bash
# Linux/macOS
cp .env.example .env

# Windows (cmd)
copy .env.example .env
```

Edite o arquivo `.env` com suas credenciais Oracle:
```
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=host:porta/service_name
```

### 4. Criar as tabelas no banco

```bash
sqlplus ORACLE_USER/ORACLE_PASSWORD@ORACLE_DSN @src/db/schema.sql
```

### 5. Executar o sistema

```bash
python -m src.main
```

### 6. Executar os testes

```bash
pytest tests/ -v
```

---

## Exemplo de saída

```
╔══════════════════════════════════════════════════════╗
║   SISTEMA DE CONTROLE DE PERDAS NA COLHEITA DE CANA  ║
╚══════════════════════════════════════════════════════╝

  1. Cadastrar talhão
  2. Cadastrar colhedora
  3. Registrar colheita
  ──────────────────────────────────────────────────────
  4. Relatório por colhedora
  5. Relatório por talhão
  6. Relatório por operador
  7. Resumo geral
  ──────────────────────────────────────────────────────
  8. Exportar todos os registros (JSON)
  0. Sair

  Opção: 7

=== Relatório Resumo ===
Total de registros        : 5
Produção total estimada   : 980.00 t
Perda total               : 107.80 t  (11.00% médio)
Perda total em R$         : R$ 12.936,00
Qtd. de alertas (>10%)    : 3
```

```
  Opção: 4

=== Relatório por Colhedora ===
+-----------+----------------+-----------------+-----------------+-----------------+
| Colhedora | Qtd. Colheitas | Perda Média (%) | Perda Total (t) | Perda Total (R$)|
+===========+================+=================+=================+=================+
| COL-01    | 3              | 9.50            | 57.00           | 6.840,00        |
+-----------+----------------+-----------------+-----------------+-----------------+
| COL-02    | 2              | 13.50           | 50.80           | 6.096,00        |
+-----------+----------------+-----------------+-----------------+-----------------+
[ALERTA] Colhedora COL-02 com perda média de 13.50%
```

---

## Estrutura de pastas

```
farm-tech-solutions/
├── src/
│   ├── db/
│   │   ├── connection.py        # Conexão Oracle via oracledb + python-dotenv
│   │   └── schema.sql           # DDL: tabelas field, harvester, harvest_record
│   ├── models/
│   │   ├── field.py             # Classe Field (talhão)
│   │   ├── harvester.py         # Classe Harvester (colhedora)
│   │   └── harvest_record.py    # Classe HarvestRecord + cálculo de perdas
│   ├── services/
│   │   ├── field_service.py     # CRUD de talhões
│   │   ├── harvester_service.py # CRUD de colhedoras
│   │   └── harvest_service.py   # CRUD de registros + agrupamentos
│   ├── reports/
│   │   └── report.py            # Relatórios por colhedora, talhão, operador e resumo
│   └── utils/
│       ├── display.py           # Funções de saída colorida (sucesso, erro, alerta)
│       ├── file_io.py           # Leitura/gravação de JSON e exportação de .txt
│       └── validation.py        # Leitura validada de float, int, data e texto
├── tests/                       # Suíte pytest (sem dependência de Oracle)
├── data/
│   └── records.json             # Exportação local dos registros
├── .env.example                 # Template de variáveis de ambiente
├── requirements.txt
└── README.md
```

---

## Integrantes do grupo

| Nome                 | RM          |
|----------------------|-------------|
| _Geovani Nepomoceno_ | _rm570373_          |

# farm-tech-solutions-2-6
