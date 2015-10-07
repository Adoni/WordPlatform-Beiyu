import web
render = web.template.render('templates/',base='layout')
dates=range(2005,2015)

def get_tf_df(dates):
    tf=dict()
    df=dict()
    for date in dates:
        tf[date]=dict()
        df[date]=dict()
        try:
            f=open('/data/adoni/catchwords/result_%d.txt'%date)
        except:
            continue
        for line in f:
            line=line.strip().decode('utf8').split(' ')
            tf[date][line[0]]=int(line[1])
            df[date][line[0]]=int(line[2])
    return tf,df

tf,df=get_tf_df(dates)

class catchwords_index:
    def GET(self):
        return render.catchwords_index()

class catchwords_show:
    def GET(self):
        raise web.seeother('/catchwords')

    def POST(self):
        params = web.input()
        word=params['word']
        distribute={'TF':[0]*len(dates),'DF':[0]*len(dates)}
        for index,date in enumerate(dates):
            try:
                distribute['TF'][index]=tf[date][word]
            except:
                pass
            try:
                distribute['DF'][index]=df[date][word]
            except:
                pass
        return render.catchwords_show(
                dates=dates,
                word=word,
                distribute=distribute,
                )
