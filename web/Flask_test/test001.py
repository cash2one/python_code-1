from flask import Flask,request
from  flask import render_template
import MySQLdb
import pdb
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        name="aaa"
    else:
        name="bbb"
    return "Hello world! \t I am Miles"+name

@app.route('/add/<name>',methods=['GET','POST'])
def add_to_db(name=None):
    #pdb.set_trace()
    if name:
        host="127.0.0.1"
        user="root"
        passwd="miles.peng"
        db="miles01"

        con=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
        cur=con.cursor()

        sql="insert miles01.test (NAME,create_time) VALUES ('%s',now())"%name
        cur.execute(sql)
        con.commit()
        return "values add to DB"

@app.route('/auto_reload',methods=['POST'])
def auto_reload():
    host="127.0.0.1"
    user="root"
    passwd="miles.peng"
    db="miles01"

    con=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
    cur=con.cursor()
    sql="insert miles01.test (NAME,create_time) VALUES ('%s',now())"%request.form.get('name',default='little apple')
    cur.execute(sql)
    con.commit()
    return "%s has insert into db"%request.form.get('name',default='little apple')


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)