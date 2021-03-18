from agents.simpleAgent import SimpleAgent
from agents.improvedAgent import ImprovedAgent

from enviornment.enviornment import Enviornment

env = Enviornment(8,10)
simp = SimpleAgent(env)
improved = ImprovedAgent(env)

improved.execute()



