import numpy as np
import matplotlib.pyplot as plt
import time
import math

class Person():
    ''' A person. '''

    age = None
    death_age = None
    dead = False

    def __init__(self, age, avg_life_expectancy, var_life_expectancy):
        self.age = age
        self.death_age = np.random.normal(avg_life_expectancy, var_life_expectancy)

    @property
    def dead(self):
        return self.age > self.death_age

class Population():
    ''' A list of people. '''

    people = []

    def __init__(self, people):
        self.people = people

    def grow(self, number, avg_life_expectancy, var_life_expectancy):
        self.people = self.people + [Person(0, avg_life_expectancy, var_life_expectancy) for n in range(number)] # Add `number` new people to the population

    def age(self):
        for person in self.people: # Age everyone by one year
            person.age += 1
        self.people = [person for person in self.people if person.dead == False] # Remove dead people

    @property
    def number(self):
        return len(self.people)

def simulate(years, birth_rate, avg_life_expectancy, var_life_expectancy, life_expectancy_increase_factor):
    population = Population([Person(0, avg_life_expectancy, var_life_expectancy) for _ in range(100)]) # Create a population of 10 people

    population_over_time = []
    years_passed = []
    avg_life_expectancy_over_time = []
    death_rates_over_time = []
    average_age_over_time = []
    try:
        for year in range(years):
            current_population = population.number
            # It is CRUCIAL that the population ages before it grows, else it is unfair since dead people are creating babies!
            population.age()
            if current_population == 0:
                death_rates_over_time.append(0)
            else:
                death_rates_over_time.append((current_population-population.number)/current_population) # The percentage of the population that died
            number_to_grow = np.sum(np.random.uniform(size=population.number) < birth_rate)
            population.grow(number_to_grow, avg_life_expectancy, var_life_expectancy)
            print("Year: {} Current population: {}".format(year, population.number))
            population_over_time.append(population.number)
            avg_life_expectancy += math.exp(-0.001*year)*life_expectancy_increase_factor
            avg_life_expectancy_over_time.append(avg_life_expectancy)
            print("Current life expectancy: {}".format(avg_life_expectancy))
            average_age = np.mean([person.age for person in population.people])
            print("Current average age: {}".format(average_age))
            average_age_over_time.append(average_age)
            if year == 50: # Increase birth rate
                birth_rate = birth_rate * 2
            if year == 100: # Restore birth rate
                birth_rate = birth_rate / 2
            years_passed.append(year)
    except KeyboardInterrupt:
        print('Stopping simulation.')
        avg_life_expectancy_over_time = avg_life_expectancy_over_time[0:int(len(years_passed))]
        population_over_time = population_over_time[0:int(len(years_passed))]
        death_rates_over_time = death_rates_over_time[0:int(len(years_passed))]
        average_age_over_time = average_age_over_time[0:int(len(years_passed))]

    return years_passed, avg_life_expectancy_over_time, population_over_time, death_rates_over_time, average_age_over_time

# INITIAL PARAMETERS #

avg_life_expectancy = 60 # The current mean age of death. Death is assumed to be a normal distribution around this value
var_life_expectancy = 10 # The variance in the age of death, assuming a normal distribution.
life_expectancy_increase_factor = 0.3 # The initial rate of increase in life expectancy per year. Note that the absolute increase exponentially decreases.
years = 10000
# TODO: Not important statistically, but might be nice to account for the fact that people only reproduce at a "fertile" age
birth_rate = 20/1000 # Probability for a living person to reproduce in a given year (calculated as N * birth rate per N people) - The `crude birth rate` https://en.wikipedia.org/wiki/Birth_rate

fig, ax = plt.subplots(1,4)
fig.set_figheight(5)
fig.set_figwidth(20)
for life_expectancy_increase_factor in [0.01, 0.012, 0.013]:
    years_passed, avg_life_expectancy_over_time, population_over_time, death_rates_over_time, average_age_over_time = simulate(years, birth_rate, avg_life_expectancy, var_life_expectancy, life_expectancy_increase_factor)
    ax[0].plot(years_passed, population_over_time, label=life_expectancy_increase_factor)
    ax[1].plot(years_passed, avg_life_expectancy_over_time, label=life_expectancy_increase_factor)
    ax[2].plot(years_passed, death_rates_over_time, label=life_expectancy_increase_factor)
    ax[3].plot(years_passed, average_age_over_time, label=life_expectancy_increase_factor)

print('Plotting and saving.')
ax[0].set_title('Population Simulations')
ax[0].set_xlabel('Year')
ax[0].set_ylabel('People')
ax[0].legend()
ax[1].set_title('Average Life Expectancy')
ax[1].set_xlabel('Year')
ax[1].set_ylabel('Average Life Expectancy')
ax[1].legend()
ax[2].plot(years_passed, np.ones_like(years_passed)*birth_rate, label='Birth rate')
ax[2].set_title('Death Rates over Time')
ax[2].set_xlabel('Year')
ax[2].set_ylabel('Death Rate')
ax[2].set_ylim(0, birth_rate*2)
ax[2].legend()
ax[3].set_title('Average Age of Population')
ax[3].set_xlabel('Year')
ax[3].set_ylabel('Average Age')
ax[3].legend()
plt.savefig('example.png')
