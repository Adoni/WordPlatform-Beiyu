#coding:utf8
from deliver import Deliver
from sklearn.cluster import AffinityPropagation
import numpy
import json

deliver=Deliver()

def distant(a,b):
    a=numpy.array(a)
    b=numpy.array(b)
    dist=numpy.linalg.norm(a-b)
    #dist=1.0/(1.0+dist)
    return dist

def get_word_meaning(date,word):
    dates=range(2005,int(date)+1)
    list_words=deliver.get_closest_words(dates,word)
    list_words=filter(lambda l:len(l)>0, list_words)
    closest_words=[]
    for i in xrange(len(list_words[0])):
        for l in list_words:
            closest_words.append(l[i])
    closest_words=list(set(closest_words))
    closest_words=zip(closest_words,map(lambda w:deliver.get_word_embedding('all',w),closest_words))
    #closest_words=zip(closest_words,map(lambda w:deliver.get_word_embedding(date,w),closest_words))
    closest_words=filter(lambda w:not w[1] is None,closest_words)
    closest_words=filter(lambda w:not w[1]=='None',closest_words)
    X=numpy.array(map(lambda w:w[1],closest_words))
    af = AffinityPropagation(preference=-680).fit(X)
    labels = af.labels_
    meaning=dict()
    if True in numpy.isnan(labels):
        return None
    for index,label in enumerate(labels):
        if label not in meaning:
            meaning[label]={
                    'words':[],
                    'center':None
                    }
        meaning[label]['words'].append(closest_words[index])
    for label in meaning:
        meaning[label]['center']=numpy.mean(map(lambda d:d[1],meaning[label]['words']),axis=0)
    #return meaning.values()
    result=[]
    for m in meaning.values():
        result.append(map(lambda w:w[0],m['words']))
    return result

def get_center(date,meaning):
    embedding=[]
    count=0
    for w in meaning:
        e=deliver.get_word_embedding(date,w)
        if e is None:
            continue
        embedding.append(e)
        count+=1
    center=numpy.mean(embedding,axis=0)
    return center,count

def get_distance(date,word,meaning):
    word_embedding=deliver.get_word_embedding(date,word)
    closest_word=deliver.get_closest_words([date],word)[0][0]
    min_distant=distant(word_embedding,deliver.get_word_embedding(date,closest_word))
    #dist=map(lambda m:1.0/distant(word_embedding,m['center']),meaning)
    #dist=map(lambda m:1.0/distant(word_embedding,get_center(date,m)),meaning)
    dist=[]
    for m in meaning:
        center,count=get_center(date,m)
        d=distant(word_embedding,center)
        d=abs(d-min_distant)
        d=1.0/d*count
        dist.append(d)
    #dist=map(lambda m:1.0/distant(word_embedding,get_center(date,m)),meaning)
    dist_sum=sum(dist)
    dist=map(lambda d:d/dist_sum,dist)
    return dist

def get_batch_distant(dates,word):
    batch_distant=dict()
    meaning=get_word_meaning(2012,word)
    if meaning is None:
        return None,''
    for date in dates:
        #meaning=get_word_meaning(date,word)
        #if meaning is None:
        #    return None,''
        dist=get_distance(date,word,meaning)
        #print dist
        batch_distant[date]=zip(meaning,dist)
    return batch_distant,meaning

def transfer_to_json(batch_distant):
    json_format_distant=json.dumps(batch_distant)
    return json_format_distant

def transfer_to_line(batch_distant,dates,meaning,count=3):
    short_meaning=['\n'.join(m[:count]) for m in meaning]
    distribute=dict()
    for m in short_meaning:
        distribute[m.encode('utf8')]={'str_meaning':json.dumps(m),'data':[0]*len(dates)}
    for index,date in enumerate(dates):
        for m,d in batch_distant[date]:
            distribute['\n'.join(m[:count]).encode('utf8')]['data'][index]=d
    return short_meaning,distribute

def test():
    word=u'小米'
    #word=u'沈阳'
    #word=u'第三者'
    word=u'山寨'
    dates=[2012]
    bach,meaning=get_batch_distant(dates,word)
    print meaning
    transfer_to_line(bach,dates,meaning)

if __name__=='__main__':
    test()
