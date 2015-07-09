#!/usr/bin/env python
#coding=utf8
import pika
import cPickle
import StringIO
from my_vector_reader import simple_embedding_cluster_viewer
from settings import Embedding_Dir
from settings import QUEUE_NAME

class word_handler:
    def __init__(self):
        self.embeddings=dict()

    def add_embedding_file(self, date):
        print 'Add embedding file of %s'%date
        if '-' in date:
            year=date.split('-')[0]
            month=date.split('-')[1]
            embedding_file_name="%s/%s/%s-%s-embedding.data"%(Embedding_Dir,year,year,month)
        else:
            year=date
            embedding_file_name="%s/%s/%s-embedding.data"%(Embedding_Dir,year,year)
            self.embeddings[date]=simple_embedding_cluster_viewer(embedding_file_name,'utf8')

    def get_closest_words(self, dates, word, count=10):
        closest_words=[]
        for date in dates:
            if date not in self.embeddings:
                self.add_embedding_file(date)
            closest_words.append(self.embeddings[date].get_closest_words(word))
        return closest_words

    def get_word_embedding(self,date,word):
        if date not in self.embeddings:
            self.add_embedding_file(date)
        return self.embeddings[date][word]


global handler

def on_request(ch, method, props, body):
    body=eval(body)
    if body['function'] is 'get_closest_words':
        result=handler.get_closest_words(body['dates'],body['word'])
    if body['function'] is 'get_word_embedding':
        result=handler.get_word_embedding(body['date'],body['word'])

    output_file=StringIO.StringIO()
    cPickle.dump(result, output_file)
    output_file.flush()
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=output_file.getvalue())
    ch.basic_ack(delivery_tag = method.delivery_tag)


def initialize_handler():
    global handler
    for year in range(2005,2006):
        handler.add_embedding_file(str(year))
def main():
    global handler
    handler=word_handler()
    initialize_handler()
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue=QUEUE_NAME)

    channel.start_consuming()

if __name__ == '__main__':
    main()
