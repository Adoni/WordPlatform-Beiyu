import web
render = web.template.render('templates/',base='layout')
from deliver import Deliver

class semantics_index:
    def GET(self):
        dates=[2005,2006,2007,2008,2009,2010,2011,2012]
        return render.semantics_index(dates=dates)

class semantics_show:
    def GET(self):
        return 'Semantics show'
    def POST(self):
        params = web.input()
        word=params['word']
        checked_dates=[]
        for p in params:
            if params[p]=='on':
                checked_dates.append(p)
        checked_dates=map(lambda d:int(d),checked_dates)
        checked_dates=sorted(checked_dates)
        dates=map(lambda d:str(d),checked_dates)
        deliver=Deliver()
        words=deliver.get_closest_words(dates,word)
        print words
        words=zip(dates,words)
        dates=[2005,2006,2007,2008,2009,2010,2011,2012]
        return render.semantics_show(dates=dates,word=word,words=words,checked_dates=checked_dates)
