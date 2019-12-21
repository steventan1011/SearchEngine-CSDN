# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
import re
import jieba
import mysql.connector
import sys
import urllib.parse
import json
import BackEndRank

# 为方便调试 将一些关键数据直接从磁盘中读取 避免重复运行原始函数
def loadData():
    with open("C:/Users/Administrator/desktop/BackPart/readMe/resultIDF.json", 'r', encoding='utf-8') as f:
        IDF = f.read()
        IDF = json.loads(IDF)["data"]
        f.close()
    with open("C:/Users/Administrator/desktop/BackPart/readMe/resultURLS.json", 'r', encoding='utf-8') as f:
        urls = f.read()
        urls = json.loads(urls)["data"]
        f.close()
    with open("C:/Users/Administrator/desktop/BackPart/readMe/resultInverse.json", 'r', encoding='utf-8') as f:
        Inverse = f.read()
        Inverse = json.loads(Inverse)["data"]
        f.close()
    return IDF, urls, Inverse

if __name__ == '__main__':

    # data = {}
    # i = 0
    #
    # while True:
    #     try:
    #         flag = 1
    #         conn = mysql.connector.connect(
    #             user='root',
    #             password='root',
    #             host='39.106.197.210',
    #             port='3306',
    #             database='CSDN'
    #         )
    #         cursor = conn.cursor(buffered=True)
    #         sql_query = 'select url, content from blogs;'
    #         cursor.execute(sql_query)
    #         for url, content in cursor:
    #             if url in data:
    #                 continue
    #             urls = {}
    #             urls['content'] = content
    #             data[url] = urls
    #             i += 1
    #             print(url, i)
    #         # print('************** %s 数据保存成功 **************' % data[url])
    #         conn.commit()
    #         cursor.close()
    #     except (mysql.connector.errors.IntegrityError, mysql.connector.errors.DataError, mysql.connector.errors.OperationalError) as e:
    #         flag = 0
    #     if flag == 1:
    #         break
    #
    # j = 0
    # for url in data:
    #     words = []
    #     print(url, j)
    #     j += 1
    #     file = str(data[url]["content"]).strip('\n')
    #     # print(file)
    #     r = '[’!"#$%&()\'*+,-./:;。，？、‘’“”<=>?@[\\]^_`{|}~]+'
    #     file = re.sub(r, ' ', file)
    #     cut = jieba.cut(file)
    #     temp1 = []
    #     for i in cut:
    #         temp1.append(i)
    #     temp2 = []
    #     for i in temp1:
    #         if not i == ' ':
    #             temp2.append(i)
    #     stop = []
    #     for line in open('C:/Users/Administrator/desktop/BackPart/stopWord.txt', encoding='utf-8'):
    #         stop.append(str(line).strip())
    #     fileNew = []
    #     for i in temp2:
    #         if i not in stop:
    #             fileNew.append(i)
    #
    #     for i in fileNew:
    #         if not i == '\n':
    #             words.append(i)
    #     data[url]["content"] = words
    #     data[url]["length"] = len(words)
    #
    # # for i in data:
    # #     print(data[i])
    #
    # (Tuples, tf, IDF, Articles_length, tf_idf) = BackEndRank.ArtributeCal(data)
    #
    # term = []
    # for i in IDF:
    #     term.append(i)
    # inversal_index = BackEndRank.GetInverseIndex(term, Tuples)
    #
    # # with
    #
    # query = "构造器"
    #
    # # 连php
    # # query = sys.argv[1]
    # query = urllib.parse.unquote(query)
    #
    #
    #
    #
    # with open("C:/Users/Administrator/desktop/BackPart/readMe/resultIDF.json", 'w', encoding='utf-8') as f:
    #     d = {}
    #     d["data"] = IDF
    #     f.writelines(json.dumps(d, indent=4) +'\n')
    #     f.close()
    #
    # urls = {}
    # for url in tf:
    #     urls[url] = {}
    #     urls[url]["tf"] = tf[url]
    #     urls[url]["len"] = Articles_length[url]
    # with open("C:/Users/Administrator/desktop/BackPart/readMe/resultURLS.json", 'w', encoding='utf-8') as f:
    #     d = {}
    #     d["data"] = urls
    #     f.writelines(json.dumps(d, indent=4) +'\n')
    #     f.close()
    #
    # with open("C:/Users/Administrator/desktop/BackPart/readMe/resultInverse.json", 'w', encoding='utf-8') as f:
    #     d = {}
    #     d["data"] = inversal_index
    #     f.writelines(json.dumps(d, indent=4) +'\n')
    #     f.close()
    #
    #
    # result = BackEndRank.VSM_search(query, inversal_index, tf, IDF, Articles_length)
    #
    # for i in result:
    #     print(i)



    # 连php
    query = sys.argv[1]
    query = urllib.parse.unquote(query)

    (IDF, urls, Inverse) = loadData()
    tf = {}
    len = {}
    for i in urls:
        tf[i] = urls[i]["tf"]
        len[i] = urls[i]["len"]
    result = BackEndRank.VSM_search(query, Inverse, tf, IDF, len)
    for i in result:
        print(i)






