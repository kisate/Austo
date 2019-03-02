import tensorflow as tf
import numpy as np
import pickle
import json


with open('train/data/config.json') as f:
    config = json.load(f)


n_features = config['n_features']
n_classes = config['n_classes']

n_neurons_h = config['neurons']
learning_rate = config['learning_rate']

path_to_model = config['path_to_model']

X = tf.placeholder(tf.float32, [None, n_features], name='features')
Y = tf.placeholder(tf.float32, [None, n_classes], name='labels')

keep_prob=tf.placeholder(tf.float32,name='drop_prob')

W1 = tf.Variable(tf.truncated_normal([n_features, n_neurons_h], mean=0, stddev=1 / np.sqrt(n_features)), name='weights1')
b1 = tf.Variable(tf.truncated_normal([n_neurons_h],mean=0, stddev=1 / np.sqrt(n_features)), name='biases1')

y1 = tf.nn.tanh((tf.matmul(X, W1)+b1), name='activationLayer1')

drop_out_layer1 = tf.nn.dropout(y1, keep_prob)

Wo = tf.Variable(tf.random_normal([n_neurons_h, n_classes], mean=0, stddev=1/np.sqrt(n_features)), name='weightsOut')
bo = tf.Variable(tf.random_normal([n_classes], mean=0, stddev=1/np.sqrt(n_features)), name='biasesOut')

a = tf.nn.softmax((tf.matmul(y1, Wo) + bo), name='activationOutputLayer')

cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(a),reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
current_step = tf.Variable(0, name='currentStep')

#compare predicted value from network with the expected value/target
correct_prediction = tf.equal(tf.argmax(a, 1), tf.argmax(Y, 1))
#accuracy determination
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="Accuracy")


# name scope for the cost function for more clarity on tensorboard
with tf.name_scope('Cost'):
    # cost function(cross entropy)
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(a),reduction_indices=[1]))#reduction indices=1 means row wise mean
    #optimization function
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
    # scalar summary for plotting cost variation againt epoches

# name scope for the accuracy for more clarity on tensorboard
with tf.name_scope('Accuracy'):
    # compare predicted value from network with the expected value/target
    correct_prediction = tf.equal(tf.argmax(a, 1), tf.argmax(Y, 1))
    # accuracy determination
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="Accuracy")
    # scalar summary for plotting accuracy variation against epoches


# initialization of all variables
initial = tf.global_variables_initializer()

saver = tf.train.Saver()
#creating a session
with tf.Session() as sess:
    sess.run(initial)
    save_path = saver.save(sess, path_to_model)
    print("Model saved in path: %s" % save_path)
    
    # writer = tf.summary.FileWriter("/home/dumtrii/Documents/Austro/train")
    # writer.add_graph(sess.graph)
    # merged_summary = tf.summary.merge_all()


    
#     # training loop over the number of epoches
#     batchsize=1
#     for epoch in range(training_epochs):
#         for i in range(len(tr_features)):

#             start=i
#             end=i+batchsize
#             x_batch=tr_features[start:end]
#             y_batch=tr_labels[start:end]
            
#             # feeding training data/examples
#             sess.run(train_step, feed_dict={X:x_batch , Y:y_batch,keep_prob:0.5})
#             i+=batchsize
#         # feeding testing data to determine model accuracy
#         y_pred = sess.run(tf.argmax(a, 1), feed_dict={X: ts_features,keep_prob:1.0})
#         y_true = sess.run(tf.argmax(ts_labels, 1))


#         summary, acc = sess.run([merged_summary, accuracy], feed_dict={X: ts_features, Y: ts_labels,keep_prob:1.0})
#         # write results to summary file
#         # print accuracy for each epoch
#         print('epoch',epoch, acc)
#         print ('---------------')
#         save_path = saver.save(sess, "/home/dumtrii/Documents/Austro/train/model/model.ckpt")
#         print("Model saved in path: %s" % save_path)

# print(y_pred, y_true)