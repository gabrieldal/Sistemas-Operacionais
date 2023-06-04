import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def calculatePi(q, min, max):
    # print (min, max)
    result = 0
    for i in range(min, max):
        numerator = (-1)**i
        denominator = 2*i + 1
        result += numerator/denominator
    q.put(result*4)


def singlecore(numIterations):
    result = 0
    t1 = time.time()
    #for i in range(MAX):
    q = mp.Queue()
    p = mp.Process(target=calculatePi, args=(q, 0, numIterations))
    p.start()
    result = q.get()
    t2 = time.time()
    print ('resultado siglecore = ', result)
    return (t2 - t1)

def multicore( numIterations, numThreads):
    result = 0
    tmp1 = time.time()
    numThreads = mp.cpu_count()
    q = mp.Queue()
    for i in range(numThreads):
        min_ = int (i*numIterations / numThreads)
        max_ = int ( (i+1)*numIterations / numThreads)
        p = mp.Process(target=calculatePi, args=(q, min_, max_))
        p.start()
    
    for i in range(numThreads):
        result += q.get()
    tmp2 = time.time()
    print ('Resultado multicore = ', result)
    return (tmp2 - tmp1)

if __name__ == '__main__':

    numRepetitions = int(input("Enter the number of repetitions: "))
    numIterations = int(input("Enter the number of iterations: "))
    numThreads = int(input("Enter the number of threads: "))

    ts = []
    tm = []
    tg = []
    tspeedup = []
    teff = []
    x = range (1, numRepetitions +1)
    for i in range (numRepetitions):
        ts.append(singlecore(numIterations))
        tm.append(multicore( numIterations, mp.cpu_count()))
        tg.append(ts[i] - tm[i])
        tspeedup.append(ts[i]/tm[i])
        teff.append(100 * tspeedup[i]/mp.cpu_count())
        print('singlecore = ', ts[i])
        print('multicore = ', tm[i])
        print('ganho = ', tg[i])
        print('speedup = ', tspeedup[i])
        print('eficiencia = ', teff[i])
        print('------------------------')
    plt.plot(x, ts, label='singlecore')
    plt.plot(x, tm, label='multicores')
    plt.xlabel('repetições')
    plt.ylabel('tempo (s)')
    plt.legend()
    plt.show()

    plt.plot(x, tg, label='ganho')
    plt.xlabel('repetições')
    plt.ylabel('tempo (s)')
    plt.legend()
    plt.show()

    plt.plot(x, tspeedup, label='speedup')
    plt.xlabel('repetições')
    plt.ylabel('number of times better than singlecore')
    plt.legend()
    plt.show()

    plt.plot(x, teff, label='eficiencia')
    plt.xlabel('repetições')
    plt.ylabel('Efficiency per core (%)')
    plt.legend()
    plt.show()



    
    print('media singlecore = ', sum(ts)/numRepetitions)
    print('media multicore = ', sum(tm)/numRepetitions)
    print('media ganho = ', sum(tg)/numRepetitions)
    print('media speedup = ', sum(tspeedup)/numRepetitions)
    print('media eficiencia = ', sum(teff)/numRepetitions)