import random
import math
from itertools import cycle, product

import matplotlib.pyplot as plot


class IsingModel:

    def __init__(self, linear_size, sum_threshold, exchange_interaction, temperature) -> None:
        self.linear_size = linear_size
        self.temperature = temperature
        self.exchange_interaction = exchange_interaction
        self.spins = [[random.choice((1, -1)) for _ in range(linear_size)] for _ in range(linear_size)]
        self.sum_energy = 0
        self.step = 0
        self.sum_threshold = sum_threshold
        self.lattice_iterator = cycle(product(range(linear_size), range(linear_size)))
        self.figure = None
        self.matrix = None
        self.plot_initialized = False

    def _neighbour_spins_sum(self, i, j):
        up = i - 1 if i > 0 else self.linear_size - 1
        down = i + 1 if i < self.linear_size - 1 else 0
        left = j - 1 if j > 0 else self.linear_size - 1
        right = j + 1 if j < self.linear_size - 1 else 0
        return self.spins[i][left] + self.spins[i][right] + self.spins[up][j] + self.spins[down][j]

    def mc_step(self):
        self.step += 1
        i, j = next(self.lattice_iterator)
        d_e = 2 * self.exchange_interaction * self.spins[i][j] * self._neighbour_spins_sum(i, j)
        if d_e <= 0 or random.random() <= math.exp(-d_e / self.temperature):
            self.spins[i][j] *= -1
            if self.step > self.sum_threshold:
                self.sum_energy += d_e

    def _initialize_plot(self):
        plot.ion()
        self.figure = plot.figure()
        ax = self.figure.add_subplot(111)
        self.matrix = ax.matshow(self.spins)

    def plot_state(self, fps):
        if self.step % fps == 0:
            if not self.plot_initialized:
                self._initialize_plot()
                self.plot_initialized = True
            self.matrix.set_data(self.spins)
            self.figure.canvas.draw()


im = IsingModel(100, 100000, 1, 0.1)
n = 10 ** 5
for t in range(4, 18, 1):
    tt = t / 4
    im.temperature = tt
    for k in range(1000000):
        im.mc_step()
    print(tt, im.sum_energy)
