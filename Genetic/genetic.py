import random
import time
from csv import reader

GATES = ["AND", "OR", "XOR", "NAND", "NOR", "XNOR"]
SURVIVING_CHROMOSOMES_NUM = 10
MUT_AND_CROSS_FROM_FIRST = 20
TO_BE_CROSSED_OVER_FIRST = 20
TO_BE_CROSSED_OVER_LAST = 30
TO_BE_MUTATED_FIRST = 20
TO_BE_MUTATED_LAST = 30
SINGLE_GENE_MUTATION_HIGH_POSSIBILITY = 0.4
SINGLE_GENE_MUTATION_LOW_POSSIBILITY = 0.15
POPULATION = 50


def get_gate_output(gate, in1, in2):
    if in1 == 'TRUE':
        in1 = True
    elif in1 == 'FALSE':
        in1 = False
    if in2 == 'TRUE':
        in2 = True
    elif in2 == 'FALSE':
        in2 = False

    if gate == "AND":
        return in1 & in2
    if gate == "OR":
        return in1 | in2
    if gate == "XOR":
        return in1 ^ in2
    if gate == "NAND":
        return not in1 & in2
    if gate == "NOR":
        return not in1 | in2
    if gate == "XNOR":
        return not in1 ^ in2


class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        fitness = 0
        for i in range(1, len(truth_table)):
            sample_input = truth_table[i]
            output = get_gate_output(self.genes[0], sample_input[0], sample_input[1])
            for k in range(gates_num - 1):
                output = get_gate_output(self.genes[k + 1], output, sample_input[k + 2])
            expected_output = sample_input[gates_num + 1]
            if expected_output == 'FALSE':
                expected_output = False
            else:
                expected_output = True

            if output == expected_output:
                fitness += 1
        return fitness


def generate_random_chromosome():
    genes = []
    for i in range(gates_num):
        rand_gate = random.choice(GATES)
        genes.append(rand_gate)
    return Chromosome(genes)


def execute_cross_over(p1, p2):
    # One point crossover
    first_chromosome = p1.genes
    second_chromosome = p2.genes
    chromosome_length = len(first_chromosome)
    start = int(0.2 * chromosome_length)
    end = int(0.9 * chromosome_length)
    point = int(random.randrange(start, end))
    first_new_chromosome = first_chromosome[:point]
    first_new_chromosome.extend(second_chromosome[point:])
    second_new_chromosome = second_chromosome[:point]
    second_new_chromosome.extend(first_chromosome[point:])
    # print("===================")
    # print("Child_length: ", len(first_new_chromosome))
    # print("Parent_length: ", len(first_chromosome))
    # print("===================")
    return Chromosome(first_new_chromosome), Chromosome(second_new_chromosome)


def cross_over(parents):
    children = []
    print("Crossover candidates num: ", len(parents))
    while len(parents) > 0:
        first_parent = parents.pop(int(random.randrange(0, len(parents))))
        second_parent = parents.pop(int(random.randrange(0, len(parents))))
        first_child, second_child = execute_cross_over(first_parent, second_parent)
        children.append(first_child)
        children.append(second_child)

    return children


def allowed_mutation(possibility):
    rand = random.randrange(0, 100)
    return rand < (possibility * 100)


def execute_mutation(chromosome, possibility):
    for i in range(len(chromosome)):
        if allowed_mutation(possibility):
            new_gate = random.choice(GATES)
            chromosome[i] = new_gate
    return chromosome


def mutate(mutation_candidates, possibility):
    print("Mutation candidates num: ", len(mutation_candidates))
    mutated_chromosomes = []
    for chromosome in mutation_candidates:
        mutated = execute_mutation(chromosome.genes, possibility)
        mutated_chromosomes.append(Chromosome(mutated))

    return mutated_chromosomes


def print_solution(chromosome, last_generation):
    print("Gates: ", chromosome.genes)
    print("Found after: ", last_generation, " generations!")


def start_genetic(total_population):
    generation_id = 1
    total_population.sort(key=lambda ch: ch.fitness, reverse=True)
    while total_population[0].fitness < max_fitness:
        print("Max fitness: ", total_population[0].fitness, total_population[1].fitness, total_population[2].fitness)
        crossed_over_chromosomes = cross_over(total_population[TO_BE_CROSSED_OVER_FIRST:TO_BE_CROSSED_OVER_LAST])
        mutated_chromosomes_high = mutate(total_population[TO_BE_MUTATED_FIRST:TO_BE_MUTATED_LAST], SINGLE_GENE_MUTATION_HIGH_POSSIBILITY)
        crossed_over_to_mutation = cross_over(total_population[:MUT_AND_CROSS_FROM_FIRST])
        crossed_over_and_mutated = mutate(crossed_over_to_mutation, SINGLE_GENE_MUTATION_LOW_POSSIBILITY)

        total_population = total_population[:SURVIVING_CHROMOSOMES_NUM]
        total_population.extend(crossed_over_and_mutated)
        total_population.extend(mutated_chromosomes_high)
        total_population.extend(crossed_over_chromosomes)
        total_population.sort(key=lambda ch: ch.fitness, reverse=True)
        generation_id += 1

    print_solution(total_population[0], generation_id)


with open('truth_table.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    truth_table = list(csv_reader)

gates_num = len(truth_table[0]) - 2
max_fitness = pow(2, gates_num + 1)
population = []
start_time = time.time()
for j in range(POPULATION):
    new_chromosome = generate_random_chromosome()
    population.append(new_chromosome)
    # print(new_chromosome)

start_genetic(population)
finish_time = time.time()
print("Genetic algorithm finished in %f seconds!" % (finish_time - start_time))
