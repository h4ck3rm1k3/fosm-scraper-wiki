import zipfile 
import mechanize
import bz2
def firstitem() : "xaaaa"
def lastitem() : "xachy"
import tarfile  
import string
from cStringIO import StringIO
import struct
from io import BytesIO
import string
import StringIO
import distutils.dir_util
import tarfile
from bs4 import BeautifulSoup

import sys, logging
import mechanize
import tarfile
import os

class Indexer :

    # write a line to the results.txt
    def logdata(self,dirpath,val,cmd) :
        self.of.write(cmd)

# this function unpacks a binary node idex, add the data to the results.txt
    def readnodes (self,fname,member,position,block, data) :    
        f = StringIO.StringIO(data)
        pos=0
        byte = f.read(4)
        while byte != "":
            value = struct.unpack('i', byte)
            if (value[0]>0) :
                val = "%d" % value[0]
                split = '/'.join(list(val))
                dirpath= '/mnt/index/nodes/%s' % split                
                cmd ="%s,%s,%s,%s\n"  % (fname,member,pos,value[0]);
                self.logdata(dirpath,val,cmd)
                pos=pos+4
            byte = f.read(4)

    def readindex(self,fname,zipfile,position,block):
        data = self.indexfile.read()
        myfileobj = StringIO.StringIO(data)
        mytarfile = tarfile.open(mode="r:bz2", fileobj =myfileobj)
        for member in mytarfile.getnames():
            if member.endswith("node_ids.bin") :
                nodes=mytarfile.extractfile(member).read()
                self.readnodes(fname,member,position,block,nodes)

    def rununzip(self,fname,position,block,data):
        output = StringIO.StringIO()
        output.write(data)
        zf = zipfile.ZipFile(output, mode='r')
        self.zipfile=zf
        il= zf.infolist()
        for zi in il :
            print("%s %s" % (fname,zi.filename))
            d = zf.open(zi)
            self.indexfile=d
            self.readindex (fname,zi.filename,position,block)

    def downloaddatafile(self,str,fname) :
        self.fd=open ("%s.zip" % fname , 'w')
#        self.fd2=open ("%s_data.html" % fname, 'w')
#        logger = logging.getLogger("mechanize")
#        logger.addHandler(logging.StreamHandler(self.fd2))
#        logger.setLevel(logging.DEBUG)        
        x = { "block" : 1, "position" : 1 , "name" : str }
        block = x["block"]
        position = x["position"]
        name = x["name"];
        position=x["position"];
        block=x["block"];
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
        uri_overview=  "%s%s/%s.zip" % (baseuri,name,name)
        print(uri_overview)
        br = mechanize.Browser()
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        br.set_handle_robots(False)
        uri_listing=  "%s%s/" % (baseuri,name)        
        print(uri_listing)
        try :
            dataconn = br.open(uri_listing)
            print(dataconn.info)
            print(dataconn.geturl)
            datalisting = br.open(uri_listing).read()
#            self.fd2.write(datalisting)
            soup = BeautifulSoup(datalisting)
            data = br.open(uri_overview).read()
            self.fd.write(data)        
#            self.rununzip(fname,position,block,data)
        except:
            print "error!"

        self.fd.close()
#        self.fd2.close()


    def downloadindexfile(self,str,fname) :
        self.fd=open (fname, 'w')
#        self.fd2=open ("%s.html" % fname, 'w')
#        logger = logging.getLogger("mechanize")
#        logger.addHandler(logging.StreamHandler(self.fd2))
#        logger.setLevel(logging.DEBUG)        
        x = { "block" : 1, "position" : 1 , "name" : str }
        block = x["block"]
        position = x["position"]
        name = x["name"];
        position=x["position"];
        block=x["block"];
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
        uri_overview=  "%s%s/%s_index.zip" % (baseuri,name,name)
        print(uri_overview)
        br = mechanize.Browser()
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        br.set_handle_robots(False)
        uri_listing=  "%s%s/" % (baseuri,name)        
        print(uri_listing)
        try :
            dataconn = br.open(uri_listing)
            print(dataconn.info)
            print(dataconn.geturl)
            datalisting = br.open(uri_listing).read()
#            self.fd2.write(datalisting)
            soup = BeautifulSoup(datalisting)
            data = br.open(uri_overview).read()
            self.fd.write(data)        
            self.rununzip(fname,position,block,data)
        except:
            print "error! getting zip"
            self.downloaddatafile(str,fname)


        self.fd.close()
#        self.fd2.close()

    def processindexfile(self,str,fname) :
        x = { "block" : 1, "position" : 1 , "name" : str }
        block = x["block"]
        position = x["position"]
        name = x["name"];
        position=x["position"];
        block=x["block"];
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
        uri_overview=  "%s%s/%s_index.zip" % (baseuri,name,name)
        self.fd = open(fname, "r")
        data = self.fd.read()
        self.rununzip(fname,position,block,data)
        self.fd.close()

    def process(self):
        data = []
        if (not os.path.isdir("cache")) :
            os.mkdir("cache");
        print(list(string.lowercase ))
        print(string.lowercase)
        self.of=open ('results_new.txt' , 'w')

        for l in list(string.lowercase ):
            for l2 in list(string.lowercase):
                for l3 in list(string.lowercase) : 
                    str = 'xa%s%s%s' % (l,l2,l3)
                    print(str)
                    if str == "xachz" :
                        return 
                    fname = "%s/%s"  % ( "cache", str )
                    if (not os.path.isfile(fname)) :
                        self.downloadindexfile(str,fname)
                    
                    self.processindexfile(str,fname)                    
        self.of.close()
 
def main():    
    i=Indexer()    
    i.process ()
 
main()
