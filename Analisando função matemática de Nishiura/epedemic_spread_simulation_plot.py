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
N = 100_000
N_h = 10_000
N_v = 10_000
A = 5_000
R_0 = 7.7

# Definindo o tempo
time = list(range(40))

# Inicializando as populações
S_h = 100_000
S_v = 2_000
I_h = 0
I_v = 6_000
R_h = 0

# Listas para armazenar os resultados
S_h_values = []
I_h_values = []
R_h_values = []
S_v_values = []
I_v_values = []

# Loop para simular a dinâmica ao longo do tempo
for i in time:
    # Armazenar os valores atuais
    S_h_values.append(S_h)
    I_h_values.append(I_h)
    R_h_values.append(R_h)
    S_v_values.append(S_v)
    I_v_values.append(I_v)

    # Atualizar as equações com base nos valores anteriores
    new_S_h = u_h * (N_h - S_h) - ((beta_h * b) / (N_h + m)) * S_h * I_v
    new_I_h = ((beta_h * b) / (N_h + m)) * S_h * I_v - (u_h + y) * I_h
    new_R_h = y * I_h - u_h * R_h
    new_S_v = A - ((beta_v * b) / (N_v + m)) * S_v * I_h - u_v * S_v
    new_I_v = ((beta_v * b) / (N_v + m)) * S_v * I_h - u_v * I_v

    # Atualizar as populações
    S_h = S_h + new_S_h
    I_h = I_h + new_I_h
    R_h = R_h + new_R_h
    S_v = S_v + new_S_v
    I_v = I_v + new_I_v



# Plotar os resultados
plt.figure(figsize=(12, 8))
plt.plot(time, S_h_values, label='S_h (Humanos Suscetíveis)')
plt.plot(time, I_h_values, label='I_h (Humanos Infectados)')
plt.plot(time, R_h_values, label='R_h (Humanos Recuperados)')
plt.plot(time, S_v_values, label='S_v (Vetor Suscetíveis)')
plt.plot(time, I_v_values, label='I_v (Vetor Infectados)')
plt.xlabel('Tempo (dias)')
plt.ylabel('População')
plt.title('Dinâmica Populacional de Humanos e Vetores')
plt.legend()
plt.grid(True)
plt.show()

plt.plot(time, I_h_values, label='I_h (Humanos Infectados)', color='red', marker='o')
plt.xlabel('Tempo (dias)')
plt.ylabel('População de Humanos Infectados')
plt.title('Dinâmica de Humanos Infectados (I_h) ao Longo do Tempo')
plt.legend()
plt.grid(True)
plt.show()