
# Epidemiological Modeling Suite

A collection of Python scripts for modeling, analyzing, and simulating the dynamics of vector-borne diseases using compartmental SIR models. This repository provides tools for both symbolic derivation of model equations and numerical simulation of outbreak scenarios.

## 📁 Project Structure

```
.
├── vector_borne_disease_sir_model.py  # Core numerical simulation
├── symbolic_sir_equation_derivation.py # Symbolic equation analysis
├── evaluate_dSdt_equation.py          # Equation evaluation
├── epidemic_spread_simulation_plot.py # Time-series visualization
├── disease_trajectory_phase_plot.py   # Phase portrait analysis
└── README.md
```

## 🧰 Requirements

This project requires the following Python libraries:
- `sympy` (for symbolic mathematics)
- `numpy` (for numerical operations)
- `matplotlib` (for plotting and visualization)

Install the dependencies with:
```bash
pip install sympy numpy matplotlib
```

## 📊 Scripts Overview

### 1. Core Simulation: `vector_borne_disease_sir_model.py`
**Purpose**: Implements the core logic of a Susceptible-Infected-Recovered (SIR) model for a vector-borne disease (e.g., malaria, dengue).
**Key Features**:
- Defines a system of difference equations for human and vector populations.
- Tracks the compartments `S_h` (Susceptible humans), `I_h` (Infected humans), `R_h` (Recovered humans), `S_v` (Susceptible vectors), `I_v` (Infected vectors).
- Performs a numerical simulation over a specified time range using a simple Euler integration method.
- Outputs a list of infected human counts over time.

**Usage**: Run the script to simulate an outbreak and obtain the population data. The output is a list (`population`) containing the number of infected humans at each time step.

### 2. Symbolic Analysis: `symbolic_sir_equation_derivation.py`
**Purpose**: Performs symbolic manipulation and derivation of the model's differential equations.
**Key Features**:
- Uses `sympy` to define the equation for `dS/dt` (the rate of change of the susceptible population) symbolically.
- Treats variables like `S` as functions of time `S(t)` to correctly compute derivatives.
- Calculates and prints the second derivative `d²S/dt²` for deeper analytical insight.
- Outputs the equations in a human-readable, pretty-printed format.

**Usage**: Run the script to see the formal mathematical structure of the model's equations and their derivatives. This is essential for theoretical analysis.

### 3. Numerical Evaluation: `evaluate_dSdt_equation.py`
**Purpose**: Evaluates the symbolic `dS/dt` equation with specific numerical parameters.
**Key Features**:
- Defines the same symbolic equation as the previous script.
- Substitutes a dictionary of real-world parameter values into the equation.
- Computes the instantaneous numerical value of `dS/dt`, indicating whether the susceptible population is increasing or decreasing at a specific point in time.

**Usage**: Modify the `valores` dictionary to test how different parameter values (e.g., transmission rate, number of infected) affect the rate of infection. The output is a single number representing the value of `dS/dt`.

### 4. Time-Series Visualization: `epidemic_spread_simulation_plot.py`
**Purpose**: Simulates the full model and creates a multi-line plot showing the evolution of all population compartments over time.
**Key Features**:
- Runs a complete simulation, storing the history of all compartments (`S_h`, `I_h`, `R_h`, `S_v`, `I_v`).
- Generates a comprehensive plot visualizing the dynamics of the outbreak.
- The plot shows classic epidemic curves, equilibrium points, and the interaction between human and vector populations.

**Usage**: Run the script to generate a visual summary of the entire epidemic. The plot is saved and displayed using `matplotlib`.

### 5. Phase-Space Analysis: `disease_trajectory_phase_plot.py`
**Purpose**: Simulates the model over a very long time scale (e.g., 40 years) and produces a phase portrait.
**Key Features**:
- Plots the trajectory of the system in the phase space of Susceptible humans (`S_h`) vs. Infected humans (`I_h`).
- This analysis reveals long-term behaviors like stable equilibria, cycles, or damped oscillations that are not obvious in time-series plots.
- Essential for understanding the endemic state of a disease.

**Usage**: Run the script to generate a phase portrait. The resulting plot helps identify fixed points and the long-term fate of the disease dynamics (elimination or endemicity).

## 🚀 How to Use This Repository

1.  **Start with the Theory**: Begin by running `symbolic_sir_equation_derivation.py` to understand the model's mathematical foundation.
2.  **Test Parameters**: Use `evaluate_dSdt_equation.py` to see how changing specific parameters affects the instantaneous rate of spread.
3.  **Run a Simulation**: Execute `vector_borne_disease_sir_model.py` to get raw numerical data from a short-term outbreak simulation.
4.  **Visualize the Outbreak**: Run `epidemic_spread_simulation_plot.py` to see a full time-series visualization of the outbreak.
5.  **Analyze Long-Term Behavior**: Finally, run `disease_trajectory_phase_plot.py` to study the system's behavior over decades and identify its stable state.
