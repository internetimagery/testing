# basic testing tensorflow
from __future__ import print_function
import tensorflow as tf

def main():
    # Placeholders
    A = tf.placeholder("float")
    B = tf.placeholder("float")

    # Variables
    w = tf.Variable(1.0)

    # Equation
    z = A + w

    # Cost
    cost = (B - z) ** 2

    # Trainer
    trainer = tf.train.AdamOptimizer(0.01).minimize(cost)

    # Train
    with tf.Session() as s:
        tf.global_variables_initializer().run()
        for _ in range(100):
            for i in range(10):
                val = i + 3
                s.run(trainer, feed_dict={A:i, B:val})

        print(s.run(w))

if __name__ == '__main__':
    main()
