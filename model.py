from mesa import Agent, Model
from mesa.time import RandomActivation
import random

# Agent class
class Person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.infected = False

    def step(self):
        if self.infected:
            # interact with only 2 random agents
            others = self.random.sample(self.model.schedule.agents, 2)
            for agent in others:
                if not agent.infected and random.random() < 0.3:
                    agent.infected = True


# Model class
class VirusModel(Model):
    def __init__(self, n):
        self.schedule = RandomActivation(self)

        # create agents
        for i in range(n):
            person = Person(i, self)
            self.schedule.add(person)

        # start with only 1 infected agent
        self.schedule.agents[0].infected = True

    def step(self):
        self.schedule.step()


# Run simulation
model = VirusModel(10)

for i in range(5):
    model.step()
    infected_count = sum([agent.infected for agent in model.schedule.agents])
    print(f"Step {i}: {infected_count} infected")