from model.model import DengueABM
from visualization.plot_results import plot_model_results
from analysis.evaluate_model import run_multiple_simulations, plot_results_with_ci

def run_single_simulation():
    """Executa uma simulação única"""
    print("Executando simulação única...")
    
    # Configurar parâmetros do modelo (teste ultra-rápido)
    model = DengueABM(
        width=10, 
        height=10,
        initial_humans=20,
        initial_mosquitoes=30,
        initial_infected_humans=2,
        initial_infected_mosquitoes=3
    )
    
    # Executar a simulação por 30 dias (teste ultra-rápido)
    for i in range(30):
        if not model.running:
            print(f"Simulação parou no dia {i}")
            break
        model.step()
        if i % 5 == 0:
            print(f"Dia {i}: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    # Plotar resultados
    plot_model_results(model, "results/single_simulation.png")
    print("Simulação única concluída. Resultados salvos em results/single_simulation.png")

def run_multiple_simulations_analysis():
    """Executa múltiplas simulações para análise estatística"""
    print("Executando múltiplas simulações para cálculo do IC 95%...")
    
    # Parâmetros para as simulações (teste ultra-rápido)
    params = {
        "width": 10,
        "height": 10,
        "initial_humans": 20,
        "initial_mosquitoes": 30,
        "initial_infected_humans": 2,
        "initial_infected_mosquitoes": 3
    }
    
    # Executar 3 simulações (teste ultra-rápido)
    results_df = run_multiple_simulations(DengueABM, params, n_simulations=3, steps=30)
    
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