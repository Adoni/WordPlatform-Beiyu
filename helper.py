#coding:utf8
from deliver import Deliver
from sklearn.cluster import AffinityPropagation
import numpy
import json

deliver=Deliver()

def distant(a,b):
    dist=numpy.linalg.norm(a-b)
    #dist=1.0/(1.0+dist)
    return dist

def get_word_meaning(date,word):
    dates=range(2005,int(date)+1)
    list_words=deliver.get_closest_words(dates,word)
    closest_words=[]
    for l in list_words:
        closest_words+=l
    closest_words=list(set(closest_words))
    closest_words=zip(closest_words,map(lambda w:deliver.get_word_embedding(date,w),closest_words))
    closest_words=filter(lambda w:not w[1] is None,closest_words)
    closest_words=filter(lambda w:not w[1]=='None',closest_words)
    X=numpy.array(map(lambda w:w[1],closest_words))
    print X.shape
    af = AffinityPropagation(preference=-25).fit(X)
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
    dist=map(lambda m:1.0/distant(word_embedding,m['center']),meaning)
    dist_sum=sum(dist)
    dist=map(lambda d:d/dist_sum,dist)
    return dist

def get_batch_distant(dates,word):
    batch_distant=dict()
    for date in dates:
        meaning=get_word_meaning(date,word)
        dist=get_distance(date,word,meaning)
        batch_distant[date]=zip(map(lambda m:map(lambda mm:mm[0],m['words']),meaning),dist)
    json_format_distant=json.dumps(batch_distant)
    return batch_distant,json_format_distant

if __name__=='__main__':
    word=u'小米'
    #word=u'第三者'
    print [get_batch_distant([2005,2007],word)[1]]
