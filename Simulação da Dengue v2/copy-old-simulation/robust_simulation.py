#!/usr/bin/env python3
"""
Simulações robustas de dengue com parâmetros realistas
"""

from model.model import DengueABM
from visualization.plot_results import plot_model_results, plot_epidemic_curves, plot_comparative_analysis
from analysis.evaluate_model import run_multiple_simulations, plot_results_with_ci
import time
import os
from datetime import datetime

def run_realistic_simulation():
    """Executa uma simulação com parâmetros realistas"""
    print("=== SIMULAÇÃO REALISTA DE DENGUE ===")
    
    # Parâmetros realistas baseados no NetLogo original
    model = DengueABM(
        width=50, 
        height=50,
        initial_humans=1000,
        initial_mosquitoes=5000,
        initial_infected_humans=10,
        initial_infected_mosquitoes=50,
        mosquitoes_eggs=50,
        inherit_dengue_eggs_percentage=5,
        fatality_percentage=1
    )
    
    print(f"Início: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    start_time = time.time()
    
    # Executar por 365 dias (1 ano)
    for i in range(365):
        if not model.running:
            print(f"Simulação parou no dia {i}")
            break
        model.step()
        if i % 30 == 0:  # Relatório mensal
            print(f"Mês {i//30 + 1}: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    end_time = time.time()
    print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")
    print(f"Resultado final: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    # Salvar resultados com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/realistic_simulation_{timestamp}.png"
    plot_model_results(model, filename)
    
    # Salvar curvas epidêmicas detalhadas
    curves_filename = f"results/realistic_curves_{timestamp}.png"
    plot_epidemic_curves(model, curves_filename)
    print(f"Resultados salvos em {filename}")
    
    return model

def run_epidemic_scenario():
    """Executa cenário de epidemia com mais infectados iniciais"""
    print("\n=== CENÁRIO DE EPIDEMIA ===")
    
    model = DengueABM(
        width=50, 
        height=50,
        initial_humans=1000,
        initial_mosquitoes=5000,
        initial_infected_humans=50,  # Mais infectados iniciais
        initial_infected_mosquitoes=200,  # Mais mosquitos infectados
        mosquitoes_eggs=50,
        inherit_dengue_eggs_percentage=5,
        fatality_percentage=1
    )
    
    print(f"Início: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    start_time = time.time()
    
    # Executar por 180 dias (6 meses)
    for i in range(180):
        if not model.running:
            print(f"Simulação parou no dia {i}")
            break
        model.step()
        if i % 15 == 0:  # Relatório quinzenal
            print(f"Semana {i//7 + 1}: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    end_time = time.time()
    print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")
    print(f"Resultado final: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    # Salvar resultados com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/epidemic_scenario_{timestamp}.png"
    plot_model_results(model, filename)
    
    # Salvar curvas epidêmicas detalhadas
    curves_filename = f"results/epidemic_curves_{timestamp}.png"
    plot_epidemic_curves(model, curves_filename)
    print(f"Resultados salvos em {filename}")
    
    return model

def run_control_scenario():
    """Executa cenário de controle com menos mosquitos"""
    print("\n=== CENÁRIO DE CONTROLE (MENOS MOSQUITOS) ===")
    
    model = DengueABM(
        width=50, 
        height=50,
        initial_humans=1000,
        initial_mosquitoes=1000,  # Menos mosquitos
        initial_infected_humans=5,
        initial_infected_mosquitoes=10,
        mosquitoes_eggs=20,  # Menos ovos
        inherit_dengue_eggs_percentage=2,  # Menor herança
        fatality_percentage=0.5  # Menor mortalidade
    )
    
    print(f"Início: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    start_time = time.time()
    
    # Executar por 365 dias
    for i in range(365):
        if not model.running:
            print(f"Simulação parou no dia {i}")
            break
        model.step()
        if i % 30 == 0:  # Relatório mensal
            print(f"Mês {i//30 + 1}: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    end_time = time.time()
    print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")
    print(f"Resultado final: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    # Salvar resultados com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/control_scenario_{timestamp}.png"
    plot_model_results(model, filename)
    
    # Salvar curvas epidêmicas detalhadas
    curves_filename = f"results/control_curves_{timestamp}.png"
    plot_epidemic_curves(model, curves_filename)
    print(f"Resultados salvos em {filename}")
    
    return model

def run_multiple_scenarios_analysis():
    """Executa múltiplas simulações para análise estatística robusta"""
    print("\n=== ANÁLISE ESTATÍSTICA ROBUSTA ===")
    
    # Parâmetros para simulações robustas
    params = {
        "width": 50,
        "height": 50,
        "initial_humans": 1000,
        "initial_mosquitoes": 5000,
        "initial_infected_humans": 10,
        "initial_infected_mosquitoes": 50,
        "mosquitoes_eggs": 50,
        "inherit_dengue_eggs_percentage": 5,
        "fatality_percentage": 1
    }
    
    print("Executando 20 simulações para análise estatística...")
    start_time = time.time()
    
    # Executar 20 simulações (mais robusto que 3)
    results_df = run_multiple_simulations(DengueABM, params, n_simulations=20, steps=365)
    
    end_time = time.time()
    print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")
    
    # Analisar e plotar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Gráfico de infectados
    plot_results_with_ci(results_df, "total_infected", "Número Total de Infectados")
    plt.savefig(f"results/multiple_simulations_infected_{timestamp}.png")
    
    # Gráfico de mortes por dengue
    plot_results_with_ci(results_df, "total_deaths_dengue", "Número de Mortes por Dengue")
    plt.savefig(f"results/multiple_simulations_deaths_{timestamp}.png")
    
    # Salvar resultados em CSV com timestamp
    csv_filename = f"results/multiple_simulations_robust_{timestamp}.csv"
    results_df.to_csv(csv_filename, index=False)
    print(f"Resultados salvos em {csv_filename}")
    
    return results_df

def run_comparative_analysis():
    """Executa análise comparativa entre diferentes cenários"""
    print("\n=== ANÁLISE COMPARATIVA DE CENÁRIOS ===")
    
    scenarios = {
        "Realista": {
            "initial_infected_humans": 10,
            "initial_infected_mosquitoes": 50,
            "mosquitoes_eggs": 50
        },
        "Epidemia": {
            "initial_infected_humans": 50,
            "initial_infected_mosquitoes": 200,
            "mosquitoes_eggs": 50
        },
        "Controle": {
            "initial_infected_humans": 5,
            "initial_infected_mosquitoes": 10,
            "mosquitoes_eggs": 20
        }
    }
    
    results_comparison = []
    
    for scenario_name, params in scenarios.items():
        print(f"\nExecutando cenário: {scenario_name}")
        
        # Parâmetros base
        base_params = {
            "width": 50,
            "height": 50,
            "initial_humans": 1000,
            "initial_mosquitoes": 5000,
            "inherit_dengue_eggs_percentage": 5,
            "fatality_percentage": 1
        }
        base_params.update(params)
        
        # Executar 5 simulações para cada cenário
        results_df = run_multiple_simulations(DengueABM, base_params, n_simulations=5, steps=180)
        results_df['scenario'] = scenario_name
        results_comparison.append(results_df)
    
    # Combinar resultados
    import pandas as pd
    combined_results = pd.concat(results_comparison, ignore_index=True)
    
    # Salvar resultados comparativos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"results/comparative_analysis_{timestamp}.csv"
    combined_results.to_csv(csv_filename, index=False)
    
    # Salvar gráfico comparativo
    plot_filename = f"results/comparative_analysis_{timestamp}.png"
    plot_comparative_analysis(combined_results, plot_filename)
    print(f"Análise comparativa salva em {csv_filename}")
    
    return combined_results

if __name__ == "__main__":
    print("=== SIMULAÇÕES ROBUSTAS DE DENGUE ===")
    print("Iniciando simulações com parâmetros realistas...")
    
    # Criar diretório de resultados se não existir
    os.makedirs("results", exist_ok=True)
    
    # Executar simulações
    realistic_model = run_realistic_simulation()
    epidemic_model = run_epidemic_scenario()
    control_model = run_control_scenario()
    
    # Análise estatística
    robust_results = run_multiple_scenarios_analysis()
    comparative_results = run_comparative_analysis()
    
    print("\n=== TODAS AS SIMULAÇÕES CONCLUÍDAS ===")
    print("Verifique a pasta 'results' para ver todos os gráficos e dados gerados.")
