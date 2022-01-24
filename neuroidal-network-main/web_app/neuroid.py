class Neuroid:
    def __init__(self, umbr, beta, kr, maxcount, t, log=False):
        self.log = log

        self.umbr = umbr
        self.beta = beta
        self.kr = kr
        self.maxcount = maxcount
        self.t = t

        self.count1 = 0
        self.count2 = 0

        self.y = 0
        self.nt_out = 0
        self.time = 0

        self.sum_stream = []
        self.count1_stream = []
        self.count2_stream = []
        self.y_stream = []
        self.nt_out_stream = []

    def run_comparator(self, inputs, weights):
        input_sum = round(sum(inputs), 3)

        if input_sum > self.umbr:
            if self.count1 > self.beta / (input_sum - self.umbr):
                self.count1 = 0
            else:
                self.count1 += 1
        else:
            self.count1 = 0

        if self.log:
            self.sum_stream.append(input_sum)
            self.count1_stream.append(self.count1)

    def run_freq_modulator(self):
        if self.count1 == 1:
            self.y = 1
        else:
            self.y = 0

        if self.log:
            self.y_stream.append(self.y)

    def run_freq_demodulator(self):
        if self.y == 1:
            self.nt_out = self.kr / self.count2
            self.count2 = 0
        else:
            self.count2 += 1

        if self.count2 > self.maxcount:
            self.nt_out = 0

        self.nt_out_stream.append(self.nt_out)

        if self.log:
            self.count2_stream.append(self.count2)

    def run_neuroid(self, inputs, weights):
        if len(inputs) != len(weights):
            raise Exception("Size of inputs and size of weights must be the same!")

        for i in range(len(weights) - self.t + 1):
            self.run_comparator(inputs[i:(i + self.t)], weights[i:(i + self.t)])
            self.run_freq_modulator()
            self.run_freq_demodulator()
            self.time += 1

            if self.log:
                print("======= Time", self.time, "=======")
                print("nt_out =", self.nt_out)
                print("y =", self.y)
                print("count1 =", self.count1)
                print("count2 =", self.count2)
                print()

        return self.nt_out_stream


def run(umbr, beta, kr, maxcount, log=False):
    inputs = [round(i / 1000, 3)for i in range(1001)] + [round(i / 1000, 3) for i in reversed(range(1000))]
    weights = [0 for i in range(2001)]

    neuroid = Neuroid(umbr=umbr, beta=beta, kr=kr, maxcount=maxcount, t=1, log=log)
    neuroid.run_neuroid(inputs, weights)

    return {"output": neuroid.nt_out_stream}
