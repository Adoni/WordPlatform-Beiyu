#!/usr/bin/env python
#coding=utf8
import pika
import cPickle
import StringIO
from my_vector_reader import simple_embedding_cluster_viewer
from settings import Embedding_Dir
from settings import QUEUE_NAME
from rpyc import Service
from rpyc.utils.server import ThreadedServer

class word_handler(Service):
    def __init__(self,Object):
        self.embeddings=dict()
        for year in range(2005,2013):
            print year
            self.add_embedding_file(str(year))

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

    def exposed_get_closest_words(self, dates, word, count=10):
        closest_words=[]
        for date in dates:
            date=str(date)
            if date not in self.embeddings:
                try:
                    self.add_embedding_file(date)
                except:
                    closest_words.append([])
                    continue
            closest_words.append(self.embeddings[date].get_closest_words(word))
        return self.encapsulate_result(closest_words)

    def exposed_get_word_embedding(self,date,word):
        date=str(date)
        if date not in self.embeddings:
            try:
                self.add_embedding_file(date)
            except:
                return self.encapsulate_result('None')
        return self.encapsulate_result(self.embeddings[date][word])

    def encapsulate_result(self, result):
        if result is None:
            result='None'
        output_file=StringIO.StringIO()
        cPickle.dump(result, output_file)
        output_file.flush()
        return output_file

def main():
    sr=ThreadedServer(word_handler,port=22222,auto_register=False)
    sr.start()

if __name__ == '__main__':
    main()
