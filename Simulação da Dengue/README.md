# Dengue Transmission Agent-Based Model

An **Agent-Based Model (ABM)** built in NetLogo to simulate the complex dynamics of dengue fever transmission between human and mosquito populations. This model explores the effects of seasonality, viral incubation, and cross-species infection on the spread of the disease.

## 🧪 Overview

This project implements a stochastic simulation where autonomous agents (``people`` and ``mosquitoes``) interact in a virtual environment. Their interactions—specifically, mosquito bites—drive the transmission of dengue virus. The model tracks the life cycle, health status, and movement of each individual agent to provide a bottom-up perspective on epidemic emergence.

## 📁 Model Components

### Agent Types & Properties

1.  **`people`**
    *   **Attributes:** `age`, `age-death`, `dengue?`, `transmitter?`, `days-dengue-incubation`, `days-dengue-viral`, `dengue-recurrence`.
    *   **Behavior:** Age, move randomly, reproduce to maintain a stable population, can get infected, recover, or die from dengue or natural causes.

2.  **`mosquitoes`**
    *   **Attributes:** `age`, `age-death`, `dengue?`, `transmitter?`, `days-dengue-incubation`.
    *   **Behavior:** Age, move randomly, reproduce seasonally (with higher rates in warm/wet seasons), bite people to transmit or acquire the virus.

### Key Global Variables & Parameters

The model is highly configurable through global variables (which would typically be controlled by sliders in the NetLogo interface):

*   **Population Control:** `variable-initial-number-people`, `variable-initial-number-mosquitoes`
*   **Initial Outbreak:** `variable-initial-number-cases-dengue-people`, `variable-initial-number-cases-dengue-mosquitoes`
*   **Mosquito Biology:** `variable-number-eggs-mosquitoes`, `variable-inherit-dengue-eggs-mosquitoes`
*   **Disease Severity:** `variable-fatality-percentage-of-people`

### Core Procedures

*   **`button-setup`:** Initializes the world, creates agents, and sets their initial state.
*   **`button-go`:** The main simulation loop executed each tick (representing a day). It handles agent movement, disease progression, aging, reproduction, and biting events.
*   **`mosquitoes-biting`:** The critical procedure where virus transmission occurs between agents that are on the same patch.
*   **`seasonal-reproduction-factor`:** A function that modulates mosquito breeding based on the time of year, simulating seasonal effects.

## 🚀 How to Run the Simulation

1.  **Open in NetLogo:** Load the `.nlogo` file into [NetLogo](https://ccl.northwestern.edu/netlogo/).
2.  **Configure Parameters:** Adjust the sliders on the interface tab to set your desired initial conditions (e.g., population sizes, initial infections, fatality rate).
3.  **Initialize:** Click the `button-setup` button to create the world and agents.
4.  **Run:** Click the `button-go` button to start the simulation. Observe the visual representation and the plots as the dynamics unfold.

## 📊 Outputs and Analysis

The model provides insights into:
*   **Epidemic Curves:** The rise and fall of infected individuals over time.
*   **Endemicity:** Whether the disease persists in the population long-term.
*   **Impact of Interventions:** By changing parameters, you can simulate the effect of control measures like insecticide spraying (reducing mosquitoes) or vaccination (reducing susceptibility).
*   **Seasonal Patterns:** How mosquito breeding seasons lead to peaks in dengue cases.

---

**Note:** This is the code for a NetLogo model. To run it, you need the complete `.nlogo` file which includes the code, interface with buttons/sliders/plots, and information tabs. The code represents the core logic found in the "Code" tab.