# zhilianzhaopin
用scrapy抓取智联招聘职业信息，用css选择器筛选出岗位，公司，薪资，职责，学历要求等
## 获取搜索结果列表 ##
利用chrome 找到搜索返回结果与搜索内容的对应关系，通过format构造动态的url，以便请求不同页面。重写start_request()方法，传入初始爬取的url，并将结果传入第一个解析函数index_parse()，利用正则表达式找出所有的详细信息链接，并调用detail_parse（）。在detail_parse()中利用css选择器提取岗位，公司，薪资，任职要求等详细信息，返回item。在index_parse()中加入判断，若是存在下一页，则回调自己，构成循环，历遍所有结果。
## 将结果存入MongoDB数据库 ##
在Pipeline中加入MongoPipeline(),并将item依次写入Mongodb数据库。在spider结束时，获取数据库中所有拥有任职要求的项，并将所有任职要求合成一个字符串，调用脚本data_deal.py进行处理
## 词频统计 ##
在data_deal脚本中先利用jieba库对字符串进行分割，返回list结果，并利用pandas库对list结果生成DataFrame对象。再读取stopwords.txt对结果进行筛选去除，stopwords可以依据结果在文本文件中进行增删。将筛选过的结果用numpy进行统计出现次数，更新DataFrame
## 词云生成 ##
将DataFrame转化成字典形式，用指定列的方法直接生成，例如：word_frequence = {x[0]: x[1] for x in words_stat.head(100).values。或者利用iterrows()历遍，并生成字典。将字典传入word_cloud()函数中，利用generate_from_frequencies生成词云，设置词云各项属性