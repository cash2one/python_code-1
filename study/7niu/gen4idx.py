# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''自动生成所有目录的 index.html
Version:
    + 13.4.18 增补meta 停息,以免乱码
    + 13.4.17 增补多层目录中的目录/文件链接 (7牛没有目录概念)
    + 13.4.11 可用
'''
import os
import sys

count = 0
def genall(dir, tpl , exclude):
    global count
    VER = "gen4idx.py v13.4.18"
    tplIDX = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8" />
<meta name="generator" content="gen4idx.py v13.4.18" />
<title>Index of %(crtROOT)s {gen. by %(VER)s}</title></head>
<body>
<h1>Index of %(crtROOT)s</h1><hr>
<pre><a href="%(crtROOT)s/..">../</a>
%(crtFILES)s
</pre>
%(footer)s
</body></html>
    """
    crtROOT = dir[1:]
    footer = open(tpl).read()
    #print footer
    crtDIR = ""
    crtFILE = ""
    for i in os.listdir(dir):
        file = os.path.join(dir,i)
        if os.path.isdir(file):
            if exclude in file:
                pass
            else:
                print file[1:]
                crtDIR += "<a href='%s'>%s/</a>\n"% (file[1:], i)
                genall(file, tpl , exclude)
        else:
            if ".DS_Store" in i:
                pass
            elif ".json" in i:
                pass
            elif "index.html" in i:
                pass
            else:
                fstat = os.lstat(file)
                #print type(fstat.st_size)
                if 1000000 < fstat.st_size:
                    #print "%.2fM"% (fstat.st_size/1000000.0)
                    fsize = "%.2fM"% (fstat.st_size/1000000.0)
                else:
                    #print type(fstat.st_size/1024.0)
                    #print "%.2f"% (fstat.st_size/1024.0)
                    fsize = "%.2fk"% (fstat.st_size/1024.0)

                crtFILE += "<a href='%s/%s'>\n%- 79s % 20s"% (crtROOT, i, "%s</a>"%i, fsize)
                pass
                #print file
    print ">>>", dir[1:]
    #print crtDIR, "\n", crtFILES
    crtFILES = "%s%s"% (crtDIR, crtFILE)

    #print locals()
    #print tplIDX% locals() 
    count += 1
    open("%s/index.html"% dir, "w").write(tplIDX% locals())


if __name__ == '__main__':
    if 4 != len(sys.argv) :
        print '''Usage:
gen4idx.py /path/2/gen /path/2/foot.html[模板] excludePath
        '''
    else:
        startPath = sys.argv[1]
        fooTpl = sys.argv[2]
        excludePath = sys.argv[3]
        genall(startPath, fooTpl, excludePath)
        print "gen %s index.html"% count