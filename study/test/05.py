#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

input_num=[]
while 1:
    num=int(raw_input("Num :\n"))
    input_num.append(num)
    if num==0:
        break

input_num.sort()
print input_num