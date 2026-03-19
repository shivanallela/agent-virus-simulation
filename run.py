from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

# Agent
class Person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.infected = False

    def step(self):
        # Move randomly
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        # Infection logic
        if self.infected:
            neighbors = self.model.grid.get_cell_list_contents([self.pos])
            for agent in neighbors:
                if not agent.infected and random.random() < 0.3:
                    agent.infected = True


# Model
class VirusModel(Model):
    def __init__(self, n, width=10, height=10):
        self.num_agents = n
        self.grid = MultiGrid(width, height, True)  # ✅ grid added
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            agent = Person(i, self)
            self.schedule.add(agent)

            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # Start with 1 infected
        self.schedule.agents[0].infected = True

    def step(self):
        self.schedule.step()