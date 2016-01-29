北语：语义历时变化项目文档
====
#服务器框架
服务器搭建主要依赖于：

* Web.py： 网站框架
* Nginx：服务器框架
* Spawn-fcgi：网站和服务器之间的连接通道
* Flup：Python包，和Python的网络服务有关，相当于web.py和之前两个服务器上的应用的连接
* MongoDB：负责存储查询过的最近词信息

具体的搭建网站的步骤见[这里](http://webpy.org/cookbook/fastcgi-nginx.zh-cn)或者[这里](http://webpy.org/cookbook/fastcgi-nginx)

#具体流程
主要流程有三步：

1. **数据的预处理**：原始数据的格式要求为每年一个文件，每个文件含有多行文本，每行文本可以是一句话、一个段落或者一篇文章，对于文本的长度不做限制，但是要求文本用空格进行分词。
2. **学习词向量表示**：学习词向量，用到了word2vec这个工具，在本项目中使用的是word2vec的python版本，即gensim包，具体关于该工具中word2vec的介绍见[这里](https://radimrehurek.com/gensim/models/word2vec.html)
3. **新语义聚类**：即网站的主体功能，也是项目最主要的部分。

#项目组织
目前项目组织来源于两部分，后台数据服务部分和网站部分。

后台数据服务负责载入原始的词向量数据并提供基础的服务：如根据请求词返回K邻近词语并存入数据库、根据请求词返回其词向量。后台数据服务独立运行，与网站主体耦合性较小，也就是说，网站的关闭并不会影响其运行。数据请求以python远程调用的方式实现。

网站部分负责根据词向量和临近词进行聚类，得到语义变化；同时负责网站的相应，如访问请求，页面生成等。

#项目启动与关闭
项目的主目录在`/websites/WordPlatform-Beiyu`目录下，下面的操作默认都是在该目录下进行。
##数据库启动
本项目依赖于MongoDB数据库，数据库不是默认启动的，所以要先尝试启动数据库，在命令行输入以下命令：

	mongod -logpath /data/db/mongo.log -fork
	
该命令可以令MongoDB在后台运行

##启动远程调用程序
网站的作用是内容呈现，而数据计算部分交给远程调用程序进行，在主目录下输入下面一条命令

	nohup python word_embedding_handler.py&
	
该程序包含了数据载入的过程，因此可能耗时较长（20分钟），验证是否载入完成的方法有两种。

一种是查看输出，输出的存放文件是`nohup.out`，在终端输入

	cat nohup.out
	
如果对应的输出为

	
	Add embedding file of all
	Done
	Add embedding file of 2005
	Done
	Add embedding file of 2006
	Done
	Add embedding file of 2007
	Done
	Add embedding file of 2008
	Done
	Add embedding file of 2009
	Done
	Add embedding file of 2010
	Done
	Add embedding file of 2011
	Done
	Add embedding file of 2012
	Done
	Add embedding file of 2013
	Done

则表示没有已经载入完成。

另一种方法是输入

	python deliver.py
	
若可以正常输出则表示载入完成。

##启动网站主程序

输入

	./start.sh

若**最后一行输出**为

	spawn-fcgi: child spawned successfully: PID: 【num】

（num表示数字，意为进程号）则表示正常启动

若**最后一行输出**为

	spawn-fcgi: bind failed: Address already in use

则表示网站主程序已经处于运行状态，此时若仍想重新启动，需要先关闭网站主程序，关闭方法见下一节内容

##关闭网站主程序

输入

	./stop.sh

若无输出，表示正常关闭；否则表示没有找到网站主程序，即说明网站主程序本来就不在运行状态。

#网站功能

