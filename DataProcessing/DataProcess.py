__author__ = 'sunxiaofei'
import numpy
import os

DATA_DIR='/mnt/data1/zzllzy/'
DATE_SORTED_DATA_DIR='/mnt/data1/adoni/date_sorted_data/'
SEMANTIC_WORD_VECTORS_DIR='/mnt/data1/adoni/semantic_word_vectors/'
def get_pos_tags_from_raw_file():
    import re
    raw_data_file=open(DATA_DIR+'data')
    i=0
    pos_tags=set()
    for line in raw_data_file:
        i+=1
        if i>1000:
            break
        p=re.compile(r'/[a-z,A-Z]+')
        for pos_tag in p.findall(line):
            pos_tags.add(pos_tag)
        print len(pos_tags)
    open('./postags.data','w').write(' '.join(pos_tags))
    raw_data_file.close()


def raw_data_to_date_sorted_data():
    raw_data_file=open(DATA_DIR+'data')
    pos_tags=open('./postags.data').readlines()[0].split(' ')
    files={}
    for line in raw_data_file:
        line=line.replace('\n','').split('\t\t')
        date=line[1].split('-')
        content=line[2]
        for pos_tag in pos_tags:
            content=content.replace(pos_tag+' ',' ')
        for pos_tag in pos_tags:
            content=content.replace(pos_tag,'')
        file_name=date[0]+'-'+date[1]+'.data'
        try:
            files[file_name].write(content+'\n')
        except:
            files[file_name]=open(DATE_SORTED_DATA_DIR+file_name,'w')


def get_word_vectors_from_file(word_vector_file):
    f = open(word_vector_file)
    word_vectors = dict()
    for line in f:
        line = line.replace('\n').decode('utf8').split('\t')
        word_vectors[line[0]] = numpy.array(word_vectors[1:], dtype=numpy.float)


def get_file_names_in_range(start_year, start_month, end_year, end_month):
    file_names=[]
    if start_year>end_year:
        raise Exception('Time range is illegal')
    if start_year==end_year and start_month>end_month:
        raise Exception('Time range is illegal')
    if start_year==end_year:
        for m in range(start_month, end_month+1):
            file_names.append(DATE_SORTED_DATA_DIR+str(start_year)+'-'+str(m)+'.data')
        return file_names
    if start_year<end_year:
        for m in range(start_month, 12+1):
            file_names.append(DATE_SORTED_DATA_DIR+str(start_year)+'-'+str(m)+'.data')
        for y in range(start_year+1,end_year):
            for m in range(1,12+1):
                file_names.append(DATE_SORTED_DATA_DIR+str(y)+'-'+str(m)+'.data')
        for m in range(1, end_month+1):
            file_names.append(DATE_SORTED_DATA_DIR+str(end_year)+'-'+str(m)+'.data')
        return file_names


def date_sorted_data_to_word_vectors_file(start_year, start_month, end_year, end_month):
    file_names = get_file_names_in_range(start_year,start_month,end_year,end_month)
    input_file = SEMANTIC_WORD_VECTORS_DIR+str(start_year)+'-'+str(start_month)+'-'+str(end_year)+'-'+str(end_month)+'.data'
    command = 'cat '+' '.join(file_names)+' > '+input_file
    #os.system(command)
    output_file = input_file.replace('.data', '.vec')
    command = '~/word2vec/word2vec -train '+input_file+' -output '+output_file\
              + ' -cbow 0 -size 50 -window 7 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 0'
    os.system(command)


if __name__=='__main__':
    date_sorted_data_to_word_vectors_file(2012,1,2012,2)
    #raw_data_to_date_sorted_data()
    #get_pos_tags_from_raw_file()
