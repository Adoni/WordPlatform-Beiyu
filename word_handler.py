#coding:utf8
from my_vector_reader import simple_embedding_cluster_viewer
from settings import Embedding_Dir
class word_handler:
    def __init__(self):
        self.embeddings=dict()

    def add_embedding_file(self, date):
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

if __name__=='__main__':
    handler=word_handler()
    handler.get_closest_words(['2005'],'呵呵')
