from mesa import Agent
import random
import math

class HumanAgent(Agent):
    def __init__(self, unique_id, model, age=None, age_death=None, initial_dengue=False):
        super().__init__(model)
        self.unique_id = unique_id
        
        # Propriedades básicas (como no NetLogo)
        self.age = age if age is not None else random.randint(0, self.model.people_lifespan)
        self.age_death = age_death if age_death is not None else random.randint(0, self.model.people_lifespan) + 10 * 365
        
        # Estados da dengue (como no NetLogo)
        self.dengue = False
        self.transmitter = False
        self.days_dengue_incubation = self.model.random_number(
            self.model.people_dengue_average_incubation_days,
            self.model.people_dengue_interval_incubation_days
        )
        self.days_dengue_viral = self.model.random_number(
            self.model.people_dengue_average_viral_days,
            self.model.people_dengue_interval_viral_days
        )
        self.days_dengue_sick = 0
        self.dengue_recurrence = 0
        
        # Inicializar com dengue se especificado
        if initial_dengue:
            self.get_sick()

    def get_sick(self):
        """Infecta o humano com dengue (como each-get-sick no NetLogo)"""
        self.dengue = True
        self.days_dengue_sick = 1
        self.transmitter = False
        self.dengue_recurrence += 1

    def move(self):
        """Movimento realista dos agentes (como each-move no NetLogo) - OTIMIZADO"""
        # OTIMIZAÇÃO: Reduzir frequência de movimento para 10% (ao invés de 30%)
        if random.random() < 0.1:
            # OTIMIZAÇÃO: Usar cache de vizinhança
            possible_steps = self.model.get_neighborhood_cached(self.pos)
            if possible_steps:
                new_position = random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)

    def check_sick(self):
        """Verifica progressão da doença (como each-check-sick no NetLogo)"""
        if self.days_dengue_sick != 0:
            self.days_dengue_sick += 1
            
            # Tornar-se transmissor após período de incubação
            if not self.transmitter and self.days_dengue_sick >= self.days_dengue_incubation:
                self.transmitter = True

    def aging(self):
        """Envelhecimento (como people-aging no NetLogo)"""
        self.age += 1
        
        # Verificar morte por idade
        if self.age >= self.age_death:
            self.model.people_count_death_common += 1
            self.model.agents.discard(self)

    def check_health(self):
        """Verifica saúde e possíveis mortes (como people-checking-health no NetLogo)"""
        if self.transmitter:
            # Chance de morte por dengue (mais realista)
            if random.random() < 0.01:  # 1% de chance de morrer quando transmissor
                self.model.people_count_death_dengue += 1
                self.model.agents.discard(self)
                return
        
        # Recuperação após período viral
        if self.days_dengue_sick > self.days_dengue_incubation + self.days_dengue_viral:
            self.dengue = False
            self.transmitter = False
            self.days_dengue_sick = 0

    def step(self):
        """Executa um passo do agente"""
        self.move()
        self.check_sick()
        self.aging()
        self.check_health()


class MosquitoAgent(Agent):
    def __init__(self, unique_id, model, age=None, age_death=None, initial_dengue=False):
        super().__init__(model)
        self.unique_id = unique_id
        
        # Propriedades básicas (como no NetLogo)
        self.age = age if age is not None else random.randint(0, self.model.mosquitoes_lifespan)
        self.age_death = age_death if age_death is not None else self.model.random_number(
            self.model.mosquitoes_lifespan, 15
        )
        
        # Estados da dengue (como no NetLogo)
        self.dengue = False
        self.transmitter = False
        self.days_dengue_incubation = self.model.random_number(
            self.model.mosquitoes_dengue_average_incubation_days,
            self.model.mosquitoes_dengue_interval_incubation_days
        )
        self.days_dengue_sick = 0
        
        # Inicializar com dengue se especificado
        if initial_dengue:
            self.get_sick()

    def get_sick(self):
        """Infecta o mosquito com dengue (como each-get-sick no NetLogo)"""
        self.dengue = True
        self.days_dengue_sick = 1
        self.transmitter = False

    def move(self):
        """Movimento realista dos agentes (como each-move no NetLogo) - OTIMIZADO"""
        # OTIMIZAÇÃO: Reduzir frequência de movimento para 10% (ao invés de 30%)
        if random.random() < 0.1:
            # OTIMIZAÇÃO: Usar cache de vizinhança
            possible_steps = self.model.get_neighborhood_cached(self.pos)
            if possible_steps:
                new_position = random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)

    def check_sick(self):
        """Verifica progressão da doença (como each-check-sick no NetLogo)"""
        if self.days_dengue_sick != 0:
            self.days_dengue_sick += 1
            
            # Tornar-se transmissor após período de incubação
            if not self.transmitter and self.days_dengue_sick >= self.days_dengue_incubation:
                self.transmitter = True

    def aging(self):
        """Envelhecimento (como mosquitoes-aging no NetLogo)"""
        self.age += 1
        
        # Verificar morte por idade
        if self.age >= self.age_death:
            self.model.agents.discard(self)

    def bite(self):
        """Simula picada e transmissão (como mosquitoes-biting no NetLogo) - OTIMIZADO"""
        # OTIMIZAÇÃO: Apenas tentar picar se relevante (infectado ou pode ser infectado)
        if not (self.dengue and self.transmitter) and not (not self.dengue):
            return
            
        # Encontrar pessoas na mesma posição
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        humans = [obj for obj in cellmates if isinstance(obj, HumanAgent)]
        
        if not humans:
            return
            
        victim = random.choice(humans)
        
        # Transmissão de mosquito para pessoa (com probabilidade realista)
        if (self.dengue and self.transmitter and 
            not victim.dengue and random.random() < 0.1):  # 10% de chance
            victim.get_sick()
        
        # Transmissão de pessoa para mosquito (com probabilidade realista)
        if (not self.dengue and victim.dengue and 
            victim.transmitter and random.random() < 0.2):  # 20% de chance
            self.get_sick()

    def step(self):
        """Executa um passo do agente"""
        self.move()
        self.check_sick()
        self.aging()
        self.bite()