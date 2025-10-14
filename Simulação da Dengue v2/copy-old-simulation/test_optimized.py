#!/usr/bin/env python3
"""
Script de teste rápido para verificar otimizações
"""

from model.model import DengueABM
from visualization.plot_results import plot_model_results
import time

def test_optimized_simulation():
    """Testa simulação com parâmetros otimizados"""
    print("=== TESTE DE OTIMIZAÇÃO ===")
    print("Este teste deve completar em 30-60 segundos.\n")
    
    # Parâmetros balanceados (não muito pequenos, não muito grandes)
    model = DengueABM(
        width=30,  # Reduzido de 50
        height=30,  # Reduzido de 50
        initial_humans=500,  # Reduzido de 1000
        initial_mosquitoes=2000,  # Reduzido de 5000
        initial_infected_humans=5,  # Reduzido de 10
        initial_infected_mosquitoes=25,  # Reduzido de 50
        mosquitoes_eggs=30,  # Reduzido de 50
        inherit_dengue_eggs_percentage=3,  # Reduzido de 5
        fatality_percentage=1
    )
    
    print(f"Início: {model.people_count_with_dengue} pessoas infectadas, "
          f"{model.mosquitoes_count_with_dengue} mosquitos infectados\n")
    
    start_time = time.time()
    
    # Executar por 180 dias (6 meses)
    steps = 180
    for i in range(steps):
        if not model.running:
            print(f"Simulação parou no dia {i}")
            break
        model.step()
        
        if i % 30 == 0:  # Relatório mensal
            elapsed = time.time() - start_time
            remaining = (elapsed / (i + 1)) * (steps - i - 1) if i > 0 else 0
            print(f"Mês {i//30 + 1}: {model.people_count_with_dengue} pessoas infectadas, "
                  f"{model.mosquitoes_count_with_dengue} mosquitos infectados "
                  f"| Tempo: {elapsed:.1f}s | Restante: ~{remaining:.1f}s")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n✓ Simulação completada!")
    print(f"  Tempo total: {duration:.2f} segundos")
    print(f"  Velocidade: {steps/duration:.1f} dias/segundo")
    print(f"  Resultado: {model.people_count_with_dengue} pessoas infectadas, "
          f"{model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    # Salvar resultado
    plot_model_results(model, "results/test_optimized.png")
    print(f"\n✓ Gráfico salvo em results/test_optimized.png")
    
    # Análise de performance
    print("\n=== ANÁLISE DE PERFORMANCE ===")
    if duration < 60:
        print("✓ EXCELENTE! Simulação muito rápida.")
    elif duration < 120:
        print("✓ BOM! Simulação em tempo aceitável.")
    elif duration < 300:
        print("⚠ MODERADO. Simulação um pouco lenta, mas aceitável.")
    else:
        print("✗ LENTO! Ainda há problemas de performance.")
    
    return model, duration

def estimate_total_time():
    """Estima tempo para simulações completas"""
    print("\n=== ESTIMATIVA DE TEMPO PARA ROBUST_SIMULATION.PY ===")
    
    # Fazer uma simulação de teste pequena
    print("Executando simulação de teste pequena...")
    test_model = DengueABM(
        width=30, height=30,
        initial_humans=500, initial_mosquitoes=2000,
        initial_infected_humans=5, initial_infected_mosquitoes=25
    )
    
    start = time.time()
    for _ in range(10):  # 10 dias
        test_model.step()
    test_duration = time.time() - start
    
    time_per_day = test_duration / 10
    
    print(f"Tempo por dia: {time_per_day:.3f} segundos\n")
    
    # Estimativas para robust_simulation.py
    scenarios = {
        "Simulação Realista (365 dias)": 365,
        "Cenário Epidemia (180 dias)": 180,
        "Cenário Controle (365 dias)": 365,
        "Análise Robusta (20 × 365 dias)": 20 * 365,
        "Análise Comparativa (3 × 5 × 180 dias)": 3 * 5 * 180
    }
    
    total_estimated = 0
    for name, days in scenarios.items():
        estimated = days * time_per_day
        total_estimated += estimated
        print(f"{name:45} ~{estimated/60:.1f} minutos")
    
    print(f"\n{'TOTAL ESTIMADO':45} ~{total_estimated/60:.1f} minutos (~{total_estimated/3600:.1f} horas)")
    print("\nNOTA: Estas são estimativas. O tempo real pode variar devido a:")
    print("  - Reprodução de mosquitos aumentando a população")
    print("  - Variabilidade aleatória")
    print("  - Carga do sistema")

if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)
    
    # Teste rápido
    model, duration = test_optimized_simulation()
    
    # Estimativa de tempo
    estimate_total_time()
    
    print("\n" + "="*60)
    print("RECOMENDAÇÕES:")
    print("="*60)
    if duration < 60:
        print("✓ As otimizações estão funcionando bem!")
        print("✓ Você pode executar robust_simulation.py")
        print("  (Tempo estimado: veja acima)")
    else:
        print("⚠ Simulação ainda lenta.")
        print("  Considere reduzir os parâmetros em robust_simulation.py:")
        print("  - initial_humans: 500 (ao invés de 1000)")
        print("  - initial_mosquitoes: 2000 (ao invés de 5000)")
        print("  - n_simulations: 10 (ao invés de 20)")

