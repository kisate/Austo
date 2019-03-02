import tensorflow as tf
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder, StandardScaler

with open('train/data/data.out', 'rb') as f:
    data = pickle.load(f)

features = data[0]
labels = data[1]

le=LabelBinarizer()
labels=le.fit_transform(labels)

print(labels)

scale=StandardScaler()
norm_features=scale.fit_transform(features)

print(norm_features)

#splitting data to train and test split
tr_features,ts_features,tr_labels,ts_labels=train_test_split(norm_features,labels,test_size=0.8,random_state=42)

n_features = 12
n_classes = 14

training_epochs = 1000
n_neurons_h = 60
learning_rate = 0.001

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

#compare predicted value from network with the expected value/target
correct_prediction = tf.equal(tf.argmax(a, 1), tf.argmax(Y, 1))
#accuracy determination
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="Accuracy")

#compare predicted value from network with the expected value/target
correct_prediction = tf.equal(tf.argmax(a, 1), tf.argmax(Y, 1))
#accuracy determination
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="Accuracy")

tf.summary.histogram("weights1", W1)
tf.summary.histogram("biases1", b1)
tf.summary.histogram("weightsOut", Wo)
tf.summary.histogram("biasesOut", bo)

# name scope for the cost function for more clarity on tensorboard
with tf.name_scope('Cost'):
    # cost function(cross entropy)
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(a),reduction_indices=[1]))#reduction indices=1 means row wise mean
    #optimization function
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
    # scalar summary for plotting cost variation againt epoches
    tf.summary.scalar('Cost', cross_entropy)

# name scope for the accuracy for more clarity on tensorboard
with tf.name_scope('Accuracy'):
    # compare predicted value from network with the expected value/target
    correct_prediction = tf.equal(tf.argmax(a, 1), tf.argmax(Y, 1))
    # accuracy determination
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="Accuracy")
    # scalar summary for plotting accuracy variation against epoches
tf.summary.scalar('Accuracy', accuracy)


# initialization of all variables
initial = tf.global_variables_initializer()

saver = tf.train.Saver()

#creating a session
with tf.Session() as sess:
    sess.run(initial)
    writer = tf.summary.FileWriter("/home/dumtrii/Documents/Austro/train")
    writer.add_graph(sess.graph)
    merged_summary = tf.summary.merge_all()

    
    # training loop over the number of epoches
    batchsize=1
    for epoch in range(training_epochs):
        for i in range(len(tr_features)):

            start=i
            end=i+batchsize
            x_batch=tr_features[start:end]
            y_batch=tr_labels[start:end]
            
            print(x_batch)

            # feeding training data/examples
            sess.run(train_step, feed_dict={X:x_batch , Y:y_batch,keep_prob:0.5})
            i+=batchsize
        # feeding testing data to determine model accuracy
        y_pred = sess.run(tf.argmax(a, 1), feed_dict={X: ts_features,keep_prob:1.0})
        y_true = sess.run(tf.argmax(ts_labels, 1))


        summary, acc = sess.run([merged_summary, accuracy], feed_dict={X: ts_features, Y: ts_labels,keep_prob:1.0})
        # write results to summary file
        writer.add_summary(summary, epoch)
        # print accuracy for each epoch
        print('epoch',epoch, acc)
        print ('---------------')
        save_path = saver.save(sess, "/home/dumtrii/Documents/Austro/train/tmp/model.ckpt")
        print("Model saved in path: %s" % save_path)

print(y_pred, y_true)