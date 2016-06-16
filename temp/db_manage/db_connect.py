import MySQLdb
import pdb

def db_conn():
    host="127.0.0.1"
    user="root"
    passwd="miles.peng"
    db="miles01"
    #pdb.set_trace()
    con=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
    return  con

def db_select(con):
    cur=con.cursor()
    sql="select * from test;"
    cur.execute(sql)
    data=cur.fetchall()
    desc=cur.description

    print "%s %3s %5s"%(desc[0][0],desc[1][0],desc[2][0])
    for data_onerow in data:
        print data_onerow
        #print data_onerow["id"],data_onerow["name"]

def db_insert(con,id,name):
    cur=con.cursor()
    sql="insert miles01.test values (%d,'%s',now())"%(int(id),name)
    print sql
    cur.execute(sql)
    con.commit()





if __name__=="__main__":
    con=db_conn()
    db_insert(con,3,"miles1")
    db_select(con)
    if con:
        con.close()



