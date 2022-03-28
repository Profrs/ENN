from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import g 

import neuroid
import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index_copy.html")

def set_umbr(umbr):
    g.umbr = umbr 
    return g.umbr

def set_kr(kr):
    g.kr = kr 
    return g.kr

def set_beta(beta):
    g.beta = beta
    return beta

def set_maxcount(maxcount):
    g.maxcount = maxcount
    return maxcount

@app.route("/index_copy", methods=["POST"])
def input():
    umbr = float(request.form["umbrValue"])
    set_umbr(umbr)
    beta = float(request.form["BetaValue"])
    set_beta(beta)
    kr = float(request.form["KrValue"])
    set_kr(kr)
    maxcount = int(request.form["maxcountValue"])
    set_maxcount(maxcount)
    #result = (g.umbr, g.beta, g.kr, g.maxcount)
    result = neuroid.run(umbr, beta, kr, maxcount)
    
    return render_template('index_copy.html', results=result)
    #return redirect('neuroid_group.html')

@app.route('/neuroid_group')
def neuroid_group():
    return render_template("neuroid_group.html")

@app.route("/neuroid_group.html", methods=["POST"])
def neuroid_group_output():
    result = []
    inputs = [round(i / 1000, 3)for i in range(1001)] + [round(i / 1000, 3) for i in reversed(range(1000))]
    weights = [0 for i in range(len(inputs))]
    neuroid_1 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2, maxcount=24, t=1)
    neuroid_1_output = neuroid_1.run_neuroid(inputs = inputs, weights = weights)
    result.extend(neuroid_1_output)
    result.append('@')
    weights = [0 for i in range(len(neuroid_1_output))]
    neuroid2 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2, maxcount=24, t=1)
    neuroid_2_output = neuroid2.run_neuroid(inputs = neuroid_1_output, weights = weights)
    result.extend(neuroid_2_output)
    result.append('@')
    weights = [0 for i in range(len(neuroid_2_output))]
    neuroid3 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2, maxcount=24, t=1)
    neuroid_3_output = neuroid3.run_neuroid(inputs = neuroid_2_output, weights = weights)
    result.extend(neuroid_3_output)
    #result = neuroid.run(umbr, beta, kr, maxcount)
    #result = neuroid.run(umbr, beta, kr, maxcount)

    return render_template('neuroid_group.html', results=result)


@app.route('/neuroid_group_two_inputs')
def neuroid_group_two_inputs():
    return render_template("neuroid_group_two_inputs.html")

@app.route('/neuroid_group_two_inputs.html', methods = ["POST"])    
def neuroid_group_two_inputs_output():
    result = []
    inputs = [1-round(i**2 / 1000**2, 3) for i in reversed(range(1000))] + [1-round(i**2 /1000**2, 3) for i in range(1001)]
    weights = [0 for i in range(len(inputs))]
    neuroid_1 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2, maxcount=24, t=1)
    neuroid_1_output = neuroid_1.run_neuroid(inputs = inputs, weights = weights)
    result.extend(neuroid_1_output)
    result.append('@')
    inputs2 = [0 for i in range(1)] + [0.5 for i in range(999)] + [0.5 for i in range(1000)] + [0 for i in range(1)]
    weights = [0 for i in range(len(inputs2))]
    neuroid2 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2, maxcount=24, t=1)
    neuroid_2_output = neuroid2.run_neuroid(inputs = inputs2, weights = weights)
    result.extend(neuroid_2_output)
    result.append('@')
    inputs3 = [x - y for (x,y) in zip(neuroid_1_output, neuroid_2_output)] 
    weights = [0 for i in range(len(inputs3))]
    neuroid3 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2, maxcount=24, t=1)
    neuroid_3_output = neuroid3.run_neuroid(inputs = inputs3, weights = weights)
    result.extend(neuroid_3_output)
    #result = neuroid.run(umbr, beta, kr, maxcount)
    #result = neuroid.run(umbr, beta, kr, maxcount)

    return render_template('neuroid_group_two_inputs.html', results=result)


@app.route('/neuroid_circle')
def neuroid_circle():
    return render_template("neuroid_circle.html")

@app.route('/neuroid_circle.html', methods = ["POST"])
def neuroid_circle_output():
    result = []
    neuroid_1_output = []
    neuroid_2_output = []
    neuroid_3_output = []

    #inputs = [round(i / 1000, 3) for i in range(1001)] + [round(i / 1000, 3) for i in reversed(range(1000))]
    inputs = [0 for i in range(1)] + [0.7 for i in range(998)] + [0.7 for i in range(1000)] + [0 for i in range(1)]
    weights = [0 for i in range(len(inputs))]

    inputs_maintained = [0 for i in range(1)] + [0.7 for i in range(998)] + [0.7 for i in range(1000)] + [0 for i in range(1)]
    neuroid_1 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2.1, maxcount=24, t=1)
    neuroid2 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2.1, maxcount=24, t=1)
    neuroid3 = neuroid.Neuroid(umbr=0.1, beta=1.25, kr=2.1, maxcount=24, t=1)

    for i in range(0, 10):
        neuroid_1_output = neuroid_1.run_neuroid(inputs=inputs, weights=weights)

        weights = [0 for i in range(len(neuroid_1_output))]

        neuroid_2_output = neuroid2.run_neuroid(inputs=neuroid_1_output, weights=weights)

        weights = [0 for i in range(len(neuroid_2_output))]

        neuroid_3_output = neuroid3.run_neuroid(inputs=neuroid_2_output, weights=weights)

        inputs = [x - y for (x, y) in zip(inputs_maintained, neuroid_3_output)]
        weights = [0 for i in range(len(inputs))]

    result.extend(neuroid_1_output)
    result.append('@')
    result.extend(neuroid_2_output)
    result.append('@')
    result.extend(neuroid_3_output)
    #result = neuroid.run(umbr, beta, kr, maxcount)
    #result = neuroid.run(umbr, beta, kr, maxcount)

    return render_template('neuroid_circle.html', results=result)