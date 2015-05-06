__author__ = 'sunxiaofei'
import pickle
from DataProcess import get_word_vectors_from_file
import numpy
from DataProcess import SEMANTIC_WORD_VECTORS_DIR

def get_word_vectors(time_batch):
    file_name = SEMANTIC_WORD_VECTORS_DIR+'-'.join([str(t) for t in time_batch])+'.vec'
    return get_word_vectors_from_file(file_name)


def get_distance(a, b):
    d = (a-b)**2
    return numpy.sqrt(d.sum())


def get_most_closed_words(word, word_vectors, count=10):
    distance = {}
    v = word_vectors[word]
    for w in word_vectors:
        distance[w] = get_distance(v, word_vectors[w])
    distance = sorted(distance.iteritems(), key=lambda d: d[1], reverse=True)
    return distance[0:count]


def get_word_semantic(start_time, end_time, word):
    word_vectors = get_word_vectors(start_time, end_time)
    most_closed_words = get_most_closed_words(word, word_vectors)
    return most_closed_words


if __name__=='__main__':
    get_word_vectors([2012,1,2012,7])
