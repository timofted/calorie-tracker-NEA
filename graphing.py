import matplotlib.pyplot as plt
import numpy as np


weight= np.array([80,78,81,79,76])


plt.title("Weight information")
plt.xlabel("Times logged")
plt.ylabel("Weight (kg)")
plt.grid()

plt.plot(weight,marker="s")


plt.show()