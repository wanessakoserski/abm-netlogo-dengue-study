from mesa import Model 
from mesa.time import RandomActivation 
from mesa.space import MultiGrid
from model.agents import HumanAgend, MosquitoAgent


class DengueABM(Model):
    def __init__(self, width=10, height=10, initial_humans=50, initial_mosquitoes=100, transmission_prob=0.2, recovery_time=14):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.transmission_prob = transmission_prob
        self.recovery_time = recovery_time

        for i in range(initial_humans):
            human = HumanAgent(i, self)
            self.schedule.add(human)
            x, y = self.random.randrange(width), self.random.randrange(height)
            self.grid.place_agent(human, (x, y))

        for i in range(initial_humans, initial_humans + initial_mosquitoes):
            mosquito = MosquitoAgent(i, self)
            self.schedule.add(mosquito)
            x, y = self.random.randrange(width), self.random.randrange(height)
            self.grid.place_agent(mosquito, (x, y))

    def step(self):
        self.schedule.step()