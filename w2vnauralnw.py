import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import tensorflow as tf
import gensim.models


lemmatizer = WordNetLemmatizer()

n_nodes_hl1 = 400
n_nodes_hl2 = 400

n_classes = 2

batch_size = 32

total_batches = int(80000/batch_size)
hm_epochs = 10
x = tf.placeholder('float')
y = tf.placeholder('float')

hidden_1_layer = {'f_fum':n_nodes_hl1,
                  'weight':tf.Variable(tf.random_normal([100, n_nodes_hl1])),
                  'bias':tf.Variable(tf.random_normal([n_nodes_hl1]))}

hidden_2_layer = {'f_fum':n_nodes_hl2,
                  'weight':tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                  'bias':tf.Variable(tf.random_normal([n_nodes_hl2]))}

output_layer = {'f_fum':None,
                'weight':tf.Variable(tf.random_normal([n_nodes_hl2, n_classes])),
                'bias':tf.Variable(tf.random_normal([n_classes]))}

def neural_network_model(data):	
    l1 = tf.add(tf.matmul(data,hidden_1_layer['weight']), hidden_1_layer['bias'])
    l1 = tf.nn.relu(l1)
    l2 = tf.add(tf.matmul(l1,hidden_2_layer['weight']), hidden_2_layer['bias'])
    l2 = tf.nn.relu(l2)
    output = tf.matmul(l2,output_layer['weight']) + output_layer['bias']
    return output


saver = tf.train.Saver()
tf_log = 'tf.log'


def train_neural_network(x):
	prediction = neural_network_model(x)
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction,y))
	optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)
	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())
		try:
			epoch = int(open(tf_log,'r').read().split('\n')[-2])+1
			print('STARTING:',epoch)
		except:
			epoch = 1
		while epoch <= hm_epochs:
			if epoch != 1:
				saver.restore(sess,"model.ckpt")
			epoch_loss = 1
			with open('train_tweets_vecs',buffering=20000) as f:
				batch_x = []
				batch_y = []
				batches_run = 0
				for line in f:
					label_vec = eval(line.split(':::')[0])
					tweet_vec = eval(line.split(':::')[1])					
					batch_x.append(tweet_vec)
					batch_y.append(label_vec)
					if len(batch_x) >= batch_size:
						_, c = sess.run([optimizer, cost], feed_dict={x: np.array(batch_x),y: np.array(batch_y)})
						epoch_loss += c
						batch_x = []
						batch_y = []
						batches_run +=1
						print('Batch run:',batches_run,'/',total_batches,'| Epoch:',epoch,'| Batch Loss:',c,)
			saver.save(sess,"model.ckpt")
			print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',epoch_loss)
			with open(tf_log,'a') as f:
				f.write(str(epoch)+'\n')
			epoch +=1

#train_neural_network(x)

def test_naural_network():
	prediction = neural_network_model(x)
	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())
		for epoch in range(hm_epochs):
			try:
				saver.restore(sess,"model.ckpt")
			except Exception as e:
				print(str(e))
			epoch_loss = 0

		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
		feature_sets = []
		labels = []
		counter = 0
		with open('test_tweets_vecs', buffering=20000) as f:			
			for line in f:
				label_vec = eval(line.split(':::')[0])
				tweet_vec = eval(line.split(':::')[1])				
				test_x = list(tweet_vec)
				test_y = list(label_vec)
				feature_sets.append(test_x)
				labels.append(test_y)
				counter += 1
		print('Tested',counter,'samples.')
		test_x = np.array(feature_sets)
		test_y = np.array(labels)
		print('Accuracy:',accuracy.eval({x:test_x, y:test_y}))


test_naural_network()


def use_neural_network(input_data):	
    prediction = neural_network_model(x)        
    with tf.Session() as sess:    	
        sess.run(tf.initialize_all_variables())
        saver.restore(sess,"model.ckpt")
        model = gensim.models.Word2Vec.load('myw2vmodel')
        current_words = word_tokenize(input_data.lower())
        current_words = [lemmatizer.lemmatize(i) for i in current_words]
        sum = np.zeros(100)
        for word in current_words:
        	if word in model:
        		sum += model[word]
        	sum = sum/100
        features = np.array(list(sum))
        arr=prediction.eval(feed_dict={x:[features]})[0]
        print(arr)
        if arr[0]>arr[1] :
        	print('non english speaking country',input_data)
        else:
        	print('english speaking country',input_data)

#use_neural_network("http ")