#!/usr/bin/env python3
"""
Versão OTIMIZADA das simulações robustas de dengue
Com coleta de dados menos frequente para análises estatísticas
"""

from model.model import DengueABM
from visualization.plot_results import plot_model_results
from analysis.evaluate_model import run_multiple_simulations
import time
import os
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para salvar gráficos
import matplotlib.pyplot as plt

def run_realistic_simulation_fast():
    """Executa uma simulação com parâmetros realistas - OTIMIZADA"""
    print("=== SIMULAÇÃO REALISTA DE DENGUE (OTIMIZADA) ===")
    
    # Parâmetros balanceados (reduzidos mas ainda realistas)
    model = DengueABM(
        width=40,  # Reduzido de 50
        height=40,
        initial_humans=800,  # Reduzido de 1000
        initial_mosquitoes=3500,  # Reduzido de 5000
        initial_infected_humans=8,
        initial_infected_mosquitoes=40,
        mosquitoes_eggs=40,
        inherit_dengue_eggs_percentage=4,
        fatality_percentage=1
    )
    
    # OTIMIZAÇÃO: Coleta de dados a cada 7 dias (ao invés de todo dia)
    model.data_collection_frequency = 7
    
    print(f"Início: {model.people_count_with_dengue} pessoas infectadas, "
          f"{model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    start_time = time.time()
    
    # Executar por 365 dias (1 ano)
    for i in range(365):
        if not model.running:
            print(f"Simulação parou no dia {i}")
            break
        model.step()
        if i % 60 == 0:  # Relatório a cada 2 meses
            elapsed = time.time() - start_time
            print(f"Dia {i}: {model.people_count_with_dengue} infectados, "
                  f"{model.mosquitoes_count_with_dengue} mosquitos | "
                  f"Tempo: {elapsed:.1f}s")
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n✓ Tempo de execução: {duration:.2f} segundos ({duration/60:.1f} min)")
    print(f"  Resultado final: {model.people_count_with_dengue} pessoas infectadas")
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/realistic_fast_{timestamp}.png"
    try:
        plot_model_results(model, filename)
        print(f"  ✓ Gráfico salvo em {filename}")
    except Exception as e:
        print(f"  ⚠ Erro ao salvar gráfico: {e}")
    
    return model

def run_multiple_scenarios_fast():
    """Executa múltiplas simulações - OTIMIZADA"""
    print("\n=== ANÁLISE ESTATÍSTICA OTIMIZADA ===")
    
    # Parâmetros balanceados
    params = {
        "width": 40,
        "height": 40,
        "initial_humans": 800,
        "initial_mosquitoes": 3500,
        "initial_infected_humans": 8,
        "initial_infected_mosquitoes": 40,
        "mosquitoes_eggs": 40,
        "inherit_dengue_eggs_percentage": 4,
        "fatality_percentage": 1
    }
    
    print("Executando 10 simulações (otimizadas)...")
    print("Cada simulação: 180 dias com coleta de dados a cada 7 dias")
    
    start_time = time.time()
    
    # OTIMIZAÇÃO: Menos simulações mas ainda estatisticamente válidas
    n_sims = 10
    all_results = []
    
    for i in range(n_sims):
        sim_start = time.time()
        print(f"\nSimulação {i+1}/{n_sims}...")
        
        model = DengueABM(**params)
        # OTIMIZAÇÃO: Coleta de dados menos frequente
        model.data_collection_frequency = 7
        
        # Executar 180 dias (6 meses)
        for j in range(180):
            if not model.running:
                break
            model.step()
            
            # Progresso a cada 60 dias
            if j % 60 == 0 and j > 0:
                print(f"  Dia {j}: {model.people_count_with_dengue} infectados")
        
        sim_duration = time.time() - sim_start
        
        # Coletar resultados finais
        result = {
            "simulation": i,
            "total_infected": model.people_count_with_dengue,
            "total_recovered": model.people_count_recovered_from_dengue,
            "total_deaths_common": model.people_count_death_common,
            "total_deaths_dengue": model.people_count_death_dengue,
            "infected_mosquitoes": model.mosquitoes_count_with_dengue,
            "total_mosquitoes": model.mosquitoes_count_total,
            "duration_seconds": sim_duration
        }
        
        all_results.append(result)
        print(f"  ✓ Completada em {sim_duration:.1f}s")
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print(f"✓ TODAS AS SIMULAÇÕES COMPLETADAS!")
    print(f"  Tempo total: {total_duration:.2f}s ({total_duration/60:.1f} min)")
    print(f"  Tempo médio por simulação: {total_duration/n_sims:.1f}s")
    print(f"{'='*60}")
    
    # Salvar resultados
    results_df = pd.DataFrame(all_results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"results/multiple_simulations_fast_{timestamp}.csv"
    results_df.to_csv(csv_filename, index=False)
    
    # Estatísticas resumidas
    print("\n=== ESTATÍSTICAS RESUMIDAS ===")
    print(f"Infectados finais: {results_df['total_infected'].mean():.1f} ± "
          f"{results_df['total_infected'].std():.1f}")
    print(f"Mortes por dengue: {results_df['total_deaths_dengue'].mean():.1f} ± "
          f"{results_df['total_deaths_dengue'].std():.1f}")
    print(f"População de mosquitos: {results_df['total_mosquitoes'].mean():.0f} ± "
          f"{results_df['total_mosquitoes'].std():.0f}")
    print(f"\nResultados salvos em: {csv_filename}")
    
    return results_df

def run_comparative_analysis_fast():
    """Executa análise comparativa entre cenários - OTIMIZADA"""
    print("\n=== ANÁLISE COMPARATIVA (OTIMIZADA) ===")
    
    scenarios = {
        "Realista": {
            "initial_infected_humans": 8,
            "initial_infected_mosquitoes": 40,
            "mosquitoes_eggs": 40
        },
        "Epidemia": {
            "initial_infected_humans": 40,
            "initial_infected_mosquitoes": 160,
            "mosquitoes_eggs": 40
        },
        "Controle": {
            "initial_infected_humans": 4,
            "initial_infected_mosquitoes": 10,
            "mosquitoes_eggs": 20
        }
    }
    
    results_comparison = []
    
    for scenario_name, scenario_params in scenarios.items():
        print(f"\n--- Cenário: {scenario_name} ---")
        
        # Parâmetros base
        base_params = {
            "width": 40,
            "height": 40,
            "initial_humans": 800,
            "initial_mosquitoes": 3500,
            "inherit_dengue_eggs_percentage": 4,
            "fatality_percentage": 1
        }
        base_params.update(scenario_params)
        
        # OTIMIZAÇÃO: 5 simulações por cenário
        for i in range(5):
            print(f"  Simulação {i+1}/5...")
            model = DengueABM(**base_params)
            model.data_collection_frequency = 7
            
            for _ in range(180):  # 6 meses
                if not model.running:
                    break
                model.step()
            
            result = {
                "scenario": scenario_name,
                "simulation": i,
                "total_infected": model.people_count_with_dengue,
                "total_deaths_dengue": model.people_count_death_dengue,
                "total_mosquitoes": model.mosquitoes_count_total
            }
            results_comparison.append(result)
    
    # Salvar resultados
    comparison_df = pd.DataFrame(results_comparison)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"results/comparative_fast_{timestamp}.csv"
    comparison_df.to_csv(csv_filename, index=False)
    
    print(f"\n✓ Análise comparativa salva em: {csv_filename}")
    
    # Resumo por cenário
    print("\n=== RESUMO POR CENÁRIO ===")
    for scenario in scenarios.keys():
        scenario_data = comparison_df[comparison_df['scenario'] == scenario]
        print(f"\n{scenario}:")
        print(f"  Infectados: {scenario_data['total_infected'].mean():.1f} ± "
              f"{scenario_data['total_infected'].std():.1f}")
        print(f"  Mortes: {scenario_data['total_deaths_dengue'].mean():.1f} ± "
              f"{scenario_data['total_deaths_dengue'].std():.1f}")
    
    return comparison_df

if __name__ == "__main__":
    print("="*60)
    print("SIMULAÇÕES OTIMIZADAS DE DENGUE")
    print("="*60)
    print("\nOtimizações aplicadas:")
    print("  ✓ População reduzida em 20-30% (ainda realista)")
    print("  ✓ Coleta de dados a cada 7 dias (ao invés de diária)")
    print("  ✓ Cache de vizinhanças")
    print("  ✓ Iterações otimizadas")
    print("  ✓ Controle de população de mosquitos")
    print("\nTempo esperado:")
    print("  - Simulação única: 1-2 minutos")
    print("  - 10 simulações: 10-20 minutos")
    print("  - Análise comparativa: 5-10 minutos")
    print("  - TOTAL: ~20-30 minutos (ao invés de horas)")
    print("="*60)
    print("\n🚀 Iniciando simulações...\n")
    
    # Criar diretório de resultados
    os.makedirs("results", exist_ok=True)
    
    start_total = time.time()
    
    # Executar análises
    realistic_model = run_realistic_simulation_fast()
    multiple_results = run_multiple_scenarios_fast()
    comparative_results = run_comparative_analysis_fast()
    
    end_total = time.time()
    total_duration = end_total - start_total
    
    print("\n" + "="*60)
    print("✓ TODAS AS ANÁLISES COMPLETADAS!")
    print("="*60)
    print(f"Tempo total: {total_duration:.2f}s ({total_duration/60:.1f} min)")
    print(f"\nVerifique a pasta 'results' para todos os arquivos gerados.")
    print("="*60)

