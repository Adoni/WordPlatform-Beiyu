#coding:utf8
import web
from deliver import Deliver
from helper import get_batch_distant
from helper import transfer_to_json
from helper import transfer_to_line
import json
from matplotlib.pyplot import figure
import mpld3
from small_utils.vector_reader import read_vectors

render = web.template.render('templates/',base='layout')

'''
deliver是用于和提供相近词模块的交互的中间层
'''
deliver=Deliver()
embedding=read_vectors(base_dir+'pca_embedding.data',as_dict=True)

'''
available_dates指当前可以获取的年份信息
'''
available_dates=[2005,2006,2007,2008,2009,2010,2011,2012,2013]
available_dates=map(lambda d:str(d),available_dates)

def draw(data,labels,ax):
    x=map(lambda d:d[0],data)
    y=map(lambda d:d[1],data)
    line, = ax.plot(x, y, '.-', color='purple')
    for l in labels:
        ax.annotate(l.decode('utf8'),
                xy=labels[l],
                )

def pca_plot(words,years,embedding):
    fig = figure()
    ax = fig.add_subplot(111)
    for w in words:
        all_embedding=[]
        all_labels=dict()
        for year in years:
            pca_w=str(year)+w
            if pca_w in embedding:
                all_embedding.append(embedding[pca_w])
                all_labels[pca_w]=embedding[pca_w]
            else:
                print 'Not in year %d'%year
        draw(all_embedding,all_labels,ax)
    return fig

class pca_index:
    def GET(self):
        return render.pca_index(dates=available_dates)

class pca_show:
    def GET(self):
        raise web.seeother('/pca')
    def POST(self):
        params = web.input()
        words=params['words'].strip().split(' ')
        checked_dates=[]
        for p in available_dates:
            if p in params and params[p]=='on':
                checked_dates.append(p)
        checked_dates=map(lambda d:int(d),checked_dates)
        checked_dates=sorted(checked_dates)
        checked_dates=map(lambda d:str(d),checked_dates)
        checked_dates=filter(lambda d:not deliver.get_word_embedding(d,word) is None,checked_dates)
        if checked_dates==[]:
            return render.error(info="Cannot find word %s in our corpus!"%word)
        fig=pca_plot(words,checked_dates,embedding)
        html_fit=mpld3.fig_to_html(fig)
        return render.pca_show_line(
                dates=available_dates,
                checked_dates=checked_dates,
                html_fig=html_fig
                )
