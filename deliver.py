#!/usr/bin/env python
#coding=utf8
import pika
import settings
import uuid
import pickle
import StringIO
import rpyc
from search_word_list_by_collocation import collocation_search

class Deliver(object):
    def __init__(self):
        self.conn=rpyc.connect('localhost',22222)

    def batch_collocation_search(self,word,dates,total_count=20):
        result=[]
        for date in dates:
            result.append(collocation_search(word,int(date),total_count))
        return result

    def get_closest_words(self,dates,word,jointly_search=False):
        result=pickle.loads(self.conn.root.get_closest_words(dates,word,count=20))
        #if jointly_search:
        if False:
            collocation_result=self.batch_collocation_search(word,dates)
            for i in xrange(len(result)):
                result[i]=filter(lambda x:x not in collocation_result[i],result[i])

        return result

    def get_word_embedding(self,date,word):
        result=self.conn.root.get_word_embedding(date,word)
        return pickle.loads(result)

if __name__=='__main__':
    deliver=Deliver()
    print '======'
    print ' '.join(deliver.get_closest_words(['2012'],'水')[0])
