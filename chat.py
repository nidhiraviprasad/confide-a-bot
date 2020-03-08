import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import pickle
import json


class chatBot():

	model = None
	words = None
	labels = None
	training = None
	output = None
	data = None

	def __init__(self):
		with open('intents.json') as file:
			self.data = json.load(file)

		try:
			#opens existing training file
			with open("data.pickle", "rb") as f:
				self.words, self.labels, self.training, self.output = pickle.load(f)

		except:
			#retrains model
			self.words = []
			self.labels = []
			docs_x = []
			docs_y = []

			#scan in json file

			for intent in self.data["intents"]:
				for pattern in intent["patterns"]:
					wrds = nltk.word_tokenize(pattern)
					self.words.extend(wrds)
					docs_x.append(wrds)
					docs_y.append(intent["tag"])

				if intent["tag"] not in self.labels:
					self.labels.append(intent["tag"])

			#finds 'root' word from given word

			word = [stemmer.stem(w.lower()) for w in self.words if w != "?"]
			self.words = sorted(list(set(self.words)))

			self.labels = sorted(self.labels)

			self.training = []
			self.output = []

			out_empty = [0 for _ in range(len(self.labels))]

			for x, doc in enumerate(docs_x):
				bag = []
				wrds = [stemmer.stem(w.lower()) for w in doc]

				for w in self.words:
					if w in wrds:
						bag.append(1)
					else:
						bag.append(0)

				output_row = out_empty[:]
				output_row[self.labels.index(docs_y[x])] = 1

				self.training.append(bag)
				self.output.append(output_row)


			self.training = numpy.array(self.training)
			self.output = numpy.array(self.output)

			with open("data.pickle", "wb") as f:
				pickle.dump((self.words, self.labels, self.training, self.output), f)

		#interpreting model

		tensorflow.reset_default_graph()

		net = tflearn.input_data(shape=[None, len(self.training[0])])
		net = tflearn.fully_connected(net, 10)
		net = tflearn.fully_connected(net, 10)
		net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
		net = tflearn.regression(net)

		self.model = tflearn.DNN(net)

		try:
			self.model.load("model.tflearn")
		except:
			self.model.fit(self.training, self.output, n_epoch=2000, batch_size=8, show_metric=True)
			self.model.save("model.tflearn")


	#converting input of user into processable 'bag' of words
	def bag_of_words(self, s):
		bag = [0 for _ in range(len(self.words))]

		s_words = nltk.word_tokenize(s)
		s_words = [stemmer.stem(word.lower()) for word in s_words]

		for se in s_words:
			for i, w in enumerate(self.words):
				if w == se:
					bag[i] = 1

		return numpy.array(bag)

	#talking to the model!!!!!
	def chat(self, text):
		inp = text
		if inp.lower() == "bye":
			return "I'm always here if you need me!"

		results = self.model.predict([self.bag_of_words(inp)])
		results_index = numpy.argmax(results)
		tag = self.labels[results_index]

		responses = []

		for tg in self.data["intents"]:
			if tg['tag'] == tag:
				responses = tg['responses']

		return random.choice(responses)

