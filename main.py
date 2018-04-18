import random
import math
import matplotlib.pyplot as plot


class IsingModel:

    def __init__(self, linear_size, sum_threshold, exchange_interaction, temperature) -> None:
        self._linear_size = linear_size
        self._sum_threshold = sum_threshold
        self._step = 0
        self._temperature = temperature
        self._exchange_interaction = exchange_interaction
        self._spins = [[random.choice((1, -1)) for _ in range(linear_size)] for _ in range(linear_size)]
        self._sum_energy = 0
        self._figure = None
        self._matrix = None
        self._plot_initialized = False

    def _neighbour_spins_sum(self, i, j):
        up = i - 1 if i > 0 else self._linear_size - 1
        down = i + 1 if i < self._linear_size - 1 else 0
        left = j - 1 if j > 0 else self._linear_size - 1
        right = j + 1 if j < self._linear_size - 1 else 0
        return self._spins[i][left] + self._spins[i][right] + self._spins[up][j] + self._spins[down][j]

    def mc_step(self):
        self._step += 1
        i = random.randrange(self._linear_size)
        j = random.randrange(self._linear_size)
        d_e = 2 * self._exchange_interaction * self._spins[i][j] * self._neighbour_spins_sum(i, j)
        if d_e <= 0 or random.random() <= math.exp(-d_e / self._temperature):
            self._spins[i][j] *= -1
            if self._step > self._sum_threshold:
                self._sum_energy += d_e

    def _initialize_plot(self):
        plot.ion()
        self._figure = plot.figure()
        ax = self._figure.add_subplot(111)
        self._matrix = ax.matshow(self._spins)

    def plot_state(self, fps):
        if self._step % fps == 0:
            if not self._plot_initialized:
                self._initialize_plot()
                self._plot_initialized = True
            self._matrix.set_data(self._spins)
            self._figure.canvas.draw()

    @property
    def average_energy(self):
        return self._sum_energy / (self._step - self._sum_threshold)


class Plotter:

    def __init__(self, iterations_number, lattice_size, sum_threshold, t_0, t_1, step, draw_spins) -> None:
        self.iterations_number = iterations_number
        self.lattice_size = lattice_size
        self.sum_threshold = sum_threshold
        self.t_0 = t_0
        self.t_1 = t_1
        self.step = step
        self.draw_spins = draw_spins

    def run(self):
        t = self.t_0
        x = []
        y = []
        for _ in range(int((self.t_1 - self.t_0) / self.step) + 1):
            im = IsingModel(self.lattice_size, self.sum_threshold, 1, t)
            for k in range(self.iterations_number):
                im.mc_step()
                if self.draw_spins:
                    im.plot_state(1000)
            t += self.step
            x.append(t)
            y.append(im.average_energy)
        plot.plot(x, y)
        plot.show()


Plotter(100000, 100, 0, 0.1, 5, 0.05, False).run()
