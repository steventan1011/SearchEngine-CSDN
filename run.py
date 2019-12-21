from flask import Flask, render_template, url_for, redirect, request, Response
import flask
from flask_wtf import Form
from wtforms import Form as baseform
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Text, DateTime
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import BackEndRank
import json
import sys
import jieba
import pymysql
pymysql.install_as_MySQLdb()
sys.path.append(r'C:\IR')
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/csdn'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = 's12saf123f'
WTF_CSRF_ENABLED = False
WTF_CSRF_CHECK_DEFAULT = False


def VSM_search(query, inverted_index, idf, urls, tag, name):
    # 查标题
    temp_list = []
    c = jieba.cut_for_search(query)
    terms = [a for a in c]
    length = len(terms) * 0.8
    for blog in name:
        sum = 0
        for t in terms:
            if t in blog:
                sum += 1
        if sum >= length:
            temp_list.append(name[blog])

    temp_list.sort(key=lambda x: int(x['times']), reverse=True)
    temp = [a['url'] for a in temp_list[:10]]


    # 查tag
    num = 0
    if query in tag:
        for u in tag[query]["url"]:
            if (num < 10):
                temp.append(u)
            num += 1

    result_list = temp
    result_list += BackEndRank.VSM_search(query, inverted_index, idf,urls)
    results = []
    for i in result_list:
        a = db.session.query(Result).filter(Result.url == i).first()
        if a:
            results.append(a)
    return results


with open(r"C:\IR\readMe\resultIDF.json", 'r', encoding='utf-8') as f:
    idf = f.read()
    idf = json.loads(idf)["data"]
    f.close()
with open(r"C:\IR\readMe\resultURLS.json", 'r', encoding='utf-8') as f:
    urls = f.read()
    urls = json.loads(urls)["data"]
    f.close()
with open(r"C:\IR\readMe\resultInverse.json", 'r', encoding='utf-8') as f:
    inverted_index = f.read()
    inverted_index = json.loads(inverted_index)["data"]
    f.close()
with open(r"C:\IR\readMe\blog_name.json", 'r', encoding='utf-8') as f:
    name = f.read()
    name = json.loads(name)["data"]
    f.close()
with open(r"C:\IR\readMe\tag.json", 'r', encoding='utf-8') as f:
    tag = f.read()
    tag = json.loads(tag)["data"]
    f.close()


class Result(db.Model):
    __tablename__ = 'blogs'
    url = db.Column(String(100),nullable=False)
    blog_name = db.Column(String(100), nullable=False, primary_key=True)
    author = db.Column(Text)
    read_times = db.Column(Integer)
    uptime = db.Column(String(100))
    tag = db.Column(Text)
    content = db.Column(Text)
    nextURLs = db.Column(Text)

    def __repr__(self):
        return "<Model Result `{}`’>".format(self.url)

    def toDict(self):
        return_dict = {'url':self.url,
                       'blog_name':self.blog_name,
                       'author':self.author,
                       'read_times':self.read_times,
                       'content':self.content,
                       'tag':self.tag,
                       'netxURLs':self.nextURLs}
        return  return_dict


class SearchForm(FlaskForm):
    query = TextField('', [DataRequired()])
    submit = SubmitField('submit')


@app.route('/',methods=['GET', 'POST'])
def SearchIndex():
    search_col = SearchForm()
    query = ''
    if search_col.validate():
        query = search_col.query.data
        return redirect(url_for('result', query=query))
    return render_template('index.html', form=search_col, title='CSDN搜索引擎-信息资源管理大作业')

@app.route('/wechatResult/<query>')
def resultforWechat(query):
    result_list = VSM_search(query, inverted_index, idf, urls, tag, name)
    result = [str(json.dumps(a.toDict(), ensure_ascii=False)) for a in result_list]
    text = '['
    text += ','.join(result)
    text += ']'
    print(text)
    return Response(text,mimetype='application/json')

@app.route('/result/<query>',methods=['POST', 'GET'])
def result(query):
    search_col = SearchForm()
    if search_col.validate():
        query = search_col.query.data
        return redirect(url_for('result', query=query))
    result_list = VSM_search(query,inverted_index,idf,urls, tag, name)
    return render_template('searchresult.html',result = result_list,form=search_col)


if __name__ == '__main__':
    app.run(debug = False,use_reloader=False)
