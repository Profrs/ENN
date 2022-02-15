from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import g 

import neuroid

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
