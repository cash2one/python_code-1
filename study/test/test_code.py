#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

def run08():
    for row in range(1,10):
        num_line=[]
        for line in range(1,10):

            num=row*line
            num_line.append(num)
        print num_line


def run11():
    from collections import deque
    rabbit_num=1
    old=1
    grow=2
    month=1
    rabbit_new=deque()
    while 1:
        month+=1
        new_=0
        if len(rabbit_new)<grow:
            new_=0
            rabbit_new.append(new_)
        elif len(rabbit_new)==grow:
            # new_=rabbit_num-rabbit_new[-1]
            # rabbit_new.append(new_)
            # rabbit_num+=new_
            # rabbit_new.popleft()
            grow_old=rabbit_new.popleft()
            old+=grow_old
            new_=old
            rabbit_new.append(new_)
            rabbit_num=old+new_+rabbit_new[0]

        else:
            print "Queue error",rabbit_new
            break
        print "Month :",month,"\tRabbit Num was :",rabbit_num
        print "Old rabbit :",old,"\t Baby :",rabbit_new
        if rabbit_num>1000:
            print "Bomb rabbit is every where"
            break

def run20():
    Hn=100
    Fn=float(Hn)/2
    total=0

    for i in range(2,11):
        total+=2*Fn
        Fn=Fn/2

    print "Total was: ",total,"\tLast High was:",Fn
def run21():
    team1=["a","b","c"]
    team2=["x","y","z"]
    choice=[]
    for i in range(len(team1)):
        pass






def main():
    run21()

if __name__=="__main__":
    main()
