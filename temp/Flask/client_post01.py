import  requests

user_info={'name':'miles.peng'}

r=requests.post("http://127.0.0.1:5000/auto_reload",data=user_info)
print r.text