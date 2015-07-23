#coding:utf8
#将数据插入mysql数据库，建立索引查看查询效果
import operator
import MySQLdb
import time
import datetime
import time
import MySQLdb.cursors
import sys
from  math import log
reload(sys)
sys.setdefaultencoding('utf8')

def sql_index_word_md5():
	cnx = MySQLdb.connect(user="root", passwd="roo", host="127.0.0.1",db="by_work", charset='utf8')
	#cnx.autocommit(1)
	cursor = cnx.cursor()
	add_item = ("INSERT INTO all_info (word,month,count,word_set) VALUES (%s, %s,%s, %s)")
	num=0
	#item=("大家","1","2","哈哈 5 人民 6")
	#cursor.execute(add_item,item)
	#cnx.commit()
	#return
	for line in open("baozhi_2012.order"):
		line=line.strip().split("\t")
		if len(line)!=4:
			continue
		num+=1
		#if num<=3266919:
		#	continue
		line[3]=line[3].strip()
		item = (line[0],line[1],line[2],line[3])
		try:
			cursor.execute(add_item, item)
		except:
			print num
		if not num%40000:
			cnx.commit()
	cnx.commit()

def take_statistics():
	my_hash={}
	word_count_hash={}
	for i in range(12):
		fname=str(i+1)
		my_hash.clear()
		word_count_hash.clear()
		for line in open("baozhi_2012"):
			line=line.strip().split("\t\t")
			if line[0]!=fname:
				continue
			if len(line)!=2:
				continue
			line[1]=line[1].strip()
			seg=line[1].split(" ")
			seg=list(set(seg))
			for word in seg:
				if word not in word_count_hash:
					word_count_hash[word]=0
				word_count_hash[word]+=1
				key=word+"\t"+str(line[0])
				if key not in my_hash:
					my_hash[key]={}
				for w in seg:
					if word==w:
						continue
					if w not in my_hash[key]:
						my_hash[key][w]=0
					my_hash[key][w]+=1
		p=open("baozhi_2012.noorder","a")
		for key in my_hash:
			p.write(key)
			p.write("\t")
			word=key.split("\t")[0]
			p.write(str(word_count_hash[word]))
			ss="\t"
			for kk in my_hash[key]:
				ss+=kk+" "+str(my_hash[key][kk])+" "
			p.write(ss)
			p.write("\n")
		p.close()

def search_by_count_bendi(word):
	cnx = MySQLdb.connect(user="root", passwd="roo", host="127.0.0.1",db="by_work",charset="utf8", \
		cursorclass=MySQLdb.cursors.DictCursor)
	cursor = cnx.cursor()
	num=0
	query1 = ("SELECT word_set FROM all_info WHERE word= %s")
	query2 = ("SELECT count FROM all_info WHERE word= %s")
	word_hash={}
	word_hash.clear()
	start=time.clock()
	cursor.execute(query1,(word,))
	cnx.commit()
	end=time.clock()
	results=cursor.fetchall()
	if len(results)==0:
		print "没有查询到该词!"
		return
	sql_time=end-start


	start=time.clock()
	for item in results:
		line=item["word_set"].strip().split(" ")
		index_len=len(line)/2
		for index in xrange(index_len):
			# if line[index*2] == word:
			# 	continue
 			if line[index*2] not in word_hash:
				word_hash[line[index*2]]=0
			word_hash[line[index*2]]+=int(line[index*2+1])

	sorted_word_hash = sorted(word_hash.iteritems(), key=operator.itemgetter(1), reverse=True)
	num=0
	for item in sorted_word_hash:
		if item[0]==word:
			continue
		print item[0],item[1]
		num+=1
		if num==50:
			break
	end=time.clock()
	print "sql时间：%f" % (sql_time)
	print "计算时间：%f" % (end-start)


#查询word，返回top10 word_set
def search_by_count(word):
	cnx = MySQLdb.connect(user="root", passwd="roo", host="127.0.0.1",db="by_work",charset="utf8", \
		cursorclass=MySQLdb.cursors.DictCursor)
	cursor = cnx.cursor()
	num=0
	query1 = ("SELECT word_set FROM all_info WHERE word= %s")
	query2 = ("SELECT count FROM all_info WHERE word= %s")
	word_hash={}
	word_hash.clear()
	start=time.clock()
	cursor.execute(query1,(word,))
	cnx.commit()
	end=time.clock()
	results=cursor.fetchall()
	if len(results)==0:
		print "没有查询到该词!"
		return
	sql_time=end-start


	start=time.clock()
	for item in results:
		line=item["word_set"].strip().split(" ")
		index_len=len(line)/2
		for index in xrange(index_len):
			# if line[index*2] == word:
			# 	continue
 			if line[index*2] not in word_hash:
				word_hash[line[index*2]]=0
			word_hash[line[index*2]]+=int(line[index*2+1])

	word_count=0.0
	cursor.execute(query2,(word,))
	results=cursor.fetchall()
	for item in results:
		word_count+=float(item["count"])

	sorted_word_hash = sorted(word_hash.iteritems(), key=operator.itemgetter(1), reverse=True)

	other_count={}
	num=0
	for key in sorted_word_hash:
		if num>60:
			break
		cur_count=0.0
		cursor.execute(query2,(key[0],))
		results=cursor.fetchall()
		for item in results:
			cur_count+=float(item["count"])
		other_count[key[0]]=cur_count
		num+=1


	num=0
	for item in sorted_word_hash:
		if item[0]==word:
			continue
		if word_hash[item[0]]>other_count[item[0]]:
			print item[0]+"\t"+str(item[1])+"\t"+str(word_count)+"\t"+str(other_count[item[0]])+"\t"+str(other_count[item[0]])
		else:
			print item[0]+"\t"+str(item[1])+"\t"+str(word_count)+"\t"+str(other_count[item[0]])+"\t"+str(word_hash[item[0]])
		num+=1
		if num==50:
			break
	end=time.clock()
	print "sql时间：%f" % (sql_time)
	print "计算时间：%f" % (end-start)

'''
MI=log(f(x,y)/N)-log((f(x)/N)*(f(y)/N))
其中：f(x,y)--在当前查找范围内共现的次数
f(x)----关键词在整个语料库中的出现次数
f(y)----上下文中的该词在整个语料库中的出现次数
N-------语料库大小
'''
def compute_mutual_info(count1,count2,count3):
	N=20717699.0
	MI=log(N)+log(count3)-log(count2)-log(count1)
	return MI

def search_by_mi(word,month1="1",month2="120",total_count=10):
	cnx = MySQLdb.connect(user="root", passwd="roo", host="127.0.0.1",db="by_work",charset="utf8", \
		cursorclass=MySQLdb.cursors.DictCursor)
	cursor = cnx.cursor()
	query1 = ("SELECT word_set FROM paper_simple WHERE word= %s and month between %s and %s")
	query2 = ("SELECT count FROM paper_simple WHERE word= %s and month between %s and %s")
	start=time.clock()
	cursor.execute(query1,(word,month1,month2))
	cnx.commit()
	results=cursor.fetchall()
	end=time.clock()
	sql_time=end-start
	if len(results)==0:
		print "没有查询到该词!"
		return []
	#return
	#共现词-频次哈希
	word_hash={}
	word_hash.clear()
	start=time.clock()
	for item in results:
		line=item["word_set"].strip().split(" ")
		index_len=len(line)/2
		for index in xrange(index_len):
 			if line[index*2] not in word_hash:
				word_hash[line[index*2]]=0
			word_hash[line[index*2]]+=int(line[index*2+1])
	#查询词word出现次数：word_count
	word_count=0.0
	cursor.execute(query2,(word,month1,month2))
	results=cursor.fetchall()
	for item in results:
		word_count+=float(item["count"])
	#以共现次数为标准筛选top n
	n=200
	sorted_word_hash = sorted(word_hash.iteritems(), key=operator.itemgetter(1), reverse=True)
	
	mutual_info={}#互信息
	other_count={}#另一个词的出现次数
	num=0
	for key in sorted_word_hash:
		if num>n:
			break
		cur_count=0.0
		cursor.execute(query2,(key[0],month1,month2))
		results=cursor.fetchall()

		for item in results:
			cur_count+=float(item["count"])
		num+=1
		if cur_count<10:
			num+=1
		other_count[key[0]]=cur_count
		mutual_info[key[0]]=compute_mutual_info(word_count,cur_count,float(word_hash[key[0]]))
	#以互信息为标准筛选top n
	n=total_count
	sorted_mutual_info = sorted(mutual_info.iteritems(), key=operator.itemgetter(1), reverse=True)
	num=0
	ret_data=[]
	for item in sorted_mutual_info:
		#print item[0]+"\t"+str(item[1])+"\t"+str(word_count)+"\t"+str(other_count[item[0]])+"\t"+str(word_hash[item[0]])
		ret_data.append(item[0])
		num+=1
		if num==n:
			return ret_data

def search():
	while(1):
		word=raw_input("请输入要查询的词:")
		#time1=raw_input("请输入第一个时间节点:")
		#time2=raw_input("请输入第二个时间节点:")
		#time3=raw_input("请输入第三个时间节点:")
		#time4=raw_input("请输入第四个时间节点:")
		#month1=str(int(time1.strip().split()[1])+12*(int(time1.strip().split()[0])-2005))
		#month2=str(int(time2.strip().split()[1])+12*(int(time2.strip().split()[0])-2005))
		#month3=str(int(time3.strip().split()[1])+12*(int(time3.strip().split()[0])-2005))
		#month4=str(int(time4.strip().split()[1])+12*(int(time4.strip().split()[0])-2005))
		print "时间段一："
		#search_by_mi(word,month1,month2)
		search_by_mi(word)
		#print "时间段二："
		#search_by_mi(word,month3,month4)
	return

def collocation_search(word,year,total_count=10):
                month1=1+12*(int(year)-2005)
                month2=12+12*(int(year)-2005)
                return search_by_mi(word,month1,month2,total_count)

if __name__ == '__main__':
	#sql_index_word_md5()
	# take_statistics()
	# for line in open("baozhi_2012.noorder"):
	#  	print line
	print collocation_search("小米",2010,20)
	print "finish"

