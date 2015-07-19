import web
render = web.template.render('templates/',base='layout')
from deliver import Deliver
from helper import get_batch_distant
import json

deliver=Deliver()
class semantics_index:
    def GET(self):
        dates=[2005,2006,2007,2008,2009,2010,2011,2012]
        return render.semantics_index(dates=dates)

class semantics_show:
    def GET(self):
        raise web.seeother('/semantics')
    def POST(self):
        params = web.input()
        word=params['word']
        checked_dates=[]
        for p in params:
            if params[p]=='on':
                checked_dates.append(p)
        checked_dates=map(lambda d:int(d),checked_dates)
        checked_dates=sorted(checked_dates)
        checked_dates=map(lambda d:str(d),checked_dates)
        checked_dates=filter(lambda d:not deliver.get_word_embedding(d,word) is None,checked_dates)
        words=deliver.get_closest_words(checked_dates,word)
        batch_distant,json_format_distant=get_batch_distant(checked_dates,word)
        if batch_distant is None:
            return render.error(info='None')
        words=dict(zip(checked_dates,words))
        dates=[2005,2006,2007,2008,2009,2010,2011,2012]
        dates=map(lambda date:str(date),dates)
        return render.semantics_show(
                dates=dates,
                checked_dates=checked_dates,
                word=word,
                words=words,
                batch_distant=batch_distant,
                json_format_distant=json_format_distant,
                )
