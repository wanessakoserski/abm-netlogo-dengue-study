import sympy as sp

# Definir as variáveis simbólicas
u_h, N, S, B_h, m, I = sp.symbols('u_h N S B_h m I')

# Definir a equação dS/dt
dS_dt = u_h * (N - S) - (B_h / (N + m)) * S * I

# Exibir a equação simbólica
print("Equação dS/dt:")
sp.pprint(dS_dt)

# Substituir os valores numéricos
valores = {u_h: 0.5, N: 1000, S: 500, B_h: 0.1, m: 2, I: 200}

# Avaliar a equação com os valores fornecidos
resultado = dS_dt.subs(valores)

print(f"\nResultado com base nos valores fornecidos: {resultado}")