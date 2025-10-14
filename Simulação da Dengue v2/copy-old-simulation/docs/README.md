# 🦟 Simulação de Dengue usando Agent-Based Modeling (ABM)

> Modelo baseado em agentes para simular a propagação de dengue em populações urbanas

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Características](#-características)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Exemplos de Simulação](#-exemplos-de-simulação)
- [Resultados](#-resultados)
- [Otimizações](#-otimizações)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

Este projeto implementa um **modelo baseado em agentes (ABM)** para simular a propagação da dengue em áreas urbanas, usando **Python** e a biblioteca **Mesa**. O modelo foi inspirado na simulação original em **NetLogo**, mas completamente reescrito e otimizado para Python.

### Proposta do Código

Simular a dinâmica de transmissão da dengue através de interações entre:
- **Agentes humanos** (suscetíveis, infectados, recuperados)
- **Agentes mosquitos** (Aedes aegypti - saudáveis, infectados)
- **Ambiente espacial** (grade representando área urbana)

---

### 🏆 Resultado Final

**Placar: Python 8 × 3 NetLogo**

---

## 🎭 Quando Usar Cada Um?

### Use **NetLogo** 🐢 se você:

- ✅ Está **aprendendo** ABM pela primeira vez
- ✅ Precisa de **protótipos rápidos** (< 1 dia)
- ✅ Quer **demonstrações visuais** interativas
- ✅ Trabalha com **simulações pequenas** (< 10.000 agentes)
- ✅ Não tem experiência com programação
- ✅ Foca em **ensino** e educação

### Use **Python/Mesa** 🐍 se você:

- ✅ Precisa de **performance** (> 10.000 agentes)
- ✅ Quer **análises estatísticas avançadas**
- ✅ Vai **publicar resultados** científicos
- ✅ Quer **automatizar** simulações (CI/CD)
- ✅ Precisa de **reprodutibilidade estrita**
- ✅ Planeja **escalar** para simulações massivas

---

## ✨ Características

### Modelo Epidemiológico

- 🦠 **Modelo SIR** (Suscetível-Infectado-Recuperado) para humanos
- 🦟 **Modelo SI** (Suscetível-Infectado) para mosquitos
- 💉 **Transmissão vetorial** realista (mosquito ↔ humano)
- 🔬 **Períodos de incubação** e viremia corretos
- 🧬 **Herança transovárica** (transmissão vertical em mosquitos)
- ⚕️ **Taxa de letalidade** configurável
- 🔄 **Imunidade permanente** após recuperação

### Dinâmica Populacional

- 👥 **População humana** com envelhecimento e mortalidade
- 🦟 **População de mosquitos** com reprodução sazonal
- 📍 **Movimento espacial** de agentes (humanos e mosquitos)
- 🌍 **Grade toroidal** (sem bordas - mais realista)
- 📊 **Coleta de dados** temporal configurável

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd "Simulação da Dengue v2/copy-old-simulation"
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências principais:**
- `mesa` - Framework de ABM
- `matplotlib` - Visualização de gráficos
- `pandas` - Análise de dados
- `numpy` - Computação numérica

---

## 📖 Como Usar

### 1️⃣ Teste Rápido (30 segundos)

Valida se tudo está funcionando:

```bash
python test_optimized.py
```

**Saída esperada:**
- ✅ Completa em < 60 segundos
- ✅ Velocidade > 100 dias/segundo
- ✅ Gráfico gerado em `results/`

---

### 2️⃣ Simulação Simples (< 5 segundos)

Para testes e desenvolvimento:

```bash
python main.py
```

**Características:**
- População pequena (20 humanos, 30 mosquitos)
- 30 dias de simulação
- Ultra-rápido para debugging

---

### 3️⃣ Simulação Realista de Cidade (6-10 segundos) ⭐

**Recomendado para análises científicas:**

```bash
python simulation_realistic_city.py
```

**Características:**
- 🏙️ Cidade média: 100.000 habitantes (escala 1:100)
- 🦟 7.000 mosquitos (proporção 7:1)
- 📅 365 dias (1 ano completo)
- 📊 Dados diários coletados
- 📈 Curvas epidêmicas detalhadas

**Arquivos gerados:**
- `results/realistic_city_*.png` - Gráfico principal
- `results/epidemic_curve_detailed_*.png` - Curvas detalhadas
- `results/simulation_data_*.csv` - Dados completos (365 dias)
- `results/metadata_*.txt` - Metadados da simulação

---

### 4️⃣ Análise Estatística (30 min)

Para estudos com intervalos de confiança:

```bash
python robust_simulation_fast.py
```

**Características:**
- 10 simulações de 180 dias cada
- Análise comparativa (3 cenários)
- Estatísticas com IC 95%
- ~20-30 minutos de execução

---

## 📊 Exemplos de Simulação

### Exemplo 1: Simulação Básica

```python
from model.model import DengueABM
from visualization.plot_results import plot_model_results

# Criar modelo
model = DengueABM(
    width=30,
    height=30,
    initial_humans=500,
    initial_mosquitoes=2000,
    initial_infected_humans=5,
    initial_infected_mosquitoes=25
)

# Executar 180 dias
for day in range(180):
    model.step()
    if day % 30 == 0:
        print(f"Dia {day}: {model.people_count_with_dengue} infectados")

# Plotar resultados
plot_model_results(model, "results/my_simulation.png")
```

### Exemplo 2: Múltiplas Simulações

```python
from analysis.evaluate_model import run_multiple_simulations
import pandas as pd

params = {
    "width": 30,
    "height": 30,
    "initial_humans": 500,
    "initial_mosquitoes": 2000,
    "initial_infected_humans": 5,
    "initial_infected_mosquitoes": 25
}

# Executar 10 simulações
results = run_multiple_simulations(
    DengueABM, 
    params, 
    n_simulations=10, 
    steps=180
)

# Analisar resultados
print(f"Média de infectados: {results['total_infected'].mean():.1f}")
print(f"Desvio padrão: {results['total_infected'].std():.1f}")

# Salvar
results.to_csv("results/my_analysis.csv")
```

### Exemplo 3: Cenário de Controle Vetorial

```python
# Cenário ANTES do controle
model_before = DengueABM(
    width=30,
    height=30,
    initial_humans=500,
    initial_mosquitoes=2000,  # Muitos mosquitos
    initial_infected_humans=5
)

# Cenário DEPOIS do controle
model_after = DengueABM(
    width=30,
    height=30,
    initial_humans=500,
    initial_mosquitoes=500,   # Redução de 75%
    initial_infected_humans=5
)

# Comparar resultados...
```

---

## 📊 Resultados

### Simulação de Cidade Média (100.000 habitantes)

**Parâmetros:**
- População: 100.000 habitantes
- Mosquitos: 700.000 (proporção 7:1)
- Duração: 365 dias
- Taxa inicial: 0.2%

**Resultados:**
- ✅ **Taxa de ataque:** 91.7% da população
- ✅ **Pico:** Dia 189 (~6 meses)
- ✅ **Casos no pico:** 54.800 simultâneos
- ✅ **Comportamento:** Curva epidêmica clássica

### Gráficos Gerados

#### 1. População ao Longo do Tempo
![População](results/realistic_city_example.png)

*Mostra evolução de suscetíveis, infectados e recuperados*

#### 2. Curva Epidêmica Detalhada
![Curva Epidêmica](results/epidemic_curve_example.png)

*Casos ativos, acumulados, mosquitos e prevalência*

---

## ⚡ Otimizações

Este projeto foi **extensivamente otimizado** para performance máxima:

### Melhorias Implementadas (8 no total):

1. ✅ **Cache de vizinhanças** (50-70% mais rápido)
2. ✅ **DataCollector otimizado** (elimina 5 iterações)
3. ✅ **Coleta de dados configurável** (85% menos overhead)
4. ✅ **Controle populacional** (evita explosão de mosquitos)
5. ✅ **Iterações unificadas** (3x menos loops)
6. ✅ **Movimento reduzido** (3x menos operações)
7. ✅ **Reprodução otimizada** (7x menos overhead)
8. ✅ **Picadas inteligentes** (30-50% mais rápido)

**Veja documentação completa:** [OPTIMIZACOES.md](OPTIMIZACOES.md)

---

## 🎓 Casos de Uso

### 1. Ensino e Educação
```python
# Demonstrar conceito de R₀
# Execute com diferentes densidades de mosquitos
```

### 2. Planejamento de Saúde Pública
```python
# Estimar capacidade hospitalar necessária
peak_cases = 54800
hospitalization_rate = 0.10
beds_needed = peak_cases * hospitalization_rate
print(f"Leitos necessários: {beds_needed}")
```

### 3. Avaliação de Intervenções
```python
# Comparar cenários: com e sem controle vetorial
# Quantificar benefício de reduzir mosquitos
```

---

## 🛠️ Configuração Avançada

### Ajustar Parâmetros do Modelo

Edite `simulation_realistic_city.py`:

```python
model = DengueABM(
    width=50,                           # Tamanho da grade
    height=50,
    initial_humans=1000,                # População inicial
    initial_mosquitoes=7000,            # Mosquitos iniciais
    initial_infected_humans=2,          # Casos iniciais
    initial_infected_mosquitoes=70,     # Mosquitos infectados
    mosquitoes_eggs=60,                 # Ovos por fêmea
    inherit_dengue_eggs_percentage=8,   # Herança transovárica (%)
    fatality_percentage=0.5             # Letalidade (%)
)

# Ajustar frequência de coleta
model.data_collection_frequency = 7  # Coletar a cada 7 dias
```

### Ajustar Performance vs Detalhe

**Para mais velocidade:**
```python
# Menos população
initial_humans=500
initial_mosquitoes=2000

# Menos dias
for day in range(90):  # 3 meses ao invés de 1 ano

# Coleta menos frequente
model.data_collection_frequency = 14  # Quinzenal
```

**Para mais precisão:**
```python
# Mais população
initial_humans=2000
initial_mosquitoes=14000

# Grade maior
width=70, height=70

# Coleta diária
model.data_collection_frequency = 1
```

---

## 🚀 Início Rápido

```bash
# 1. Instalar
pip install -r requirements.txt

# 2. Testar
python test_optimized.py

# 3. Simular cidade realista
python simulation_realistic_city.py

# 4. Analisar resultados
# Veja arquivos em results/
```

---

<div align="center">

[⬆ Voltar ao topo](#-simulação-de-dengue-usando-agent-based-modeling-abm)

</div>

