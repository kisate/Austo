import tensorflow as tf
import numpy as np
import pickle
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder, StandardScaler

with open('train/data/config.json') as f:
    config = json.load(f)


n_features = config['n_features']
n_classes = config['n_classes']

n_neurons_h = config['neurons']
learning_rate = config['learning_rate']
training_epochs = config['epochs']

path_to_model = config['path_to_model']
path_to_events = config['path_to_events']
path_to_data = config['path_to_data']
train_dir = config['train_dir']
batchsize = config['batchsize']

with open(path_to_data, 'rb') as f:
    data = pickle.load(f)

features = data[0]
labels = data[1]

le=LabelBinarizer()
labels=le.fit_transform(labels)

for l in labels : 
    print (l)

#splitting data to train and test split
tr_features,ts_features,tr_labels,ts_labels=train_test_split(features,labels,test_size=0.7,random_state=42)


sess = tf.Session()

saver = tf.train.import_meta_graph(train_dir + 'model.ckpt.meta')
saver.restore(sess, tf.train.latest_checkpoint(train_dir))

graph = tf.get_default_graph()

X = graph.get_tensor_by_name('features:0')
Y = graph.get_tensor_by_name('labels:0')

keep_prob = graph.get_tensor_by_name('drop_prob:0')

W1 = graph.get_tensor_by_name(name='weights1:0')
b1 = graph.get_tensor_by_name(name='biases1:0')

y1 = graph.get_tensor_by_name('activationLayer1:0')

drop_out_layer1 = tf.nn.dropout(y1, keep_prob)

Wo = graph.get_tensor_by_name(name='weightsOut:0')
bo = graph.get_tensor_by_name(name='biasesOut:0')

a = graph.get_tensor_by_name(name='activationOutputLayer:0')

current_step = graph.get_tensor_by_name(name='currentStep:0')

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
    
    accuracy = graph.get_tensor_by_name(name="Accuracy:0")
    tf.summary.scalar('Accuracy', accuracy)


writer = tf.summary.FileWriter(path_to_events)
writer.add_graph(graph)
merged_summary = tf.summary.merge_all()



# training loop over the number of epoches
for epoch in range(sess.run(current_step), training_epochs):
    for i in range(len(tr_features)):

        start=i
        end=i+batchsize
        x_batch=tr_features[start:end]
        y_batch=tr_labels[start:end]

        # print(x_batch)

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
    op = tf.assign(current_step, epoch)
    sess.run(op)
    
    if (epoch % 30 == 29) :
        save_path = saver.save(sess, train_dir + "model.ckpt", global_step=epoch)
        print("Model saved in path: %s" % save_path)

print(y_pred, y_true)

sess.close()