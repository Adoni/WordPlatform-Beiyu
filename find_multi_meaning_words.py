#coding:utf8
from my_vector_reader import read_vectors
from helper import get_batch_distant
from my_progress_bar import progress_bar

def output_all_words():
    words=read_vectors('/data/adoni/embedding/2012/2012-embedding.data','utf8')[0]
    fout=open('all_words.data','w')
    for w in words:
        fout.write('%s\n'%w.encode('utf8'))

def find_multi_meaning_words():
    all_words=[line[:-1] for line in open('./all_words.data')]
    fout=open('multi_meaning_words.data','w')
    bar=progress_bar(len(all_words))
    for index,w in enumerate(all_words):
        meaning=get_batch_distant(['2012'],w)[0]
        if meaning is None:
            continue
        meaning=meaning['2012']
        if len(meaning)>1:
            fout.write("%s %d\n"%(w,len(meaning)))
        bar.draw(index)

if __name__=='__main__':
    find_multi_meaning_words()
