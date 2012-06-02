 
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
import zipfile
import distutils.dir_util


import tarfile
from bs4 import BeautifulSoup

import sys, logging
import mechanize
import tarfile
import os

class Indexer :

    def addtar1(self,dirpath,val,cmd) :
        string = StringIO.StringIO()
        string.write(cmd)
        string.seek(0)
        info = tarfile.TarInfo(name=dirpath)
        info.size=len(string.buf)
        self.tar.addfile(tarinfo=info, fileobj=string)

    def addtar2(self,dirpath,val,cmd) :
        string = StringIO.StringIO()
        string.write(cmd)
        string.seek(0)
        info = tarfile.TarInfo(name=dirpath)
        info.size=len(string.buf)
        self.tar.addfile(tarinfo=info, fileobj=string)
        info.name=val #
        string.seek(0)
        self.tar2.addfile(tarinfo=info, fileobj=string)
        self.zip.writestr(dirpath, cmd)
        self.zip2.writestr(val, cmd)

    def addzip(self,dirpath,val,cmd) :
        self.zip.writestr(dirpath, cmd)

    def addzip2(self,dirpath,val,cmd) :
        self.zip2.writestr(val, cmd)


    def adddata(self,dirpath,val,cmd) :
        distutils.dir_util.mkpath(dirpath)
        of=open ('%s/data.txt' % dirpath, 'w')        
        of.write(cmd)
        of.close()

#zip -0 -r /mnt/target/node_index/node_index.zip /mnt/target/index/

    def readnodes (self,fname,member,position,block, data) :    
        f = StringIO.StringIO(data)
        pos=0
        byte = f.read(4)
        while byte != "":
            value = struct.unpack('i', byte)
            if (value[0]>0) :
                val = "%d" % value[0]
                split = '/'.join(list(val))
#                dirpath= '/mnt/target/index/%s' % split                
                dirpath= '/mnt/index/nodes/%s' % split                
                cmd ="%s,%s,%s,%s\n"  % (fname,member,pos,value[0]);
                self.addzip(dirpath,val,cmd)
#                self.adddata(dirpath,val,cmd)

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

#        exit

    def rununzip(self,fname,position,block,data):
        output = StringIO.StringIO()
        output.write(data)
        zf = zipfile.ZipFile(output, mode='r')
        self.zipfile=zf
        print zf
        il= zf.infolist()
        for zi in il :
            print "%s %s" % (fname,zi.filename)
            d = zf.open(zi)
            self.indexfile=d
            self.readindex (fname,zi.filename,position,block)


    def onefile(self,str,fname) :
        self.fd=open (fname, 'w')
        self.fd2=open ("%s.html" % fname, 'w')
        self.of=open ('%s.results' % fname , 'w')
        logger = logging.getLogger("mechanize")
        logger.addHandler(logging.StreamHandler(fd2))
        logger.setLevel(logging.DEBUG)        
        x = { "block" : 1, "position" : 1 , "name" : str }
        block = x["block"]
        position = x["position"]
        name = x["name"];
        position=x["position"];
        block=x["block"];
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
        uri_overview=  "%s%s/%s_index.zip" % (baseuri,name,name)
        print uri_overview
        br = mechanize.Browser()
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        br.set_handle_robots(False)
        uri_listing=  "%s%s/" % (baseuri,name)        
        print uri_listing
        dataconn = br.open(uri_listing)
        print dataconn.info
        print dataconn.geturl
        datalisting = br.open(uri_listing).read()
        self.fd2.write(datalisting)
        soup = BeautifulSoup(datalisting)
        data = br.open(uri_overview).read()
        self.fd.write(data)        
        self.rununzip(fname,position,block,data)
        self.fd.close()
        self.fd2.close()
        self.of.close()

    def processfile(self,str,fname) :
        x = { "block" : 1, "position" : 1 , "name" : str }
        block = x["block"]
        position = x["position"]
        name = x["name"];
        position=x["position"];
        block=x["block"];
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
        uri_overview=  "%s%s/%s_index.zip" % (baseuri,name,name)
#        self.of=open ('%s.results' % fname , 'w')    
        self.fd = open(fname, "r")
        data = self.fd.read()
        self.rununzip(fname,position,block,data)
        self.fd.close()
#        self.of.close()

    def process(self):
        data = []
        if (not os.path.isdir("cache")) :
            os.mkdir("cache");
        print list(string.lowercase )
        print string.lowercase
#        self.tar = tarfile.open("sample.tar", "w")
#        self.tar2 = tarfile.open("sample2.tar", "w")
        self.zip  = zipfile.ZipFile("sample.zip ",mode= "w")
#        self.zip2 = zipfile.ZipFile("sample2.zip", mode="w")


        for l in list(string.lowercase ):
            for l2 in list(string.lowercase):
                for l3 in list(string.lowercase) : 
                    str = 'xa%s%s%s' % (l,l2,l3)
                    print str
                    if str == "xachz" :
                        return 
                    fname = "%s/%s"  % ( "cache", str )
                    if (not os.path.isfile(fname)) :
                        self.onefile(str,fname)
                    if (not os.path.isfile('%s.results2' % fname)) :
                        self.processfile(str,fname)
                    
#        self.tar.close()
#        self.tar2.close()

        self.zip.close()
#        self.zip2.close()

 
def main():
    
    print "test"
    
    #print genletters (lastitem())
 
    i=Indexer()    
    i.process ()

 
main()
