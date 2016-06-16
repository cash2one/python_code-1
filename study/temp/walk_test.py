#!/usr/bin/python
import os,pdb

fileDir = "/home/qa"
pdb.set_trace()
for root, dirs, files in os.walk(fileDir):  
    #begin  
    print(root)  
    print(dirs)  
    print(files) 
