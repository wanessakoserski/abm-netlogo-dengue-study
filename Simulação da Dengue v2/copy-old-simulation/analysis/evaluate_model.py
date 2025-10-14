# analysis/evaluate_model.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_confidence_interval(results, confidence=0.95):
    """
    Calcula o intervalo de confiança para os resultados das simulações
    
    Args:
        results: array-like com os resultados das simulações
        confidence: nível de confiança (padrão: 0.95 para 95%)
    
    Returns:
        tuple: (média, limite inferior, limite superior)
    """
    results = np.array(results)
    mean = np.mean(results)
    std_err = np.std(results, ddof=1) / np.sqrt(len(results))
    h = std_err * abs(np.percentile(np.random.standard_normal(10000), 
                                   [(1-confidence)/2*100, (1+confidence)/2*100])[1])
    
    return mean, mean - h, mean + h

def run_multiple_simulations(model_class, params, n_simulations=100, steps=365):
    """
    Executa múltiplas simulações e coleta resultados
    
    Args:
        model_class: classe do modelo a ser simulado
        params: dicionário com parâmetros do modelo
        n_simulations: número de simulações a executar
        steps: número de passos por simulação
    
    Returns:
        DataFrame com resultados de todas as simulações
    """
    all_results = []
    
    for i in range(n_simulations):
        print(f"Executando simulação {i+1}/{n_simulations}")
        model = model_class(**params)
        
        for j in range(steps):
            model.step()
        
        # Coletar resultados finais
        final_data = {
            "simulation": i,
            "total_infected": model.people_count_with_dengue,
            "total_recovered": model.people_count_recovered_from_dengue,
            "total_deaths_common": model.people_count_death_common,
            "total_deaths_dengue": model.people_count_death_dengue,
            "infected_mosquitoes": model.mosquitoes_count_with_dengue,
            "total_mosquitoes": model.mosquitoes_count_total
        }
        
        all_results.append(final_data)
    
    return pd.DataFrame(all_results)

def plot_results_with_ci(results_df, variable="total_infected", title="Número de Infectados"):
    """
    Plota resultados com intervalo de confiança
    
    Args:
        results_df: DataFrame com resultados das simulações
        variable: nome da variável a plotar
        title: título do gráfico
    """
    data = results_df[variable].values
    mean, ci_lower, ci_upper = calculate_confidence_interval(data)
    
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=15, alpha=0.7, edgecolor='black')
    plt.axvline(ci_lower, color='red', linestyle='--', label='IC 95% inferior')
    plt.axvline(ci_upper, color='red', linestyle='--', label='IC 95% superior')
    plt.axvline(mean, color='green', linewidth=2, label='Média')
    plt.xlabel(title)
    plt.ylabel('Frequência')
    plt.legend()
    plt.title(f'Distribuição de {title} com IC 95%')
    plt.show()
    
    print(f"Média: {mean:.1f}")
    print(f"IC 95%: [{ci_lower:.1f}, {ci_upper:.1f}]")