#!/usr/bin/env python
#coding=utf8
import pika
import settings
import uuid
import pickle
import StringIO
import rpyc

class Deliver(object):
    def __init__(self):
        self.conn=rpyc.connect('localhost',22222)

    def get_closest_words(self,dates,word):
        result=self.conn.root.get_closest_words(dates,word)
        return pickle.loads(result)

    def get_word_embedding(self,date,word):
        result=self.conn.root.get_word_embedding(date,word)
        return pickle.loads(result)

if __name__=='__main__':
    deliver=Deliver()
    print deliver.get_word_embedding('2005','hello')
