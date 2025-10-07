from mesa import Model
try:
    from mesa.time import RandomActivation
    from mesa.space import MultiGrid
    from mesa.datacollection import DataCollector
except ImportError:
    # Para versões mais recentes do Mesa
    from mesa import time, space, datacollection
    RandomActivation = time.RandomActivation
    MultiGrid = space.MultiGrid
    DataCollector = datacollection.DataCollector
import random
import numpy as np


from agents_old import HumanAgent, MosquitoAgent

class DengueABM(Model):
    def __init__(self, width=50, height=50, 
                 initial_humans=1000, initial_mosquitoes=5000,
                 initial_infected_humans=10, initial_infected_mosquitoes=50,
                 transmission_prob_mosquito_to_human=0.3,
                 transmission_prob_human_to_mosquito=0.4,
                 recovery_time=14,
                 people_dengue_fatality_percentage=0.01,
                 mosquitoes_eggs=50,
                 mosquitoes_dengue_inherit_eggs_percentage=0.05):
        
        super().__init__()
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        # Parâmetros de transmissão
        self.transmission_prob_mosquito_to_human = transmission_prob_mosquito_to_human
        self.transmission_prob_human_to_mosquito = transmission_prob_human_to_mosquito
        self.recovery_time = recovery_time
        self.people_dengue_fatality_percentage = people_dengue_fatality_percentage
        self.mosquitoes_eggs = mosquitoes_eggs
        self.mosquitoes_dengue_inherit_eggs_percentage = mosquitoes_dengue_inherit_eggs_percentage
        
        # Parâmetros fixos baseados no NetLogo
        self.mosquitoes_lifespan = 30
        self.people_lifespan = 72 * 365
        
        self.mosquitoes_dengue_average_incubation_days = 10
        self.mosquitoes_dengue_interval_incubation_days = 2
        
        self.people_dengue_average_incubation_days = 6
        self.people_dengue_interval_incubation_days = 2
        self.people_dengue_average_viral_days = 8
        self.people_dengue_interval_viral_days = 4
        
        # Contadores
        self.people_count_total = initial_humans
        self.people_count_with_dengue = initial_infected_humans
        self.people_count_recovered = 0
        self.people_count_death_common = 0
        self.people_count_death_dengue = 0
        
        self.mosquitoes_count_total = initial_mosquitoes
        self.mosquitoes_count_with_dengue = initial_infected_mosquitoes
        
        # Criar agentes
        self.create_agents(initial_humans, initial_mosquitoes, 
                          initial_infected_humans, initial_infected_mosquitoes)
        
        # Coletor de dados
        self.datacollector = DataCollector(
            {
                "Humanos Saudáveis": lambda m: self.count_humans_by_state(m, "S"),
                "Humanos Infectados": lambda m: self.count_humans_by_state(m, "I"),
                "Humanos Recuperados": lambda m: self.count_humans_by_state(m, "R"),
                "Mosquitos Saudáveis": lambda m: self.count_mosquitoes_by_state(m, "S"),
                "Mosquitos Infectados": lambda m: self.count_mosquitoes_by_state(m, "I"),
                "Mortes Comuns": lambda m: m.people_count_death_common,
                "Mortes por Dengue": lambda m: m.people_count_death_dengue,
            }
        )

    def create_agents(self, num_humans, num_mosquitoes, num_infected_humans, num_infected_mosquitoes):
        # Criar humanos
        for i in range(num_humans):
            initial_dengue = i < num_infected_humans
            human = HumanAgent(i, self, initial_dengue=initial_dengue)
            self.schedule.add(human)
            
            # Posicionar na grade
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(human, (x, y))
        
        # Criar mosquitos
        for i in range(num_humans, num_humans + num_mosquitoes):
            initial_dengue = (i - num_humans) < num_infected_mosquitoes
            mosquito = MosquitoAgent(i, self, initial_dengue=initial_dengue)
            self.schedule.add(mosquito)
            
            # Posicionar na grade
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(mosquito, (x, y))

    def seasonal_reproduction_factor(self):
        """Fator sazonal de reprodução baseado no dia do ano"""
        day_of_year = self.schedule.time % 365
        reproduction_factor = np.sin(2 * np.pi * (day_of_year / 365)) * 0.5 + 0.5
        return reproduction_factor

    def reproduce_mosquitoes(self):
        """Reprodução de mosquitos com influência sazonal"""
        reproduction_factor = self.seasonal_reproduction_factor()
        new_mosquitoes = 0
        
        # Cada mosquito tem chance de reproduzir
        for agent in self.schedule.agents:
            if isinstance(agent, MosquitoAgent):
                if agent.age > 5 and agent.age < agent.age_death:
                    if random.random() < 0.1:  # 10% de chance de reproduzir
                        new_mosquitoes += int(reproduction_factor * self.mosquitoes_eggs)
        
        # Criar novos mosquitos
        if new_mosquitoes > 0:
            current_id = self.people_count_total + self.mosquitoes_count_total
            for i in range(current_id, current_id + new_mosquitoes):
                # Herdar dengue com certa probabilidade
                inherit_dengue = random.random() < self.mosquitoes_dengue_inherit_eggs_percentage
                mosquito = MosquitoAgent(i, self, age=0, initial_dengue=inherit_dengue)
                self.schedule.add(mosquito)
                
                # Posicionar na grade
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(mosquito, (x, y))
                
                self.mosquitoes_count_total += 1
                if inherit_dengue:
                    self.mosquitoes_count_with_dengue += 1

    def reproduce_humans(self):
        """Reposição da população humana para manter tamanho constante"""
        if self.people_count_total < 1000:  # Manter população constante
            difference = 1000 - self.people_count_total
            current_id = self.people_count_total + self.mosquitoes_count_total
            
            for i in range(current_id, current_id + difference):
                human = HumanAgent(i, self, age=0)
                self.schedule.add(human)
                
                # Posicionar na grade
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(human, (x, y))
                
                self.people_count_total += 1

    def step(self):
        """Avance o modelo por um passo."""
        self.schedule.step()
        self.reproduce_mosquitoes()
        self.reproduce_humans()
        self.datacollector.collect(self)
        
        # Atualizar contadores
        self.update_counts()

    def update_counts(self):
        """Atualiza os contadores de população"""
        people_infected = 0
        people_recovered = 0
        mosquitoes_infected = 0
        
        for agent in self.schedule.agents:
            if isinstance(agent, HumanAgent):
                if agent.state == "I":
                    people_infected += 1
                elif agent.state == "R":
                    people_recovered += 1
            elif isinstance(agent, MosquitoAgent):
                if agent.state == "I":
                    mosquitoes_infected += 1
        
        self.people_count_with_dengue = people_infected
        self.people_count_recovered = people_recovered
        self.mosquitoes_count_with_dengue = mosquitoes_infected
        self.mosquitoes_count_total = sum(1 for agent in self.schedule.agents if isinstance(agent, MosquitoAgent))
        self.people_count_total = sum(1 for agent in self.schedule.agents if isinstance(agent, HumanAgent))

    @staticmethod
    def count_humans_by_state(model, state):
        return sum(1 for agent in model.schedule.agents 
                  if isinstance(agent, HumanAgent) and agent.state == state)

    @staticmethod
    def count_mosquitoes_by_state(model, state):
        return sum(1 for agent in model.schedule.agents 
                  if isinstance(agent, MosquitoAgent) and agent.state == state)