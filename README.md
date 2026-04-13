# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# FarmTech Solutions — Sistema de Controle de Perdas na Colheita de Cana-de-Açúcar

## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/geovani-nepomoceno/">Geovani Nepomoceno — RM 570373</a>

## 👩‍🏫 Professores:
### Tutor(a)
- Sabrina Otoni
### Coordenador(a)
- André Godoi Chiovato

---

## 📜 Descrição

O Brasil é o maior produtor mundial de cana-de-açúcar, e o estado de São Paulo concentra a maior parte dessa produção. Com a mecanização acelerada da colheita, as perdas de biomassa no campo tornaram-se um problema econômico relevante: enquanto a colheita manual apresenta perdas de aproximadamente **5%**, a colheita mecânica pode gerar perdas de **até 15%** da produção.

Segundo dados da **SOCICANA** (Associação dos Fornecedores de Cana de Guariba), esse diferencial representa um impacto financeiro estimado em **cerca de R$ 20 milhões por ano** apenas no estado de São Paulo. Fatores como regulagem inadequada das colhedoras, perfil do operador e condições do talhão influenciam diretamente o nível de perda em cada operação.

Sem uma ferramenta que centralize e analise esses dados operacionais, os gestores de usinas e fornecedores de cana dependem de registros manuais fragmentados, o que dificulta a identificação de colhedoras ou operadores com desempenho abaixo do esperado e impede ações corretivas em tempo hábil.

Este sistema é uma aplicação de linha de comando desenvolvida em **Python** que permite registrar, monitorar e analisar as perdas na colheita de cana-de-açúcar por talhão e por colhedora. Os dados são persistidos em um banco **Oracle Database** e também exportados em JSON para análise externa.

O sistema emite **alertas automáticos** quando a perda medida em uma colheita supera **10%**, permitindo intervenção imediata — como verificação da regulagem da colhedora. Relatórios analíticos agrupados por colhedora, por talhão e por operador facilitam a identificação de padrões recorrentes de perda e apoiam decisões de manutenção preventiva e treinamento de equipes.

Toda a lógica de negócio (cálculo de perdas em toneladas e em reais, alertas, agrupamentos) é coberta por **testes unitários com `pytest`**, garantindo confiabilidade das métricas apresentadas.

**Funcionalidades principais:**
- Cadastro de talhões e colhedoras
- Registro de colheitas com cálculo automático de perdas (% e R$)
- Alertas quando a perda supera 10%
- Relatórios por colhedora, por talhão, por operador e resumo geral
- Exportação de registros em JSON e relatórios em `.txt`

**Conteúdo técnico coberto (cap. 3–6):**

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

## 📁 Estrutura de pastas

```
farm-tech-solutions-2-6/
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
├── assets/                      # Imagens e recursos estáticos
├── docker-compose.yml           # Oracle Database Express via Docker
├── .env.example                 # Template de variáveis de ambiente
├── requirements.txt
└── README.md
```

---

## 🔧 Como executar o código

### Pré-requisitos

- **Python 3.11** ou superior
- **Oracle Database** acessível — local, remoto, ou via Docker (ver seção abaixo)
- `pip` para instalação das dependências

---

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/farm-tech-solutions-2-6.git
cd farm-tech-solutions-2-6
```

### 2. Criar e ativar o ambiente virtual

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

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

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

### 5. Criar as tabelas no banco

```bash
sqlplus ORACLE_USER/ORACLE_PASSWORD@ORACLE_DSN @src/db/schema.sql
```

### 6. Executar o sistema

```bash
python -m src.main
```

### 7. Executar os testes

```bash
pytest tests/ -v
```

---

### 🐳 Opcional — Subindo o Oracle com Docker Compose

Caso não tenha uma instância Oracle disponível, você pode subir o **Oracle Database 21c Express Edition** localmente usando Docker.

**Pré-requisito:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.

**1. Iniciar o container:**
```bash
docker compose up -d
```

**2. Aguardar a inicialização** (~60 segundos). Acompanhe o log:
```bash
docker logs -f oracle-fiap
```
Aguarde a mensagem `DATABASE IS READY TO USE!` antes de prosseguir.

**3. Configurar o `.env`** com as credenciais do container:
```
ORACLE_USER=system
ORACLE_PASSWORD=fiap_password
ORACLE_DSN=localhost:1521/XEPDB1
```

**4. Parar o container** (preserva os dados no volume `oracle-data`):
```bash
docker compose down
```

> Para remover também o volume de dados: `docker compose down -v`

---

### Exemplo de saída

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

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
