import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_model_results(model, filename=None):
    """
    Plota os resultados de uma execução do modelo
    
    Args:
        model: instância do modelo após execução
        filename: nome do arquivo para salvar o gráfico (opcional)
    """
    results = model.datacollector.get_model_vars_dataframe()
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # População humana
    axes[0, 0].plot(results.index, results["Humanos Saudáveis"], label="Saudáveis")
    axes[0, 0].plot(results.index, results["Humanos Infectados"], label="Infectados")
    axes[0, 0].plot(results.index, results["Humanos Recuperados"], label="Recuperados")
    axes[0, 0].set_title("População Humana")
    axes[0, 0].set_xlabel("Dias")
    axes[0, 0].set_ylabel("Número de Indivíduos")
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # População de mosquitos
    axes[0, 1].plot(results.index, results["Mosquitos Saudáveis"], label="Saudáveis")
    axes[0, 1].plot(results.index, results["Mosquitos Infectados"], label="Infectados")
    axes[0, 1].set_title("População de Mosquitos")
    axes[0, 1].set_xlabel("Dias")
    axes[0, 1].set_ylabel("Número de Mosquitos")
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Mortes
    axes[1, 0].plot(results.index, results["Mortes Comuns"], label="Mortes Comuns")
    axes[1, 0].plot(results.index, results["Mortes por Dengue"], label="Mortes por Dengue")
    axes[1, 0].set_title("Mortes")
    axes[1, 0].set_xlabel("Dias")
    axes[1, 0].set_ylabel("Número de Mortes")
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Proporção de infectados
    total_humans = results["Humanos Saudáveis"] + results["Humanos Infectados"] + results["Humanos Recuperados"]
    infection_rate = results["Humanos Infectados"] / total_humans * 100
    axes[1, 1].plot(results.index, infection_rate, label="Taxa de Infecção", color="red")
    axes[1, 1].set_title("Taxa de Infecção na População Humana")
    axes[1, 1].set_xlabel("Dias")
    axes[1, 1].set_ylabel("Percentual de Infectados (%)")
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename)
    
    plt.show()

def plot_multiple_runs(results_df, variable="total_infected", title="Número de Infectados"):
    """
    Plota resultados de múltiplas execuções com intervalo de confiança
    
    Args:
        results_df: DataFrame com resultados de múltiplas simulações
        variable: variável a ser plotada
        title: título do gráfico
    """
    mean = results_df[variable].mean()
    std = results_df[variable].std()
    ci_lower = mean - 1.96 * std / np.sqrt(len(results_df))
    ci_upper = mean + 1.96 * std / np.sqrt(len(results_df))
    
    plt.figure(figsize=(10, 6))
    plt.hist(results_df[variable], bins=15, alpha=0.7, edgecolor='black')
    plt.axvline(ci_lower, color='red', linestyle='--', label='IC 95% inferior')
    plt.axvline(ci_upper, color='red', linestyle='--', label='IC 95% superior')
    plt.axvline(mean, color='green', linewidth=2, label='Média')
    plt.xlabel(title)
    plt.ylabel('Frequência')
    plt.legend()
    plt.title(f'Distribuição de {title} com IC 95% (Múltiplas Simulações)')
    plt.show()
    
    print(f"Média: {mean:.1f}")
    print(f"Desvio Padrão: {std:.1f}")
    print(f"IC 95%: [{ci_lower:.1f}, {ci_upper:.1f}]")