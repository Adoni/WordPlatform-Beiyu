__author__ = 'sunxiaofei'
import numpy
import subprocess


def get_word_vectors_from_file(word_vector_file):
    f = open(word_vector_file)
    word_vectors = dict()
    for line in f:
        line = line.replace('\n').decode('utf8').split('\t')
        word_vectors[line[0]] = numpy.array(word_vectors[1:], dtype=numpy.float)


def raw_data_to_word_vectors_file(start_time, end_time):
    file_names = []
    for i in range(start_time, end_time+1):
        file_names.append(str(i)+'.txt')
    input_file = str(start_time)+'-'+str(end_time)+'.txt'
    command = 'cat '+' '.join(file_names)+' > '+input_file
    print command
    subprocess.call(command)
    output_file = input_file.replace('.txt', '.vec')
    command = './word2vec -train '+input_file+' -output '+output_file\
              + ' -cbow 0 -size 200 -window 7 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 0'
    subprocess.call(command)


if __name__=='__main__':
    raw_data_to_word_vectors_file(1,7)
