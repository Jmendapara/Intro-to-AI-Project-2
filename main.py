import matplotlib.pyplot as plt

from agents.simpleAgent import SimpleAgent
from agents.improvedAgent import ImprovedAgent

from enviornment.enviornment import Enviornment

TRIALS_PER_DENSITY = 20
BOARD_SIZE = 8
x = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]



simpleAgentValues = []
improvedAgentValues = []

env = Enviornment(8,0)
simp = SimpleAgent(env)
improved = ImprovedAgent(env)


for density in x:

    numberOfMines = int(round(BOARD_SIZE * BOARD_SIZE * density))

    print(density)
    print(numberOfMines)

    simpTempAcc = 0
    improvedTempAcc = 0

    for i in range(TRIALS_PER_DENSITY):

        env = Enviornment(BOARD_SIZE,numberOfMines)

        simp = SimpleAgent(env)
        improved = ImprovedAgent(env)


        print('simp')
        tempSimp = simp.execute()
        simpTempAcc += tempSimp/numberOfMines

        print('improved')
        tempImproved = improved.execute()

        improvedTempAcc += tempImproved/numberOfMines

        print('here')

    simpleAgentValues.append(simpTempAcc/TRIALS_PER_DENSITY)
    improvedAgentValues.append(improvedTempAcc/TRIALS_PER_DENSITY)

# plt.plot(x, simpleAgentValues)
# plt.ylabel('Accuracy')
# plt.xlabel('Mines Density')
# plt.title('Simple Strategy Accuracy')
# plt.ylim([0, 1])

# plt.show()

# plt.plot(x, improvedAgentValues)
# plt.ylabel('Accuracy')
# plt.xlabel('Mines Density')
# plt.title('Improved Strategy Accuracy')
# plt.ylim([0, 1])
# plt.show()


# plotting the line 1 points 
plt.plot(x, simpleAgentValues, label = "Simple Strategy")

# plotting the line 2 points 
plt.plot(x, improvedAgentValues, label = "Improved Strategy")
plt.xlabel('Mines Density')
# Set the y axis label of the current axis.
plt.ylabel('Accuracy')
# Set a title of the current axes.
plt.title('Simple vs. Improved Strategy Accuracy')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()




