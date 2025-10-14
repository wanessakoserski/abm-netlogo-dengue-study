#!/usr/bin/env python3
"""
Teste ultra-rápido da simulação de dengue
"""

from model.model import DengueABM
import time

def test_quick_simulation():
    """Teste ultra-rápido sem reprodução"""
    print("=== TESTE ULTRA-RÁPIDO DA SIMULAÇÃO DE DENGUE ===")
    
    # Parâmetros mínimos
    model = DengueABM(
        width=5, 
        height=5,
        initial_humans=10,
        initial_mosquitoes=15,
        initial_infected_humans=1,
        initial_infected_mosquitoes=2
    )
    
    print(f"Início: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    
    start_time = time.time()
    
    # Executar apenas 10 passos
    for i in range(10):
        model.step()
        print(f"Passo {i+1}: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
        
        # Parar se não há mais agentes
        if model.people_count_total == 0 or model.mosquitoes_count_total == 0:
            print("Simulação parou: sem agentes")
            break
    
    end_time = time.time()
    print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")
    print(f"Resultado final: {model.people_count_with_dengue} pessoas infectadas, {model.mosquitoes_count_with_dengue} mosquitos infectados")
    print("Teste concluído!")

if __name__ == "__main__":
    test_quick_simulation()
