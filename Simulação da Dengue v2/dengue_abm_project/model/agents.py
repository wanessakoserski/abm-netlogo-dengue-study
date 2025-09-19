from mesa import Agent
import random 


class HumanAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.days_infected = 0

        # Estados: S (susceptível), I (infectado), R (recuperado)
        self.state = "S" 

    def step(self):
        if self.state == "I":
            self.days_infected += 1
            
            if self.days_infected > self.model.recovery_time:
                self.state = "R"


class MosquitoAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state == "S"

    def step(self):
        if self.state == "I":
            humans = [a for a in self.model.grid.get_cell_list_contents([self.pos])
                        if isinstance(a, HumanAgent) and a.state == "S"]
            
            for human in humans:
                if random.random() < self.model.transmission_prob:
                    human.state = "I"

        else:
            humans = [a for a in self.model.grid.get_cell_list_contents([self.pos])
                        if isinstance(a, HumanAgent) and a.state == "I"]
            
            if humans and random.random() < self.model.transmission_prob:
                self.state = "I"

