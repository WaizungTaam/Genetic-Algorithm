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

import random
import string


class Genetic:
    """Genetic algorithm for learning a string

    Re-generate the given string from random string.
    """
    def __init__(self, population_size, elite_rate, cross_rate, mutate_rate,
                 error_criterion=1e-8):
        """Init Genetic

        :param population_size  the size of the population
        :param elite_rate       the rate for choosing the elites
        :param cross_rate       the rate of crossing over
        :param mutate_rate      the rate of mutation
        :param error_criterion  error criterion for quiting the loop
        """
        self._population_size = population_size
        self._elite_rate = elite_rate
        self._cross_rate = cross_rate
        self._mutate_rate = mutate_rate
        self._error_criterion = error_criterion
        self._elite_size = int(self._elite_rate * self._population_size)
        self._feasible_region = string.ascii_letters + string.digits + \
            string.punctuation + string.whitespace

    def evolve(self, target):
        """Evolve to fit the target string.

        :param target  the target string
        """
        population = [self._random_string(len(target)) for _ in \
            range(self._population_size)]
        next_generateion = [self._random_string(len(target)) for _ in \
            range(self._population_size)]
        while self._fitness(population[0], target) > self._error_criterion:
            self._select(population, next_generateion, target)
            self._cross_over(population, next_generateion, len(target))
            self._mutate(next_generateion, len(target))
            population, next_generateion = next_generateion, population
            print("%.2f" % self._fitness(population[0], target), \
                population[0])

    def _select(self, population, next_generateion, target):
        population = sorted(population, key=lambda x: self._fitness(x, target))
        next_generateion[: self._elite_size] = population[: self._elite_size]

    def _cross_over(self, population, next_generateion, target_length):
        for i in range(self._elite_size, self._population_size):
            if self._cross_rate >= random.uniform(0, 1):
                i_left = random.randint(0, self._population_size - 1)
                i_right = random.randint(0, self._population_size - 1)
                pos = random.randint(0, target_length - 1)
                next_generateion[i] = population[i_left][:pos] + \
                    population[i_right][pos:]

    def _mutate(self, next_generateion, target_length):
        for i in range(self._elite_size, self._population_size):
            if self._mutate_rate >= random.uniform(0, 1):
                pos = random.randint(0, target_length - 1)
                next_generateion[i] = next_generateion[i][:pos] + \
                    random.choice(self._feasible_region) + \
                    next_generateion[i][pos + 1 :]

    def _random_string(self, length):
        return "".join(random.choice(self._feasible_region) \
            for _ in range(length))

    def _fitness(self, individual, target):
        return sum([abs(ord(individual[i]) - ord(target[i])) \
            for i in range(len(target))]) / len(target)


def demo():
    model = Genetic(2048, 0.2, 0.5, 0.1)
    model.evolve("Hello World!")


if __name__ == "__main__":
    demo()