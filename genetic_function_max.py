"""
Copyright 2016 Waizung Taam

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# 2016-09-25

import math
import random
import string


class Genetic:
    """Genentic algorithm for finding function maximum value

    Find the maximum value of a function in a certain interval with a
    cartain precision.
    """
    def __init__(self, population_size, elite_rate, cross_rate, mutate_rate,
                 num_generations=1000):
        """Init Genetic

        :param population_size  the size of the population
        :param elite_rate       the rate for choosing the elites
        :param cross_rate       the rate of crossing over
        :param mutate_rate      the rate of mutation
        :param num_generation   the max number of generations
        """
        self._population_size = population_size
        self._elite_rate = elite_rate
        self._cross_rate = cross_rate
        self._mutate_rate = mutate_rate
        self._num_generations = num_generations
        self._elite_size = int(self._elite_rate * self._population_size)
        self._lower_bound = None
        self._upper_bound = None
        self._precision = None
        self._binary_length = None

    def evolve(self, function, lower_bound, upper_bound, precision):
        """Evolve to find the maximum value

        :param function     the objective function
        :param lower_bound  the lower bound of the interval
        :param upper_bound  the upper bound of the interval
        :param precision    the required precision
        """
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._precision = precision
        self._binary_length = math.ceil(math.log2(
            (upper_bound - lower_bound) / precision))
        chromosomes = self._encode()
        population = [random.choice(chromosomes) for _ in \
            range(self._population_size)]
        next_generateion = [random.choice(chromosomes) for _ in \
            range(self._population_size)]
        for i in range(self._num_generations):
            self._select(population, next_generateion, function)
            self._cross_over(population, next_generateion)
            self._mutate(next_generateion)
            population, next_generateion = next_generateion, population
            print(i, "%.4f" % self._fitness(
                function, self._decode(population[0])), 
                self._decode(population[0]))

    def _select(self, population, next_generateion, function):
        population = sorted(population, 
            key=lambda x: self._fitness(function, self._decode(x)), 
            reverse=True)
        next_generateion[: self._elite_size] = population[: self._elite_size]

    def _cross_over(self, population, next_generateion):
        for i in range(self._elite_size, self._population_size):
            if self._cross_rate >= random.uniform(0, 1):
                i_left = random.randint(0, self._population_size - 1)
                i_right = random.randint(0, self._population_size - 1)
                pos = random.randint(0, self._binary_length - 1)
                next_generateion[i] = population[i_left][:pos] + \
                    population[i_right][pos:]

    def _mutate(self, next_generateion):
        for i in range(self._elite_size, self._population_size):
            if self._mutate_rate >= random.uniform(0, 1):
                pos = random.randint(0, self._binary_length - 1)
                if next_generateion[i][pos] == 0:
                    mutated_bit = '1'
                else:
                    mutated_bit = '0'
                next_generateion[i] = next_generateion[i][:pos] + \
                    mutated_bit + next_generateion[i][pos + 1 :]

    def _fitness(self, function, *args):
        return function(*args)

    def _encode(self):
        ls = []
        for i in range(int(
            (self._upper_bound - self._lower_bound) / self._precision)):
            ls.append(bin(i)[2:].zfill(self._binary_length))
        return ls

    def _decode(self, binary):
        x = self._lower_bound + int(binary, 2) * \
            (self._upper_bound - self._lower_bound) / 2 ** self._binary_length
        return x


def f(x):
    return x + 10 * math.sin(5 * x) + 7 * math.cos(4 * x)

def demo():
    model = Genetic(9000, 0.1, 0.8, 0.9, 100)
    model.evolve(f, 0, 9, 1e-4)
    
    # 24.8554 7.85687255859375


if __name__ == "__main__":
    demo()