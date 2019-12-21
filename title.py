import json
import mysql.connector


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

    data = {}
    i = 0

    while True:
        try:
            flag = 1
            conn = mysql.connector.connect(
                user='root',
                password='1234',
                host='39.105.186.225',
                port='3306',
                database='csdn'
            )
            cursor = conn.cursor(buffered=True)
            sql_query = 'select url, blog_name, read_times from blogs;'
            cursor.execute(sql_query)
            for url, blog_name, read_times in cursor:
                if blog_name in data:
                    continue
                names = {}
                names['url'] = url
                names['times'] = read_times
                data[blog_name] = names
                i += 1
                print(url, i)
            # print('************** %s 数据保存成功 **************' % data[url])
            conn.commit()
            cursor.close()
        except (mysql.connector.errors.IntegrityError, mysql.connector.errors.DataError, mysql.connector.errors.OperationalError) as e:
            flag = 0
        if flag == 1:
            break

    with open("C:/IR/readMe/blog_name.json", 'w', encoding='utf-8') as f:
        d = {}
        d["data"] = data
        f.writelines(json.dumps(d, indent=4) +'\n')
        f.close()








