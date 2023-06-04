import sys
import multiprocessing as mp
import time
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton


def calculatePi(q, min_, max_):
    result = 0
    for i in range(min_, max_):
        numerator = (-1) ** i
        denominator = 2 * i + 1
        result += numerator / denominator
    q.put(result * 4)


class PiCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pi Calculator")
        self.setGeometry(200, 200, 400, 300)
        self.initUI()

    def initUI(self):
        self.iterations_label = QLabel("Number of Iterations:")
        self.iterations_input = QLineEdit()
        self.threads_label = QLabel("Number of Threads:")
        self.threads_input = QLineEdit()
        self.repetitions_label = QLabel("Number of Repetitions:")
        self.repetitions_input = QLineEdit()

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.iterations_label)
        self.layout.addWidget(self.iterations_input)
        self.layout.addWidget(self.threads_label)
        self.layout.addWidget(self.threads_input)
        self.layout.addWidget(self.repetitions_label)
        self.layout.addWidget(self.repetitions_input)
        self.layout.addWidget(self.calculate_button)

        self.setLayout(self.layout)

    def calculate(self):
        numIterations = int(self.iterations_input.text())
        numThreads = int(self.threads_input.text())
        numRepetitions = int(self.repetitions_input.text())

        ts = []
        tm = []
        tg = []
        tspeedup = []
        teff = []
        x = range(1, numRepetitions + 1)

        for i in range(numRepetitions):
            ts.append(self.singlecore(numIterations))
            tm.append(self.multicore(numIterations, numThreads))
            tg.append(ts[i] - tm[i])
            tspeedup.append(ts[i] / tm[i])
            teff.append(100 * tspeedup[i] / numThreads)
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

        print('media singlecore = ', sum(ts) / numRepetitions)
        print('media multicore = ', sum(tm) / numRepetitions)
        print('media ganho = ', sum(tg) / numRepetitions)
        print('media speedup = ', sum(tspeedup) / numRepetitions)
        print('media eficiencia = ', sum(teff) / numRepetitions)

    def calculatePi(self, q, min_, max_):
        result = 0
        for i in range(min_, max_):
            numerator = (-1) ** i
            denominator = 2 * i + 1
            result += numerator / denominator
        q.put(result * 4)

    def singlecore(self, numIterations):
        result = 0
        t1 = time.time()
        q = mp.Queue()
        calculatePi(q, 0, numIterations)
        result = q.get()
        t2 = time.time()
        print('resultado singlecore = ', result)
        return (t2 - t1)

    def multicore(self, numIterations, numThreads):
        result = 0
        tmp1 = time.time()
        q = mp.Queue()
        for i in range(numThreads):
            min_ = int(i * numIterations / numThreads)
            max_ = int((i + 1) * numIterations / numThreads)
            p = mp.Process(target=calculatePi, args=(q, min_, max_))
            p.start()

        for i in range(numThreads):
            result += q.get()
        tmp2 = time.time()
        print('Resultado multicore = ', result)
        return (tmp2 - tmp1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PiCalculator()
    window.show()
    sys.exit(app.exec_())
