import  urllib2

def check_url(url,values):
    req=urllib2.Request(url)
    response= urllib2.urlopen(req)
    html=response.read()
    
