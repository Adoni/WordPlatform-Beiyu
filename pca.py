import numpy as np
from small_utils.vector_reader import read_vectors
from small_utils.vector_reader import simple_embedding_cluster_viewer
from sklearn.decomposition import PCA
from matplotlib.pyplot import figure
from matplotlib.patches import Ellipse
import mpld3

base_dir='/Users/sunxiaofei/Desktop/'
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
    print mpld3.fig_to_html(fig)

def test():
    embedding=read_vectors(base_dir+'pca_embedding.data',as_dict=True)
    while 1:
        words=raw_input('Words:').strip().split(' ')
        pca_plot(words,[2005,2006],embedding)

if __name__=='__main__':
    test()
