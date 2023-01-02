import joblib
import numpy as np

my_model = joblib.load("model.joblib")

print(my_model.predict(np.array([4,2,2,2]).reshape(1,-1)))

from flask import Flask

app = Flask(__name__)

@app.route("/<my_input>")
def hello_world(my_input):

    input = [int(x) for x in my_input]
    my_model = joblib.load("model.joblib")

    my_flower = f"{my_model.predict(np.array(input).reshape(1, -1))}"

    return f"<p>The flower with sepal {input} is flower number {my_flower}</p>"