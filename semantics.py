import web
render = web.template.render('templates/',base='layout')
from deliver import Deliver
from helper import get_batch_distant
import json

deliver=Deliver()
available_dates=[2005,2006,2007,2008,2009,2010,2011,2012]
available_dates=map(lambda d:str(d),available_dates)
def get_intersection(words1,words2):
    a=[]
    b=[]
    c=[]
    for w1,w2 in zip(words1,words2):
        a.append(filter(lambda x:x not in w2, w1))
        b.append(filter(lambda x:x not in w1, w2))
        c.append(filter(lambda x:x in w1 and x in w2, w2))
    return a,b,c
class semantics_index:
    def GET(self):
        return render.semantics_index(dates=available_dates)

class semantics_show:
    def GET(self):
        raise web.seeother('/semantics')
    def POST(self):
        params = web.input()
        word=params['word']
        checked_dates=[]
        for p in available_dates:
            if p in params and params[p]=='on':
                checked_dates.append(p)
        if 'joint' in params and params['joint']=='on':
            jointly_search=True
        else:
            jointly_search=False
        checked_dates=map(lambda d:int(d),checked_dates)
        checked_dates=sorted(checked_dates)
        checked_dates=map(lambda d:str(d),checked_dates)
        checked_dates=filter(lambda d:not deliver.get_word_embedding(d,word) is None,checked_dates)
        if checked_dates==[]:
            return render.error(info="Cannot find word %s in our corpus!"%word)
        words=deliver.get_closest_words(checked_dates,word, jointly_search=jointly_search)
        collocation_result=deliver.batch_collocation_search(word,checked_dates)
        if jointly_search:
            words,collocation_result,intersection=get_intersection(words,collocation_result)
        else:
            words,collocation_result,intersection=words,collocation_result,[]
        batch_distant,json_format_distant=get_batch_distant(checked_dates,word)
        if batch_distant is None:
            return render.error(info='None')
        words=dict(zip(checked_dates,words))
        collocation_result=dict(zip(checked_dates,collocation_result))
        intersection=dict(zip(checked_dates,intersection))
        return render.semantics_show(
                dates=available_dates,
                checked_dates=checked_dates,
                word=word,
                words=words,
                batch_distant=batch_distant,
                json_format_distant=json_format_distant,
                jointly_search=jointly_search,
                collocation_result=collocation_result,
                intersection=intersection,
                )
