# Importando bibliotecas necessárias
import numpy as np
import matplotlib.pyplot as plt

# Definindo os parâmetros
u_h = 0.0000457
u_v = 0.25
b = 1.0
y = 0.167
beta_h = 0.4
beta_v = 0.4
m = 0
N_h = 10_000  # População humana
A = 5_000     # Taxa de nascimento do vetor (mosquitos)
R_0 = 7.7

# Definindo o tempo (40 anos)
time = list(range(1400))  # 0 a 40 anos

# Inicializando as populações
S_h = 100_000    # Humanos suscetíveis
S_v = 2_000      # Vetores suscetíveis
I_h = 0          # Humanos infectados
I_v = 50         # Vetores infectados
R_h = 0          # Humanos recuperados


# Listas para armazenar os resultados de S_h (suscetíveis humanos) e I_h (infectados humanos)
S_h_values = []
I_h_values = []

# Loop para simular a dinâmica ao longo do tempo (em anos)
for i in time:
    # Armazenar os valores atuais
    S_h_values.append(S_h)
    I_h_values.append(I_h)

    # Atualizar as equações com base nos valores anteriores
    new_S_h = u_h * (N_h - S_h) - ((beta_h * b) / (N_h + m)) * S_h * I_v
    new_I_h = ((beta_h * b) / (N_h + m)) * S_h * I_v - (u_h + y) * I_h
    new_R_h = y * I_h - u_h * R_h
    new_S_v = A - ((beta_v * b) / (N_h + m)) * S_v * I_h - u_v * S_v
    new_I_v = ((beta_v * b) / (N_h + m)) * S_v * I_h - u_v * I_v

    # Atualizar as populações
    S_h = S_h + new_S_h
    I_h = I_h + new_I_h
    R_h = R_h + new_R_h
    S_v = S_v + new_S_v
    I_v = I_v + new_I_v


# Plotar o gráfico de S_h (humanos suscetíveis) vs I_h (humanos infectados)
plt.figure(figsize=(8, 6))
plt.plot(I_h_values, S_h_values, label='S_h por I_h', color='blue', marker='o')
plt.xlabel('I_h (Humanos Infectados)')
plt.ylabel('S_h (Humanos Suscetíveis)')
# plt.title('Gráfico de S_h por I_h ao Longo de 80 dias')
plt.legend()
plt.grid(True)
plt.show()

