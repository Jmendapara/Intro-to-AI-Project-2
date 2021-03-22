import matplotlib.pyplot as plt

from agents.improvedAgent import ImprovedAgent

from enviornment.enviornment import Enviornment


env = Enviornment(8,10)
improved = ImprovedAgent(env)
improved.execute()