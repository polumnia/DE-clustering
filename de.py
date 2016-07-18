import random
import math

# math functions & constants
sin = math.sin
cos = math.cos
sqrt = math.sqrt
pi = math.pi
fabs = math.fabs

# FIX (no globals)
dim = 0
Xu = []
Xl = []
pop = []
fvals = []
num_fe = 0  # count the total number of function evaluations
max_gen = 0  # number of generations
NP = 15
cr = 0.90  # crossover probability
F = 0.90  # Scaling factor
U = []  # trial vector

f_best = -1


# util function- return a random real in (0.0,1.0)
def urand():
    return random.random()


# objective function
def func(X):
    global num_fe
    sum = 0

    # Rastrigin function (2 variables)
    # for i in xrange(0,dim):
    #     sum = sum + 10*cos(2*pi*X[i]*X[i])


    # Schwefel function (20 variables)
    #     for i in xrange(0,dim):
    #         sum = sum + X[i]*sin(sqrt(fabs(X[i])))
    #     sum = 418.9828872724337998*(dim*1.0) - sum


    # First De Jong function (Sphere)
    # [-5.12,5.12]
    for i in xrange(0, dim):
        sum = sum + X[i] * X[i];

    # Second De Jong function (Rosenbrock's Function)
    # [-2.048,2.048]
    # sum = 100.0*((X[0]**2 - X[1])**2) + (1.0-X[0])**2

    num_fe = num_fe + 1

    return sum


# Control parameters
def setup():
    global max_gen, dim, Xu, Xl, NP, f_best

    max_gen = input("Enter the max. number of generations:: ")
    dim = input("Enter the dimension of the problem:: ")

    #     for i in xrange(0,dim):
    #         print "Enter the lower and upper bound of %d th variable" %i
    #         Xl.insert(i,input())
    #         Xu.insert(i,input())

    print
    "Enter the lower and upper bound of variables: "
    l = input()
    u = input()
    for i in xrange(0, dim):
        Xl.insert(i, l)
        Xu.insert(i, u)

    # NP=20*dim #population size

    # Open the file to store the best individual of every generation
    f_best = open("best_pop.out", "w")


# Initialize population
def initpop():
    global pop, fvals, num_fe

    pop = []
    fvals = []

    for i in xrange(0, NP):
        X = []
        for j in xrange(0, dim):
            # fill up X and just add it to the pop
            X.insert(j, (Xl[j] + (Xu[j] - Xl[j]) * urand()))

        # bounds check
        for j in xrange(0, dim):
            while X[j] < Xl[j] or X[j] > Xu[j]:
                if X[j] < Xl[j]:
                    X[j] = 2 * Xl[j] - X[j]
                if X[j] > Xu[j]:
                    X[j] = 2 * Xu[j] - X[j]

        pop.insert(i, X)
        fvals.insert(i, func(X))  # function evaluation


# DE/rand/1
def evolve_de_rand_1():
    global pop, fvals

    for i in xrange(0, max_gen):
        # Write the best individual of this generation into a file
        # best_pop.out
        write_best()
        for j in xrange(0, NP):

            ''' Mutation '''
            # select r1,r2,r3 in [0,NP) such that r1 != j !r2 != r3
            while 1:
                r1 = random.randint(0, NP - 1)
                if r1 != j:
                    break

            while 1:
                r2 = random.randint(0, NP - 1)
                if r2 != r1 and r2 != j:
                    break

            while 1:
                r3 = random.randint(0, NP - 1)
                if r3 != r2 and r3 != r1 and r3 != j:
                    break

            U = []
            for k in xrange(0, dim):
                # if urand() <= cr and k == dim_rand:
                U.insert(k, (pop[r3])[k] + F * ((pop[r1])[k] - (pop[r2])[k]))
                # else:
                #    U.insert(k,(pop[j])[k])

            ''' Crossover '''
            n = int(urand() * dim)
            L = 0
            while 1:
                L = L + 1
                if urand() > cr or L > dim:
                    break

            for k in xrange(0, dim):
                for kk in (n, n + L):
                    if k != (kk % dim):
                        U.insert(k, (pop[j])[k])

            # bounds check
            for k in xrange(0, dim):
                while U[k] < Xl[k] or U[k] > Xu[k]:
                    if U[k] < Xl[k]:
                        U[k] = 2 * Xl[k] - U[k]
                    if U[k] > Xu[k]:
                        U[k] = 2 * Xu[k] - U[k]

            U.insert(dim, func(U))  # the last value in the list is the function value

            ''' Selection'''
            # Comparing the trial vector, 'U' and the old individual
            if U[dim] <= fvals[j]:
                for k in xrange(0, dim):
                    (pop[j])[k] = U[k]
                fvals.insert(j, func(pop[j]))


# Find the best obj. fn. value and write it to the file
# called every generation
def write_best():
    best_val = fvals[0]
    best_index = 0
    for i in xrange(0, NP):
        if fvals[i] < best_val:
            best_index = i
            best_val = fvals[i]

    # for i in xrange(0,dim):
    #     f_best.write(str((pop[best_index])[i]) + '\t')
    f_best.write(str(best_val))
    f_best.write('\n')


# Report the best pop and save the population
# statistics
def report():
    # Save the final population to the file
    f = open("final_pop.out", "w")
    f.write("Final population Data: Variable values || Objective function values\n")
    for i in xrange(0, NP):
        for j in xrange(0, dim):
            f.write(str((pop[i])[j]) + '\t')
        f.write('\t\t|| ')
        f.write(str(fvals[i]))
        f.write('\n')
    f.close()

    # Find the best individual and report
    best_val = fvals[0]
    best_index = 0
    for i in xrange(0, NP):
        if fvals[i] < best_val:
            best_index = i
            best_val = fvals[i]

    print
    "The best indvidual is", pop[best_index], ":: ", fvals[best_index]
    print
    "Total number of function evaluations:: ", num_fe


if __name__ == '__main__':
    print
    "****************************************"
    print
    "Simple Differential Evolution- Scheme DE1"
    print
    "*****************************************"
    setup()
    initpop()
    print
    "Evolution in progress.."
    evolve_de_rand_1()
    print
    print
    "Evolution Summary"
    print
    "*****************"
    report()
