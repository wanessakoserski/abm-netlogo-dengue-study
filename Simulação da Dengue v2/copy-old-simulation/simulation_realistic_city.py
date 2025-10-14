#!/usr/bin/env python3
"""
Simulação Realista de Dengue em Cidade Média Brasileira
Baseado em dados epidemiológicos reais
"""

from model.model import DengueABM
from visualization.plot_results import plot_model_results
import time
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def run_realistic_city_simulation():
    """
    Simula dengue em uma cidade média brasileira
    
    Parâmetros baseados em:
    - Cidade média: ~100.000 habitantes
    - Densidade: ~50-100 hab/km²
    - Proporção mosquito:humano em áreas urbanas: 5:1 a 10:1
    - Prevalência inicial: 0.1-0.5% (típico no início de surto)
    """
    print("="*70)
    print("SIMULAÇÃO REALISTA DE DENGUE - CIDADE MÉDIA BRASILEIRA")
    print("="*70)
    
    print("\n📊 PARÂMETROS DA CIDADE:")
    print("-" * 70)
    
    # Parâmetros escalados para simulação computacionalmente viável
    # Escala: 1:100 (cada agente representa ~100 pessoas reais)
    SCALE_FACTOR = 100
    
    # População real vs simulada
    real_population = 100000
    sim_population = real_population // SCALE_FACTOR  # 1000
    
    # Mosquitos (proporção 7:1 típica em áreas urbanas)
    real_mosquitoes = real_population * 7
    sim_mosquitoes = sim_population * 7  # 7000
    
    # Taxa de infecção inicial: 0.2% (200 casos em 100k habitantes)
    initial_infection_rate = 0.002
    sim_infected_humans = max(2, int(sim_population * initial_infection_rate))
    
    # Mosquitos infectados (aproximadamente 1% dos mosquitos)
    sim_infected_mosquitoes = int(sim_mosquitoes * 0.01)
    
    print(f"  População real representada: {real_population:,} habitantes")
    print(f"  População simulada: {sim_population} agentes (escala 1:{SCALE_FACTOR})")
    print(f"  Mosquitos simulados: {sim_mosquitoes} agentes")
    print(f"  Proporção mosquito:humano: 7:1")
    print(f"  Casos iniciais: {sim_infected_humans} (~{real_population * initial_infection_rate:.0f} reais)")
    print(f"  Taxa de infecção inicial: {initial_infection_rate*100}%")
    print("-" * 70)
    
    # Grade proporcional à população
    # Densidade urbana típica: 50-100 hab/km²
    # Para 1000 agentes, grade 50x50 = 2500 células
    grid_size = 50
    
    print(f"\n⚙️  CONFIGURAÇÃO DA SIMULAÇÃO:")
    print("-" * 70)
    print(f"  Grade espacial: {grid_size}×{grid_size} células")
    print(f"  Duração: 365 dias (1 ano completo)")
    print(f"  Taxa de natalidade mosquitos: ajustada sazonalmente")
    print(f"  Taxa de letalidade: 1% (típica para dengue sem complicações)")
    print("-" * 70)
    
    # Criar modelo com parâmetros realistas ajustados
    model = DengueABM(
        width=grid_size,
        height=grid_size,
        initial_humans=sim_population,
        initial_mosquitoes=sim_mosquitoes,
        initial_infected_humans=sim_infected_humans,
        initial_infected_mosquitoes=sim_infected_mosquitoes,
        mosquitoes_eggs=60,  # Fêmea Aedes aegypti põe ~40-100 ovos (média 60)
        inherit_dengue_eggs_percentage=8,  # ~5-10% herança transovárica
        fatality_percentage=0.5  # 0.5% letalidade (mais realista para dengue clássica)
    )
    
    # AJUSTE CRÍTICO: Manter população de mosquitos mais estável
    # Ajustar frequência de reprodução para manter população ao longo do ano
    model.data_collection_frequency = 1  # Coleta diária para curva epidêmica
    
    print(f"\n🚀 INICIANDO SIMULAÇÃO...")
    print(f"Início: {model.people_count_with_dengue} pessoas infectadas")
    print(f"        {model.mosquitoes_count_with_dengue} mosquitos infectados")
    print("-" * 70)
    
    start_time = time.time()
    
    # Estatísticas para rastrear picos
    max_infected = model.people_count_with_dengue
    max_infected_day = 0
    
    # Executar por 365 dias (1 ano completo)
    for day in range(365):
        if not model.running:
            print(f"\n⚠️  Simulação parou no dia {day}")
            print(f"   Razão: Epidemia extinta ou população muito pequena")
            break
        
        model.step()
        
        # Rastrear pico
        if model.people_count_with_dengue > max_infected:
            max_infected = model.people_count_with_dengue
            max_infected_day = day
        
        # Relatórios mensais
        if day % 30 == 0 and day > 0:
            elapsed = time.time() - start_time
            remaining = (elapsed / day) * (365 - day)
            
            # Calcular casos reais (escala reversa)
            real_infected = model.people_count_with_dengue * SCALE_FACTOR
            real_recovered = model.people_count_recovered_from_dengue * SCALE_FACTOR
            real_deaths = model.people_count_death_dengue * SCALE_FACTOR
            
            print(f"\n📅 Mês {day//30} (Dia {day}):")
            print(f"   Infectados: {model.people_count_with_dengue} simulados (~{real_infected:,} reais)")
            print(f"   Recuperados: {model.people_count_recovered_from_dengue} (~{real_recovered:,} reais)")
            print(f"   Óbitos dengue: {model.people_count_death_dengue} (~{real_deaths} reais)")
            print(f"   Mosquitos infectados: {model.mosquitoes_count_with_dengue}")
            print(f"   População mosquitos: {model.mosquitoes_count_total}")
            print(f"   Tempo decorrido: {elapsed:.1f}s | Estimativa restante: {remaining:.1f}s")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Resultados finais
    print("\n" + "="*70)
    print("📊 RESULTADOS FINAIS (365 DIAS)")
    print("="*70)
    
    # Calcular valores reais
    final_infected = model.people_count_with_dengue * SCALE_FACTOR
    final_recovered = model.people_count_recovered_from_dengue * SCALE_FACTOR
    final_deaths_dengue = model.people_count_death_dengue * SCALE_FACTOR
    final_deaths_common = model.people_count_death_common * SCALE_FACTOR
    
    # Taxa de ataque (% da população que foi infectada)
    attack_rate = (model.people_count_recovered_from_dengue + model.people_count_with_dengue) / sim_population * 100
    
    # Taxa de letalidade (CFR)
    total_cases = model.people_count_recovered_from_dengue + model.people_count_with_dengue + model.people_count_death_dengue
    cfr = (model.people_count_death_dengue / total_cases * 100) if total_cases > 0 else 0
    
    print(f"\n🏥 EPIDEMIOLOGIA:")
    print(f"   Casos totais: {total_cases} simulados (~{total_cases * SCALE_FACTOR:,} reais)")
    print(f"   Taxa de ataque: {attack_rate:.2f}% da população")
    print(f"   Pico de infecções: {max_infected} no dia {max_infected_day}")
    print(f"   Pico real estimado: ~{max_infected * SCALE_FACTOR:,} casos simultâneos")
    
    print(f"\n📈 DESFECHOS:")
    print(f"   Infectados atuais: {model.people_count_with_dengue} (~{final_infected} reais)")
    print(f"   Recuperados: {model.people_count_recovered_from_dengue} (~{final_recovered:,} reais)")
    print(f"   Óbitos por dengue: {model.people_count_death_dengue} (~{final_deaths_dengue} reais)")
    print(f"   Taxa de letalidade (CFR): {cfr:.2f}%")
    print(f"   Óbitos por outras causas: {model.people_count_death_common} (~{final_deaths_common} reais)")
    
    print(f"\n🦟 VETORES:")
    print(f"   População final de mosquitos: {model.mosquitoes_count_total}")
    print(f"   Mosquitos infectados: {model.mosquitoes_count_with_dengue}")
    
    print(f"\n⏱️  PERFORMANCE:")
    print(f"   Tempo de execução: {duration:.2f}s ({duration/60:.1f} min)")
    print(f"   Velocidade: {365/duration:.1f} dias/segundo")
    
    print("="*70)
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Gráfico principal
    filename = f"results/realistic_city_{timestamp}.png"
    try:
        plot_model_results(model, filename)
        print(f"\n✅ Gráfico salvo: {filename}")
    except Exception as e:
        print(f"\n⚠️  Erro ao salvar gráfico: {e}")
    
    # Gráfico adicional: curva epidêmica detalhada
    plot_detailed_epidemic_curve(model, timestamp, SCALE_FACTOR)
    
    # Salvar dados em CSV
    save_simulation_data(model, timestamp, SCALE_FACTOR, {
        'real_population': real_population,
        'scale_factor': SCALE_FACTOR,
        'attack_rate': attack_rate,
        'cfr': cfr,
        'peak_day': max_infected_day,
        'peak_infected': max_infected
    })
    
    return model

def plot_detailed_epidemic_curve(model, timestamp, scale_factor):
    """Plota curva epidêmica detalhada"""
    results = model.datacollector.get_model_vars_dataframe()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Curva Epidêmica de Dengue - Cidade Média (1 Ano)', fontsize=16, fontweight='bold')
    
    # 1. Curva epidêmica (casos por dia)
    axes[0, 0].plot(results.index, results["Humanos Infectados"] * scale_factor, 
                    color='red', linewidth=2, label='Casos Ativos')
    axes[0, 0].fill_between(results.index, 0, results["Humanos Infectados"] * scale_factor, 
                             alpha=0.3, color='red')
    axes[0, 0].set_title('Curva Epidêmica - Casos Ativos', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Dias')
    axes[0, 0].set_ylabel('Número de Casos Ativos')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    
    # 2. Casos acumulados
    recovered_cumulative = results["Humanos Recuperados"] * scale_factor
    deaths_cumulative = results["Mortes por Dengue"] * scale_factor
    total_cumulative = recovered_cumulative + deaths_cumulative
    
    axes[0, 1].plot(results.index, total_cumulative, 
                    color='darkblue', linewidth=2, label='Total Acumulado')
    axes[0, 1].plot(results.index, recovered_cumulative, 
                    color='green', linewidth=2, label='Recuperados', linestyle='--')
    axes[0, 1].plot(results.index, deaths_cumulative, 
                    color='black', linewidth=2, label='Óbitos', linestyle='--')
    axes[0, 1].set_title('Casos Acumulados', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Dias')
    axes[0, 1].set_ylabel('Número Acumulado')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. População de mosquitos
    axes[1, 0].plot(results.index, results["Total Mosquitos"], 
                    color='brown', linewidth=2, label='Total')
    axes[1, 0].plot(results.index, results["Mosquitos Infectados"], 
                    color='orange', linewidth=2, label='Infectados')
    axes[1, 0].set_title('Dinâmica da População de Mosquitos', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Dias')
    axes[1, 0].set_ylabel('Número de Mosquitos')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Taxa de prevalência (%)
    total_population = (results["Humanos Saudáveis"] + 
                       results["Humanos Infectados"] + 
                       results["Humanos Recuperados"])
    prevalence = (results["Humanos Infectados"] / total_population * 100)
    
    axes[1, 1].plot(results.index, prevalence, 
                    color='purple', linewidth=2)
    axes[1, 1].fill_between(results.index, 0, prevalence, 
                            alpha=0.3, color='purple')
    axes[1, 1].set_title('Taxa de Prevalência', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Dias')
    axes[1, 1].set_ylabel('Prevalência (%)')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    
    filename = f"results/epidemic_curve_detailed_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✅ Curva epidêmica detalhada salva: {filename}")
    plt.close()

def save_simulation_data(model, timestamp, scale_factor, metadata):
    """Salva dados da simulação em CSV"""
    results = model.datacollector.get_model_vars_dataframe()
    
    # Adicionar coluna de dias
    results['dia'] = results.index
    
    # Escalar para valores reais
    results['casos_ativos_reais'] = results["Humanos Infectados"] * scale_factor
    results['recuperados_reais'] = results["Humanos Recuperados"] * scale_factor
    results['obitos_reais'] = results["Mortes por Dengue"] * scale_factor
    
    # Salvar
    filename = f"results/simulation_data_{timestamp}.csv"
    results.to_csv(filename, index=False)
    print(f"✅ Dados salvos: {filename}")
    
    # Salvar metadados
    metadata_filename = f"results/metadata_{timestamp}.txt"
    with open(metadata_filename, 'w') as f:
        f.write("METADADOS DA SIMULAÇÃO\n")
        f.write("="*50 + "\n\n")
        f.write(f"População real: {metadata['real_population']:,}\n")
        f.write(f"Fator de escala: 1:{metadata['scale_factor']}\n")
        f.write(f"Taxa de ataque: {metadata['attack_rate']:.2f}%\n")
        f.write(f"Taxa de letalidade: {metadata['cfr']:.2f}%\n")
        f.write(f"Pico no dia: {metadata['peak_day']}\n")
        f.write(f"Casos no pico: {metadata['peak_infected'] * scale_factor:,}\n")
        f.write(f"\nTimestamp: {timestamp}\n")
    
    print(f"✅ Metadados salvos: {metadata_filename}")

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    
    print("\n🏙️  Simulando dengue em cidade média brasileira...")
    print("   Baseado em parâmetros epidemiológicos reais\n")
    
    model = run_realistic_city_simulation()
    
    print("\n✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    print("\nArquivos gerados na pasta 'results/':")
    print("  📊 Gráfico principal")
    print("  📈 Curva epidêmica detalhada")
    print("  📄 Dados em CSV")
    print("  📋 Metadados\n")

