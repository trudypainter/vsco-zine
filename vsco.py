from datetime import datetime
import requests, json, time, datetime

################################
##  CONSTANTS FOR VSCO CLASS  ##
################################

visitvsco = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"en-US,en;q=0.9",
    "Connection":"keep-alive",
    "Host":"vsco.co",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }

visituserinfo = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"en-US,en;q=0.9",
    "Connection":"keep-alive",
    "Host":"vsco.co",
    "Referer":"http://vsco.co/bob/images/1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    }

media = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"en-US,en;q=0.9",
    "Connection":"keep-alive",
    "Host":"vsco.co",
    "Referer":"http://vsco.co/bob/images/1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "X-Client-Build":"1",
    "X-Client-Platform":"web",
    }

################################
##         VSCO CLASS         ##
################################
class VSCO:

    def __init__(self, username):

        # INITIALIZATION COOKIES/UID 
        self.username = username
        self.session = requests.Session() 
        self.session.get("http://vsco.co/content/Static/userinfo?callback=jsonp_%s_0" %(str(round(time.time()*1000))),\
                    headers=visituserinfo)
        self.uid = self.session.cookies.get_dict()['vs']
        
        res = self.session.get("http://vsco.co/ajxp/%s/2.0/sites?subdomain=%s" % (self.uid,self.username))
        self.siteid = res.json()["sites"][0]["id"]
        
        # GET JSON OF ALL IMAGE INFO
        self.mediaurl = "http://vsco.co/ajxp/%s/2.0/medias?site_id=%s" %(self.uid,self.siteid)
        self.image_json = self.session.get(self.mediaurl,params={"size":1000,"page":1},\
                             headers=media).json()["media"]
    
    def __iter__(self):
        for image in self.image_json:
           yield image 

    def __getitem__(self, ix):
        return self.image_json[ix] 