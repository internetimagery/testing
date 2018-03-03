# learning estimators
from __future__ import print_function
import tensorflow as tf
import os.path
import shutil
import os
import random

# https://stackoverflow.com/questions/47068709/your-cpu-supports-instructions-that-this-tensorflow-binary-was-not-compiled-to-u
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # hide warning

temp = os.path.join(os.path.dirname(__file__), "temp_brain")
if os.path.exists(temp):
    shutil.rmtree(temp)
os.mkdir(temp)

def input_fn():
    # Generate data
    vals = [float(random.randint(0,9)) for _ in range(500)]
    compare = [a+3 for a in vals]
    return {"train": vals}, compare

def predict_fn():
    return {"train": [5]}

def main():


    # features
    train = tf.feature_column.numeric_column("train")

    # estimator = tf.estimator.LinearRegressor(
    #     feature_columns=[train],
    #     model_dir=temp)

    estimator = tf.estimator.DNNRegressor(
        feature_columns=[train],
        hidden_units=[1024,512,256],
        model_dir=temp)

    estimator.train(input_fn=input_fn, steps=1000)
    # print({a: estimator.get_variable_value(a) for a in estimator.get_variable_names()})
    print("evaluate", estimator.evaluate(input_fn=input_fn, steps=100))
    print("expected 3, got", estimator.predict(input_fn=predict_fn).__next__()["predictions"][0])


if __name__ == '__main__':
    main()
