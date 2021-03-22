import matplotlib.pyplot as plt

from agents.simpleAgent import SimpleAgent
from agents.improvedAgent import ImprovedAgent

from enviornment.enviornment import Enviornment


env = Enviornment(8,8)
simp = SimpleAgent(env)
simp.execute()