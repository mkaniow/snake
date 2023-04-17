import numpy as np

memory = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])

#print(memory)

a = np.random.choice(5, 2)

states = memory[a]

#print(a)

#print(states)

n_actions = 5

action_space = [i for i in range(n_actions)]

action_values = np.array(action_space, dtype=np.int8)

print(action_values)