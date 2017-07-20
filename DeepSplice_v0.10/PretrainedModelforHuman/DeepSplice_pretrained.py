from __future__ import print_function
import tensorflow as tf
import numpy as np
import random
import loadData
import sys

Input = sys.argv[1]
Output = sys.argv[2]

dataSet = loadData.load_csv_with_header(filename=Input, features_dtype=np.float)
X = dataSet.data

# Network Parameters
n_input = X.shape[1] # Splice junction data input
n_classes = 2 # Splice junction total classes (positive or negative)

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) #dropout (keep probability)

def conv2d(x, W, b, strides=1):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)

# Create model
def conv_net(x, weights, biases, dropout):
    # Reshape input data
    x = tf.reshape(x, shape=[-1, 120, 1, 4])
    # Convolution Layer
    conv1 = conv2d(x, weights['wc1'], biases['bc1'])
    # Convolution Layer
    conv2 = conv2d(conv1, weights['wc2'], biases['bc2'])
    # Fully connected layer
    # Reshape conv2 output to fit fully connected layer input
    fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
    fc1 = tf.nn.relu(fc1)
    # Apply Dropout
    fc1 = tf.nn.dropout(fc1, dropout)
    # Output, class prediction
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
    return out

# Store layers weight & bias
weights = {
    'wc1': tf.Variable(tf.random_normal([3, 1, 4, 8], 0, 0.1)),
    'wc2': tf.Variable(tf.random_normal([3, 1, 8, 16], 0, 0.1)),
    'wd1': tf.Variable(tf.random_normal([120*1*16, 32], 0, 0.1)),
    'out': tf.Variable(tf.random_normal([32, n_classes], 0, 0.1))
}

biases = {
    'bc1': tf.Variable(tf.random_normal([8], 0, 0.1)),
    'bc2': tf.Variable(tf.random_normal([16], 0, 0.1)),
    'bd1': tf.Variable(tf.random_normal([32], 0, 0.1)),
    'out': tf.Variable(tf.random_normal([n_classes], 0, 0.1))
}

# Construct model
pred = conv_net(x, weights, biases, keep_prob)
result = tf.argmax(pred,1)

# Launch the graph
with tf.Session() as sess:
    saver = tf.train.Saver()
    saver.restore(sess, "./model.ckpt")
    Y, Y_raw = sess.run([result, pred], feed_dict={x: X, keep_prob: 1.})
    np.savetxt(Output + "predictionResult.txt", Y)
    np.savetxt(Output + "additionalInfo.txt", Y_raw[:,1])