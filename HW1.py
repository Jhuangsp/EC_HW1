import random as rd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Evolutionary Computation HW1', fromfile_prefix_chars='@')

# Data parameter
parser.add_argument('-p', '--POPULATION_SIZE', type=int, default=500,
                    help='population size')
parser.add_argument('-b', '--BITS', type=int, default=60,
                    help='number of bits')
parser.add_argument('-t', '--TERMINATION', type=int, default=200,
                    help='termination rounds')


parser.add_argument('-r', '--repeat', type=int, default=1,
                    help='repeat n rounds')
parser.add_argument('-s', '--selector', type=str, default='r',
                    help='choose selector RouletteWheel or Tournament [r|t]')
parser.add_argument('-f', '--fitnessBias', type=int, default=0,
                    help='fitness bias')
parser.add_argument('--debug', action="store_true",
                    help='DEBUG')
args = parser.parse_args()
debug = args.debug

def getFitness(pop, bias=0):
    return pop.sum(axis=1) + bias

def rouletteWheelSelect(pop, nsize, replace=True, fBias=0):
    f = getFitness(pop, bias=fBias)
    p = f / f.sum()
    d = np.random.choice(len(p), nsize//2, p=p)
    m = np.random.choice(len(p), nsize//2, p=p)
    if not replace:
        pass
    return d, m

def tournamentSelect(pop, nsize, tournamentSize=2, replace=True, fBias=0):
    f = getFitness(pop, bias=fBias)
    dm = np.random.choice(len(f), (nsize, tournamentSize))
    if debug:
        print(f)
        print(dm)
        print(np.arange(len(f)))
        print(np.argmax(f[dm], axis=1))
    dm = dm[(np.arange(len(f)),np.argmax(f[dm], axis=1))].reshape(-1, 2)
    if not replace:
        pass
    return dm[:,0], dm[:,1]

def crossover(u, v, nmax, nsize, ncut=1, pc=1.0):
    cuts = np.sort(np.random.randint(nmax, size=(nsize//2, ncut), dtype=int))
    u1 = u.copy()
    v1 = v.copy()
    if debug:
        print('cut', cuts)
    for n in range(nsize//2):
        for c in cuts[n]:
            u1[n] = np.concatenate((u[n,:c], v[n,c:]), 0)
            v1[n] = np.concatenate((v[n,:c], u[n,c:]), 0)
    return u1, v1

def main():
    POPULATION_SIZE = args.POPULATION_SIZE
    BITS = args.BITS
    TERMINATION = args.TERMINATION

    sumBest = list()
    
    for r in range(args.repeat):
        pop = np.random.randint(2, size=(POPULATION_SIZE,BITS), dtype=int)
        if debug:
            print('INIT')
            print(pop)
            print(pop.sum(1))

        # best record
        best = list()
        best.append(pop[np.argmax(pop.sum(axis=1))])
        print('Best@000:', best[0].sum())
        if debug:
            print()

        # Main loop
        for gen in range(1,TERMINATION):
            # Parent selection
            if args.selector == 'r':
                d, m = rouletteWheelSelect(pop, POPULATION_SIZE, fBias=args.fitnessBias)
            elif args.selector == 't':
                d, m = tournamentSelect(pop, POPULATION_SIZE, fBias=args.fitnessBias)
            else:
                return
            dads = pop[d]
            moms = pop[m]
            if debug:
                print('Dads', d)
                print(dads)
                print('Moms', m)
                print(moms)
                print(dads.sum(axis=1), moms.sum(axis=1))
                print()

            # Recombination
            sons, daus = crossover(dads, moms, BITS, POPULATION_SIZE)
            if debug:
                print(sons)
                print(daus)
                print(sons.sum(axis=1), daus.sum(axis=1))

            # Generational model
            pop = np.concatenate((sons,daus), axis=0)
            best.append(pop[np.argmax(pop.sum(axis=1))])
            print('Best@{:03d}:'.format(gen), best[gen].sum())
            if debug:
                print()
        best = np.array(best).sum(axis=1)
        # plt.plot(np.arange(0,len(best), dtype=int), best)
        # plt.show()
        sumBest.append(best)
    sumBest = np.array(sumBest).sum(axis=0) / args.repeat
    plt.plot(np.arange(0,len(sumBest), dtype=int), sumBest)
    plt.show()
    pass

if __name__ == '__main__':
    main()