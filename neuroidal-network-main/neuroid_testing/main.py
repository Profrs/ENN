from neuroid import Neuroid
import matplotlib.pyplot as plt


def main():
    inputs = [round(i / 1000, 3)for i in range(1001)] + [round(i / 1000, 3) for i in reversed(range(1000))]
    weights = [0 for i in range(2001)]

    neuroid = Neuroid(umbr=0.1, beta=1.25, kr=2, maxcount=50, t=1, log=False)
    output = neuroid.run_neuroid(inputs, weights)

    plt.plot(output)
    plt.show()


if __name__ == "__main__":
    main()
