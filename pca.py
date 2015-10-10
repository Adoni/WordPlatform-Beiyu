#coding:utf8
import web
from deliver import Deliver
from helper import get_batch_distant
from helper import transfer_to_json
from helper import transfer_to_line
import json
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure
from matplotlib.font_manager import FontProperties
import mpld3
from small_utils.vector_reader import read_vectors
from settings import Embedding_Dir
import StringIO
import base64
from matplotlib import colors
import six

render = web.template.render('templates/',base='layout')

'''
deliver是用于和提供相近词模块的交互的中间层
'''
deliver=Deliver()
embedding=read_vectors('%s/pca_embedding.data'%Embedding_Dir,as_dict=True)
colors_=list(six.iteritems(colors.cnames))

'''
available_dates指当前可以获取的年份信息
'''
available_dates=[2005,2006,2007,2008,2009,2010,2011,2012,2013]
available_dates=map(lambda d:str(d),available_dates)

def draw(data,labels,ax,color):
    x=map(lambda d:d[0],data)
    y=map(lambda d:d[1],data)
    line, = ax.plot(x, y, '.-', color=color)
    font = FontProperties(fname=r"/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", size=10)
    print color
    for l in labels:
        ax.annotate(l.decode('utf8'),
                xy=labels[l],
                fontproperties=font,
                )

def pca_plot(words,years):
    fig = figure()
    ax = fig.add_subplot(111)
    for index,w in enumerate(words):
        w=w.encode('utf8')
        all_embedding=[]
        all_labels=dict()
        for year in years:
            pca_w=str(year)+w
            if pca_w in embedding:
                xy=embedding[pca_w]
                all_embedding.append(xy)
                all_labels[pca_w]=xy
            else:
                print 'Not in year %s'%str(year)
        draw(all_embedding,all_labels,ax,color=colors_[index][0])
    buf=StringIO.StringIO()
    fig.savefig(buf, format='png')
    return base64.encodestring(buf.getvalue())

def dump_pca_data(words,years):
    data=[]
    for index,w in enumerate(words):
        word_data=dict()
        w=w.encode('utf8')
        word_data['name']=w
        word_data['data']=[]
        word_data['type']='line'
        word_data['smooth']=True
        for year in years:
            pca_w=str(year)+w
            if pca_w in embedding:
                xy=embedding[pca_w]
                word_data['data'].append([xy[0],xy[1]])
            else:
                print 'Not in year %s'%str(year)
        data.append(word_data)
    return json.dumps(words),json.dumps(data)


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
        for word in words:
            checked_dates=filter(lambda d:not deliver.get_word_embedding(d,word) is None,checked_dates)
        if checked_dates==[]:
            return render.error(info="Cannot find those in our corpus!")
        # fig=pca_plot(words,checked_dates)
        # return render.pca_show(
        #         dates=available_dates,
        #         checked_dates=checked_dates,
        #         fig=fig
        #         )
        legend,data=dump_pca_data(words,checked_dates)
        return render.pca_show(
                dates=available_dates,
                checked_dates=checked_dates,
                legend=ledend,
                data=data,
                )

if __name__=='__main__':
    print pca_plot(['中国'],[2005,2006,2007])
