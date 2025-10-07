from model.model_old import DengueABM
from visualization.plot_results_old import plot_model_results
from analysis.evaluate_model_old import run_multiple_simulations, plot_results_with_ci

def run_single_simulation():
    """Executa uma simulação única"""
    print("Executando simulação única...")
    
    # Configurar parâmetros do modelo
    model = DengueABM(
        width=50, 
        height=50,
        initial_humans=1000,
        initial_mosquitoes=5000,
        initial_infected_humans=10,
        initial_infected_mosquitoes=50
    )
    
    # Executar a simulação por 365 dias (1 ano)
    for i in range(365):
        model.step()
        if i % 50 == 0:
            print(f"Dia {i}: {model.people_count_with_dengue} pessoas infectadas")
    
    # Plotar resultados
    plot_model_results(model, "results/single_simulation.png")
    print("Simulação única concluída. Resultados salvos em results/single_simulation.png")

def run_multiple_simulations_analysis():
    """Executa múltiplas simulações para análise estatística"""
    print("Executando múltiplas simulações para cálculo do IC 95%...")
    
    # Parâmetros para as simulações
    params = {
        "width": 50,
        "height": 50,
        "initial_humans": 1000,
        "initial_mosquitoes": 5000,
        "initial_infected_humans": 10,
        "initial_infected_mosquitoes": 50
    }
    
    # Executar 30 simulações (pode aumentar para mais precisão)
    results_df = run_multiple_simulations(DengueABM, params, n_simulations=30, steps=365)
    
    # Analisar e plotar resultados
    plot_results_with_ci(results_df, "total_infected", "Número Total de Infectados")
    
    # Salvar resultados em CSV
    results_df.to_csv("results/multiple_simulations.csv", index=False)
    print("Resultados das múltiplas simulações salvos em results/multiple_simulations.csv")

if __name__ == "__main__":
    print("=== Simulação de Propagação de Dengue usando ABM ===")
    
    # Executar simulação única
    run_single_simulation()
    
    # Executar múltiplas simulações para análise
    run_multiple_simulations_analysis()
    
    print("Simulação concluída!")