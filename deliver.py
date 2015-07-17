#!/usr/bin/env python
#coding=utf8
import pika
import settings
import uuid
import cPickle
import StringIO

class Deliver(object):
    def __init__(self):
        self.conn=rpyc.connect('localhost',22222)

    def get_closest_words(self,dates,word):
        return self.conn.get_closest_words(dates,word)

    def get_word_embedding(self,date,word):
        return self.conn.get_word_embedding(date,word)

if __name__=='__main__':
    deliver=Deliver()
    print deliver.get_word_embedding('2005','hello')
