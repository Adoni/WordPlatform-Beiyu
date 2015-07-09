#!/usr/bin/env python
#coding=utf8
import pika
import settings
import uuid
import cPickle
import StringIO

class Deliver(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response,
                                   no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response=cPickle.load(StringIO.StringIO(body))

    def request(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=settings.QUEUE_NAME,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(body))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def get_closest_words(self,dates,word):
        body={'function':'get_closest_words',
                'dates':dates,
                'word':word
                }
        return self.request(body)

    def get_word_embedding(self,date,word):
        body={'function':'get_word_embedding',
                'date':date,
                'word':word
                }
        return self.request(body)

if __name__=='__main__':
    deliver=Deliver()
    print deliver.get_word_embedding('2005','hello')
