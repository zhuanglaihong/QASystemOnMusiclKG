# QABasedOnMusicKnowledgeGraph

学习了刘焕勇老师的问答系统后，我自己尝试使用模板匹配搭建一个音乐领域的知识图谱QA系统，数据来源于现成的文件，网址为http://www.openkg.cn/dataset/163music
数据库使用的是neo4j-community-5.6.0-windows和jdk-17.0.5

# 项目介绍
本项目将包括以下两部分的内容：
1) 基于网易云音乐的音乐图谱构建
2) 基于医药知识图谱的自动问答，并设计了UI界面

# 项目UI效果
UI截图：左上角的使用说明中包含有问句提示
![image](https://github.com/zhuanglaihong/QASystemOnMusiclKG/blob/master/img/demo2.png)

在文本框中输入问句，按下开始即可回答，点击清除即可清屏
![image](https://github.com/zhuanglaihong/QASystemOnMusiclKG/blob/master/img/demo1.png)

# 项目运行方式
1、配置要求：要求配置neo4j数据库及相应的python依赖包。neo4j数据库用户名密码记住，并在对应位置修改相应文件。这里我  
2、知识图谱数据导入：python build_music.py，运行时间预计30-40分钟。  
3、启动问答界面：python UI.py

## 以下介绍详细方案
# 一、音乐知识图谱构建

# 1 脚本
build_music.py：知识图谱入库脚本    　　

# 2 基于neo4j的知识图谱
![image](https://github.com/zhuanglaihong/QASystemOnMusiclKG/blob/master/img/neo4j.png)

|  实体类型 |  实体关系类型 | 属性键 |
| :--- | :---: | :---: |
| 歌曲 | 演唱 | name |
| 歌手 | 歌手发布 | 歌手 |
| 专辑 | 归属专辑 | 专辑|
| 歌曲内容 | 歌曲内容 | 歌曲内容 |
| 歌单 | 歌单 | 歌单 |
|  | 相似歌曲 | 相似歌曲 |



# 二、基于知识图谱的自动问答

# 1. 脚本结构
question_classifier.py：问句类型分类脚本  
question_parser.py：问句解析脚本  
answer_search.py：问句回答脚本  
chatbot_graph.py：图谱问答脚本  
UI.py：设计的UI界面交互脚本  

# 2.3　支持问答类型

| 问句类型 | 中文含义 | 问句举例 |
| :--- | :---: | :---: |
|1.song_desc 	|	歌曲描述(回答歌词的信息)	  |  爱情转移 |
|2.artist_desc	|	歌手描述(回答歌曲+专辑)	  |  陈奕迅|
|3.artist_name	|	歌曲演唱者(问的是某一首歌是谁唱的)	 |   红玫瑰的演唱者是谁|
|4.artist_song	|	歌手唱的歌(回答歌手的所有曲子)	  |  陈奕迅唱的歌|
|5.album_artist	|	专辑属于哪个歌手(回答发布专辑的歌手)	 |   陈奕迅发布的专辑|
|6.album_song	|	专辑包含的歌曲(回答专辑下的曲目)	 |   三人主义包含有什么歌|
|7.similar_songs	|	相似歌曲推荐(回答相似歌曲)	 |   和红玫瑰类似的歌有什么|
|8.playlist_song	|	歌单里的歌曲(回答歌单)	 |   包含红玫瑰的歌单有什么|

# 总结
１、本项目参考QABasedOnMedicalKnowledgeGraph，构建起以歌曲为中心的音乐知识图谱，实体规模3.5万，实体关系规模13万，搭建起了一个可以回答8类问题的问答QA系统。    
2、本项目以neo4j作为存储，并基于模板匹配的方式完成了知识问答，并最终以cypher查询语句作为问答搜索sql，支持了问答服务。  
3、本项目可以快速部署，数据已经放在data/163music.json当中，本项目的数据来源于网络，不是使用爬虫爬取，所以节点与关系的类型较少。
4、自行设计的UI界面，界面交互更友好

# 不足
1、没有使用网络模型，后面进行尝试增加。 
2、数据应该尝试自己爬取，节点类型才能多种多样。
2.在问题类型'artist_desc'中的回答是问题'artist_song'和'album_artist'的简单结合，没有额外的歌手信息。
3.输入问题时有时候会识别到多个歌曲类型，例如：输入歌曲'晴天'有时候会返回歌曲'晴'，分词处理上还要加强。

------------------------更新于2023.4.21------------------------


作者邮箱：994182204@mail.dlut.edu.cn 
