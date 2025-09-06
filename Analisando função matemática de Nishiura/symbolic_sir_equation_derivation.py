import sympy as sp

# Definir as variáveis simbólicas
t, u_h, N, S, B_h, m, I = sp.symbols('t u_h N S B_h m I')

# Definir a equação dS/dt
dS_dt = u_h * (N - S) - (B_h / (N + m)) * S * I

# Exibir a equação
print("Equação dS/dt:")
sp.pprint(dS_dt)

# Se você precisar calcular a derivada da equação dS/dt em relação ao tempo (t)
# e S depende de t, você pode derivar em relação a t

# Primeiro, assumimos que S é uma função de t
S = sp.Function('S')(t)

# Definir a nova equação
dS_dt_time_dep = u_h * (N - S) - (B_h / (N + m)) * S * I

# Derivar dS/dt em relação a t
derivada = sp.diff(dS_dt_time_dep, t)

print("\nDerivada da equação em relação ao tempo (t):")
sp.pprint(derivada)