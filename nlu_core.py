from gensim import corpora, models, similarities
import nltk
from nltk.corpus import brown
import pymystem3
import time
import re
import logging
import os
import tempfile

lda = models.LdaModel.load('model.lda')
index = similarities.MatrixSimilarity.load('sims.sims')

TEMP_FOLDER = tempfile.gettempdir()
dictionary = corpora.Dictionary.load(os.path.join(TEMP_FOLDER, 'deerwester.dict'))

import pandas as pd
import numpy as np
dfr = pd.read_csv('vk.csv')

def utterance_to_bow(utterance):
	stop_words= nltk.corpus.stopwords.words('russian')
	stop_word="пожалуйста здоавствуйте"
	for i in stop_words:
		stop_word=  stop_word+" "+i
	stoplist = stop_word
	
	utterance=utterance.lower()
	utterance=utterance.replace("тк","").replace("сбербанк","банк").replace("сбер","банк").replace("сбербанка","банк").replace("банка","банк")
	utterance=re.sub(r'[^а-яА-Я ]+', '',utterance)
	tokens = [word for word in str(utterance).split() if word not in stoplist]
	
	mystem = pymystem3.Mystem()
	utterance = [mystem.lemmatize(token)[0] for token in tokens]
	
	
	bow=dictionary.doc2bow(utterance)
	return bow

def utterance_to_result(utterance):
	result=""
	
	vec_lda = lda[utterance_to_bow(utterance)]
	
	
	
	
	
	sims = index[vec_lda]
	sims = sorted(enumerate(sims), key=lambda item: -item[1])[0:5]
	
	result+="Top answers:\n\n"
	
	for nearest in sims:
		result = result + str(nearest[1]) + "\n" + str(dfr['answer'][nearest[0]]) + "\nВопрос в логе: " + str(dfr['question'][nearest[0]]) + "\n\n" 
	
	result+="\n\n\nNearest clusters:\n\n"
	
	
	vec_lda_sorted = sorted(vec_lda, key=lambda tup: -tup[1])
	print(vec_lda_sorted)
	
	
	for cluster in vec_lda_sorted:
		topic_text = ""
		for keyword in lda.show_topic(cluster[0],topn=12):
			topic_text = topic_text + " " + keyword[0]
		result = result + str(cluster[1]) + "\n" + topic_text +  "\n\n"
		
	
	#print(lda.print_topic(max(vec_lda, key=lambda item: item[1])[0]))

	
	return result
	