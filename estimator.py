# learning estimators
from __future__ import print_function
import tensorflow as tf
import numpy
import os.path
import os
import random

# https://stackoverflow.com/questions/47068709/your-cpu-supports-instructions-that-this-tensorflow-binary-was-not-compiled-to-u
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # hide warning

temp = os.path.join(os.path.dirname(__file__), "temp")

def input_fn():
    # Generate data
    # return {"train": numpy.array/([a for a in range(100)])}, numpy.array([a+3 for a in range(100)])
    vals = [float(random.randint(0,9)) for _ in range(200)]
    compare = [a+3 for a in vals]
    return {"train": vals}, compare

def eval_fn():
    return {"train": [5]}, [5+3]

def predict_fn():
    return {"train": [5]}

def main():


    # features
    train = tf.feature_column.numeric_column("train")

    estimator = tf.estimator.LinearRegressor(
        feature_columns=[train],
        model_dir=temp)

    estimator.train(input_fn=input_fn, steps=1000)
    # print({a: estimator.get_variable_value(a) for a in estimator.get_variable_names()})
    print("evaluate", estimator.evaluate(input_fn=input_fn, steps=100))
    print("predict", estimator.predict(input_fn=predict_fn).__next__())


if __name__ == '__main__':
    main()
