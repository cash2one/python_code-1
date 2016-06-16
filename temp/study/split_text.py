import  string
import  re
import pdb
def replace_word(text,key,change_to):
    #link=re.compile(key)
    new_text=text.replace(key,change_to)

   # new_text=re.sub(key,change_to,text)
    return new_text


input_file=r'D:\code\send_report\study\pg1952.txt'

with open (input_file,'r') as f:
    data=f.read()
#pdb.set_trace()
data=data.replace("\n"," ")
new=data
split_word=string.whitespace+string.punctuation
print "split_word is %s"%split_word
_split_word="[%s]"%split_word
link=re.compile(_split_word)
_data=re.sub(link," ",data)

#
# for _split in split_word:
#     new=replace_word(text=new,key=_split,change_to=" ")
#

#print new

list_new=new.split(" ")
data_dict=dict()
for a in list_new:
    if data_dict.get(a.lower(),None)==None:
        data_dict[a.lower()]=1
    else:
        data_dict[a.lower()]+=1
print sorted(data_dict.items(), key=lambda x:x[1], reverse=True)

print data_dict.keys()
print len(data_dict.keys())


