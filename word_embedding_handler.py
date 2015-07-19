#!/usr/bin/env python
#coding=utf8
import pika
import pickle
from pymongo import MongoClient
from my_vector_reader import simple_embedding_cluster_viewer
from settings import Embedding_Dir
from settings import QUEUE_NAME
from rpyc import Service
from rpyc.utils.server import ThreadedServer

class word_handler():
    def __init__(self):
        self.embeddings=dict()
        self.closest_words_db=MongoClient().word_platform.closest_words

    def add_embedding_file(self, date):
        print 'Add embedding file of %s'%date
        date=str(date)
        if '-' in date:
            year=date.split('-')[0]
            month=date.split('-')[1]
            embedding_file_name="%s/%s/%s-%s-embedding.data"%(Embedding_Dir,year,year,month)
        else:
            year=date
            embedding_file_name="%s/%s/%s-embedding.data"%(Embedding_Dir,year,year)
        self.embeddings[date]=simple_embedding_cluster_viewer(embedding_file_name,'utf8')
        print 'Done'

    def get_closest_words(self, dates, word, count=10):
        if type(word)==unicode:
            word=word.encode('utf8')
        closest_words=[]
        for date in dates:
            date=str(date)
            if date not in self.embeddings:
                try:
                    self.add_embedding_file(date)
                except:
                    closest_words.append([])
                    continue
            date_closest_words=self.closest_words_db.find_one({'_id':'%s %s'%(word,date)})
            if date_closest_words is None:
                date_closest_words=self.embeddings[date].get_closest_words(word,count=20)
                self.closest_words_db.insert({'_id':'%s %s'%(word,date),'closest_words':date_closest_words})
            else:
                date_closest_words=date_closest_words['closest_words']
            closest_words.append(date_closest_words[:count])
        return pickle.dumps(closest_words)

    def get_word_embedding(self,date,word):
        date=str(date)
        if date not in self.embeddings:
            try:
                self.add_embedding_file(date)
            except:
                return pickle.dumps('None')
        result=self.embeddings[date][word]
        return pickle.dumps(result)

class Listener(Service):
    def exposed_get_closest_words(self, dates, word, count=10):
        global handler
        return handler.get_closest_words(dates,word,count)
    def exposed_get_word_embedding(self,date,word):
        global handler
        return handler.get_word_embedding(date,word)

global handler
def main():
    global handler
    handler=word_handler()
    for date in xrange(2005,2013):
        handler.add_embedding_file(date)
    sr=ThreadedServer(Listener,port=22222,auto_register=False)
    sr.start()

if __name__ == '__main__':
    main()
