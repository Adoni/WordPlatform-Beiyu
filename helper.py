#coding:utf8
from deliver import Deliver
from sklearn.cluster import AffinityPropagation
import numpy

deliver=Deliver()

def distant(a,b):
    dist=numpy.linalg.norm(a-b)
    #dist=1.0/(1.0+dist)
    return dist

def get_word_meaning(date,word):
    dates=range(2005,date+1)
    list_words=deliver.get_closest_words(dates,word)
    closest_words=[]
    for l in list_words:
        closest_words+=l
    closest_words=list(set(closest_words))
    closest_words=zip(closest_words,map(lambda w:deliver.get_word_embedding(date,w),closest_words))
    closest_words=filter(lambda w:not w[1]=='None',closest_words)
    X=numpy.array(map(lambda w:w[1],closest_words))
    af = AffinityPropagation(preference=-20).fit(X)
    labels = af.labels_
    meaning=dict()
    for index,label in enumerate(labels):
        if label not in meaning:
            meaning[label]={
                    'words':[],
                    'center':None
                    }
        meaning[label]['words'].append(closest_words[index])
    for label in meaning:
        meaning[label]['center']=numpy.mean(map(lambda d:d[1],meaning[label]['words']),axis=0)
    return meaning.values()

def get_distance(date,word,meaning):
    word_embedding=deliver.get_word_embedding(date,word)
    for m in meaning:
        print ' '.join(map(lambda d:d[0].encode('utf8'),m['words']))
        print distant(word_embedding,m['center'])


if __name__=='__main__':
    word=u'小米'
    word=u'第三者'
    for year in range(2005,2012):
        print year
        meaning=get_word_meaning(year,word)
        get_distance(year,word,meaning)
