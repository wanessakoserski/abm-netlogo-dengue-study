from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.agent import AgentSet
import random
import math
import numpy as np

from .agents import HumanAgent, MosquitoAgent

class DengueABM(Model):
    def __init__(self, width=50, height=50, 
                 initial_humans=1000, initial_mosquitoes=5000,
                 initial_infected_humans=10, initial_infected_mosquitoes=50,
                 mosquitoes_eggs=50,
                 inherit_dengue_eggs_percentage=5,
                 fatality_percentage=1):
        
        super().__init__()
        self.grid = MultiGrid(width, height, torus=True)
        self.running = True
        
        # Parâmetros do modelo (como no NetLogo)
        self.width = width
        self.height = height
        
        # Parâmetros dos mosquitos (como no NetLogo)
        self.mosquitoes_lifespan = 30
        self.mosquitoes_eggs = mosquitoes_eggs
        self.mosquitoes_dengue_average_incubation_days = 10
        self.mosquitoes_dengue_interval_incubation_days = 2
        self.mosquitoes_dengue_inherit_eggs_percentage = inherit_dengue_eggs_percentage / 100
        
        # Parâmetros das pessoas (como no NetLogo)
        self.people_lifespan = 72 * 365  # 72 anos em dias
        self.people_dengue_average_incubation_days = 6
        self.people_dengue_interval_incubation_days = 2
        self.people_dengue_average_viral_days = 8
        self.people_dengue_interval_viral_days = 4
        self.people_dengue_fatality_percentage = fatality_percentage / 100
        
        # Contadores globais (como no NetLogo)
        self.people_count_total = initial_humans
        self.people_count_with_dengue = initial_infected_humans
        self.people_count_recovered_from_dengue = 0
        self.people_count_death_common = 0
        self.people_count_death_dengue = 0
        
        self.mosquitoes_count_total = initial_mosquitoes
        self.mosquitoes_count_with_dengue = initial_infected_mosquitoes
        
        # OTIMIZAÇÃO: Cache para estados (calculados em update_counts)
        self.people_count_healthy = initial_humans - initial_infected_humans
        self.mosquitoes_count_healthy = initial_mosquitoes - initial_infected_mosquitoes
        
        # OTIMIZAÇÃO: Cache de vizinhanças (pré-calcular para cada célula)
        self._neighborhood_cache = {}
        
        # OTIMIZAÇÃO: Controle de frequência de coleta de dados
        self.data_collection_frequency = 1  # Coletar a cada N steps (1 = todo step)
        
        # Criar população inicial
        self.setup_initial_population(initial_humans, initial_mosquitoes, 
                                    initial_infected_humans, initial_infected_mosquitoes)
        
        # OTIMIZAÇÃO: Coletor de dados usa variáveis ao invés de funções
        # (evita iterações redundantes sobre todos os agentes)
        self.datacollector = DataCollector(
            {
                "Humanos Saudáveis": lambda m: m.people_count_healthy,
                "Humanos Infectados": lambda m: m.people_count_with_dengue,
                "Humanos Recuperados": lambda m: m.people_count_recovered_from_dengue,
                "Mosquitos Saudáveis": lambda m: m.mosquitoes_count_healthy,
                "Mosquitos Infectados": lambda m: m.mosquitoes_count_with_dengue,
                "Mortes Comuns": lambda m: m.people_count_death_common,
                "Mortes por Dengue": lambda m: m.people_count_death_dengue,
                "Total Pessoas": lambda m: m.people_count_total,
                "Total Mosquitos": lambda m: m.mosquitoes_count_total,
            }
        )

    def random_number(self, average, interval):
        """Gera número aleatório dentro de um intervalo (como random-number no NetLogo)"""
        interval_min = average - interval
        interval_max = average + interval
        return random.randint(interval_min, interval_max)
    
    def get_neighborhood_cached(self, pos):
        """
        OTIMIZAÇÃO: Retorna vizinhança com cache
        Em uma grade toroidal, a vizinhança de cada célula é sempre a mesma
        """
        if pos not in self._neighborhood_cache:
            self._neighborhood_cache[pos] = self.grid.get_neighborhood(
                pos, moore=True, include_center=False
            )
        return self._neighborhood_cache[pos]

    def setup_initial_population(self, num_humans, num_mosquitoes, 
                                num_infected_humans, num_infected_mosquitoes):
        """Cria população inicial (como setup-initial-population no NetLogo)"""
        # Criar humanos
        for i in range(num_humans):
            initial_dengue = i < num_infected_humans
            human = HumanAgent(i, self, initial_dengue=initial_dengue)
            
            # Posicionar na grade
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            self.grid.place_agent(human, (x, y))
        
        # Criar mosquitos
        for i in range(num_humans, num_humans + num_mosquitoes):
            initial_dengue = (i - num_humans) < num_infected_mosquitoes
            mosquito = MosquitoAgent(i, self, initial_dengue=initial_dengue)
            
            # Posicionar na grade
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            self.grid.place_agent(mosquito, (x, y))

    def seasonal_reproduction_factor(self):
        """Fator sazonal de reprodução (como seasonal-reproduction-factor no NetLogo)"""
        day_of_year = self.steps % 365
        reproduction_factor = math.sin(2 * math.pi * (day_of_year / 365)) * 0.5 + 0.5
        return reproduction_factor

    def reproduce_mosquitoes(self):
        """Reprodução de mosquitos (como mosquitoes-reproducing no NetLogo)"""
        # OTIMIZAÇÃO: Usar AgentSet para filtrar apenas mosquitos
        mosquitoes = [agent for agent in self.agents if isinstance(agent, MosquitoAgent)]
        
        if not mosquitoes:
            return
        
        mosquitoes_to_create = 0
        reproduction_factor = self.seasonal_reproduction_factor()
        
        # AJUSTE PARA SIMULAÇÕES REALISTAS: Balancear reprodução vs mortalidade
        # Chance de reprodução ajustada para manter população estável
        reproduction_chance = 0.95  # 5% de chance base
        
        # Aumentar chance se população está muito baixa (reposição)
        if self.mosquitoes_count_total < 100:
            reproduction_chance = 0.90  # 10% de chance
        
        for agent in mosquitoes:
            if random.random() > reproduction_chance:
                if agent.age > 3 and agent.age < agent.age_death:
                    # Número de ovos varia com sazonalidade
                    new_eggs = max(1, round(reproduction_factor * 5))  # Até 5 ovos
                    mosquitoes_to_create += new_eggs
        
        # Limitar crescimento populacional para evitar explosão
        max_mosquitoes = 15000  # Limite aumentado para permitir dinâmica realista
        if self.mosquitoes_count_total + mosquitoes_to_create > max_mosquitoes:
            mosquitoes_to_create = max(0, max_mosquitoes - self.mosquitoes_count_total)
        
        # Criar novos mosquitos
        if mosquitoes_to_create > 0:
            self.create_new_mosquitoes(mosquitoes_to_create)

    def create_new_mosquitoes(self, new_mosquitoes):
        """Cria novos mosquitos (como create-new-mosquitoes no NetLogo)"""
        current_id = self.people_count_total + self.mosquitoes_count_total
        
        for i in range(current_id, current_id + new_mosquitoes):
            # Determinar se o mosquito herda dengue
            inherit_dengue = False
            if random.random() < self.mosquitoes_dengue_inherit_eggs_percentage:
                inherit_dengue = True
            
            mosquito = MosquitoAgent(i, self, age=0, initial_dengue=inherit_dengue)
            
            # Posicionar na grade
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            self.grid.place_agent(mosquito, (x, y))
            
            self.mosquitoes_count_total += 1
            if inherit_dengue:
                self.mosquitoes_count_with_dengue += 1

    def reproduce_humans(self):
        """Reposição da população humana (como people-reproducing no NetLogo)"""
        if self.people_count_total < 1000:  # Manter população constante
            difference = 1000 - self.people_count_total
            current_id = self.people_count_total + self.mosquitoes_count_total
            
            for i in range(current_id, current_id + difference):
                human = HumanAgent(i, self, age=0, age_death=self.people_lifespan)
                
                # Posicionar na grade
                x = random.randint(0, self.grid.width - 1)
                y = random.randint(0, self.grid.height - 1)
                self.grid.place_agent(human, (x, y))
                
                self.people_count_total += 1

    def step(self):
        """Executa um passo da simulação (como button-go no NetLogo) - OTIMIZADO"""
        # Condição de parada: população muito pequena
        if self.people_count_total < 5 or self.mosquitoes_count_total < 5:
            self.running = False
            return
        
        # Parar se não há mais infectados
        if self.people_count_with_dengue == 0 and self.mosquitoes_count_with_dengue == 0:
            self.running = False
            return
        
        # OTIMIZAÇÃO: Criar lista apenas uma vez e permitir modificações
        # (agentes podem morrer durante o step)
        agents_to_step = list(self.agents)
        for agent in agents_to_step:
            # Verificar se agente ainda existe (pode ter morrido)
            if agent in self.agents:
                agent.step()
        
        # Reprodução (ajustada para manter dinâmica populacional)
        # Mosquitos: a cada 3 dias (ciclo de vida mais curto)
        # Humanos: a cada 7 dias (reposição da população)
        if self.steps % 3 == 0:
            self.reproduce_mosquitoes()
        if self.steps % 7 == 0:
            self.reproduce_humans()
        
        # Atualizar contadores (sempre necessário)
        self.update_counts()
        
        # OTIMIZAÇÃO: Coletar dados com frequência configurável
        # Para análises estatísticas robustas, não precisamos de todos os steps
        if self.steps % self.data_collection_frequency == 0:
            self.datacollector.collect(self)

    def update_counts(self):
        """Atualiza os contadores de população - OTIMIZADO"""
        people_infected = 0
        people_recovered = 0
        people_healthy = 0
        mosquitoes_infected = 0
        mosquitoes_healthy = 0
        people_total = 0
        mosquitoes_total = 0
        
        # OTIMIZAÇÃO: Uma única iteração para contar tudo
        for agent in self.agents:
            if isinstance(agent, HumanAgent):
                people_total += 1
                if agent.dengue:
                    people_infected += 1
                elif agent.dengue_recurrence > 0:
                    people_recovered += 1
                else:
                    people_healthy += 1
            elif isinstance(agent, MosquitoAgent):
                mosquitoes_total += 1
                if agent.dengue:
                    mosquitoes_infected += 1
                else:
                    mosquitoes_healthy += 1
        
        self.people_count_with_dengue = people_infected
        self.people_count_recovered_from_dengue = people_recovered
        self.people_count_healthy = people_healthy
        self.mosquitoes_count_with_dengue = mosquitoes_infected
        self.mosquitoes_count_healthy = mosquitoes_healthy
        self.mosquitoes_count_total = mosquitoes_total
        self.people_count_total = people_total

    @staticmethod
    def count_humans_by_state(model, state):
        """Conta humanos por estado - OTIMIZADO"""
        count = 0
        for agent in model.agents:
            if isinstance(agent, HumanAgent):
                if state == "S" and not agent.dengue and agent.dengue_recurrence == 0:
                    count += 1
                elif state == "I" and agent.dengue:
                    count += 1
                elif state == "R" and not agent.dengue and agent.dengue_recurrence > 0:
                    count += 1
        return count

    @staticmethod
    def count_mosquitoes_by_state(model, state):
        """Conta mosquitos por estado - OTIMIZADO"""
        count = 0
        for agent in model.agents:
            if isinstance(agent, MosquitoAgent):
                if state == "S" and not agent.dengue:
                    count += 1
                elif state == "I" and agent.dengue:
                    count += 1
        return count