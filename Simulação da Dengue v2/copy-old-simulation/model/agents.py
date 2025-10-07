from mesa import Agent
import random

class HumanAgent(Agent):
    def __init__(self, unique_id, model, age=None, age_death=None, initial_dengue=False):
        super().__init__(unique_id, model)
        self.state = "S"  # Estados: S (susceptível), I (infectado), R (recuperado)
        self.age = age if age is not None else random.randint(0, 72*365)
        self.age_death = age_death if age_death is not None else random.randint(0, 72*365) + 10*365
        
        # Parâmetros da dengue
        self.days_dengue_incubation = self.model.random.normalvariate(
            self.model.people_dengue_average_incubation_days,
            self.model.people_dengue_interval_incubation_days/3
        )
        self.days_dengue_viral = self.model.random.normalvariate(
            self.model.people_dengue_average_viral_days,
            self.model.people_dengue_interval_viral_days/3
        )
        self.days_sick = 0
        self.dengue_recurrence = 0
        self.transmitter = False
        
        # Inicializar com dengue se especificado
        if initial_dengue:
            self.get_sick()

    def get_sick(self):
        """Infecta o humano com dengue"""
        if self.state != "R":  # Só pode ser infectado se não for imune
            self.state = "I"
            self.days_sick = 1
            self.transmitter = False
            self.dengue_recurrence += 1

    def step(self):
        # Envelhecer
        self.age += 1
        
        # Verificar morte por idade
        if self.age >= self.age_death:
            self.model.people_count_death_common += 1
            self.model.schedule.remove(self)
            return
            
        # Processar progressão da doença
        if self.state == "I":
            self.days_sick += 1
            
            # Tornar-se transmissor após período de incubação
            if not self.transmitter and self.days_sick >= self.days_dengue_incubation:
                self.transmitter = True
                
            # Recuperar após período viral
            if self.days_sick > self.days_dengue_incubation + self.days_dengue_viral:
                # Verificar morte por dengue
                if random.random() < self.model.people_dengue_fatality_percentage:
                    self.model.people_count_death_dengue += 1
                    self.model.schedule.remove(self)
                else:
                    self.state = "R"
                    self.transmitter = False
                    self.days_sick = 0

class MosquitoAgent(Agent):
    def __init__(self, unique_id, model, age=None, age_death=None, initial_dengue=False):
        super().__init__(unique_id, model)
        self.state = "S"  # Estados: S (susceptível), I (infectado)
        self.age = age if age is not None else random.randint(0, model.mosquitoes_lifespan)
        self.age_death = age_death if age_death is not None else random.randint(
            max(0, model.mosquitoes_lifespan - 15), 
            model.mosquitoes_lifespan + 15
        )
        
        # Parâmetros da dengue
        self.days_dengue_incubation = self.model.random.normalvariate(
            self.model.mosquitoes_dengue_average_incubation_days,
            self.model.mosquitoes_dengue_interval_incubation_days/3
        )
        self.days_sick = 0
        self.transmitter = False
        
        # Inicializar com dengue se especificado
        if initial_dengue:
            self.get_sick()

    def get_sick(self):
        """Infecta o mosquito com dengue"""
        self.state = "I"
        self.days_sick = 1
        self.transmitter = False

    def step(self):
        # Envelhecer
        self.age += 1
        
        # Verificar morte por idade
        if self.age >= self.age_death:
            self.model.schedule.remove(self)
            return
            
        # Processar progressão da doença
        if self.state == "I":
            self.days_sick += 1
            
            # Tornar-se transmissor após período de incubação
            if not self.transmitter and self.days_sick >= self.days_dengue_incubation:
                self.transmitter = True
                
            # Tentar picar humanos
            self.bite()

    def bite(self):
        """Simula a picada do mosquito e possível transmissão de dengue"""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        humans = [obj for obj in cellmates if isinstance(obj, HumanAgent)]
        
        if humans:
            human = random.choice(humans)
            
            # Mosquito infectado pode infectar humano susceptível
            if self.transmitter and human.state == "S":
                if random.random() < self.model.transmission_prob_mosquito_to_human:
                    human.get_sick()
            
            # Humano infectado pode infectar mosquito susceptível
            if human.transmitter and self.state == "S":
                if random.random() < self.model.transmission_prob_human_to_mosquito:
                    self.get_sick()
                    