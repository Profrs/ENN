from flask import Flask
from flask import render_template
from flask import request

import neuroid

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/input", methods=["POST"])
def input():
    umbr = float(request.form["umbrValue"])
    beta = float(request.form["BetaValue"])
    kr = float(request.form["KrValue"])
    maxcount = int(request.form["maxcountValue"])

    result = neuroid.run(umbr, beta, kr, maxcount)

    return render_template('index.html', results=result)
