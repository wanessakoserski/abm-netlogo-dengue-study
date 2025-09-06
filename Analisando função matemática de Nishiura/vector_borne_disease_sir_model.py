from re import S
u_h = 0.0000457
u_v = 0.25
b = 1.0
y = 0.167
beta_h = 0.4
beta_v = 0.4
m = 0
N = 10_000
A = 5_000
R_0 = 7.7

time = list(range(40)) # 0 a 40
population = list()

S_h = 100_000
S_v = 2_000
I_h = 0
I_v = 50
R_h = 0

for i in time:
  S_h = u_h * (N - S_h) - ((beta_h * b) / (N + m)) * S_h * I_v
  I_h = ((beta_h * b) / (N + m)) * S_h * I_v - (u_h + y) * I_h
  R_h = y * I_h - u_h * R_h
  S_v = A - ((beta_v * b) / (N + m)) * S_v * I_h - u_v * S_v
  I_h = ((beta_v * b) / (N + m)) * S_v * I_h - u_v * I_v

  population.append(I_h)

print(population)