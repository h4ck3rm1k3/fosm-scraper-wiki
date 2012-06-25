import bz2
import distutils.dir_util
import io
import os
import string
import struct
import sys
import logging
import tarfile  
import zipfile 

def firstitem() : "xaaaa"
def lastitem() : "xachy"


class Indexer :

    # write a line to the results.txt
    def logdata(self,dirpath,val,cmd) :
        self.of.write(cmd)

# this function unpacks a binary node idex, add the data to the results.txt
    def readnodes (self,fname,member, data) :    
        datalen = sys.getsizeof(data)
        f = io.BytesIO(data)
        pos=0
        byte = f.read(4)
        while byte != b'':
            len = sys.getsizeof(byte)
            if len == 37 :
                value = struct.unpack('i', byte)
                if (value[0]>0) :
                    val = "%d" % value[0]
                    split = '/'.join(list(val))
                    dirpath= '/mnt/index/nodes/%s' % split                
                    cmd ="%s,%s,%s,%s\n"  % (fname,member,pos,value[0]);
                    self.logdata(dirpath,val,cmd)
            else:
                print("error, did not get 37 %d %s %d %d" % (len, byte, pos, datalen ) )

            pos=pos+4
            byte = f.read(4)


    def readindex(self,fname,zipfile):
        data = self.indexfile.read()
        myfileobj = io.BytesIO(data)
        mytarfile = tarfile.open(mode="r:bz2", fileobj =myfileobj)
        for member in mytarfile.getnames():
            if member.endswith("node_ids.bin") :
                nodes=mytarfile.extractfile(member).read()
                self.readnodes(fname,member,nodes)

    def rununzip(self,fname):
        zf = zipfile.ZipFile(fname, mode='r')
        self.zipfile=zf
        il= zf.infolist()
        for zi in il :
            print("%s %s" % (fname,zi.filename))
            d = zf.open(zi)
            self.indexfile=d
            self.readindex (fname,zi.filename)


    def processindexfile(self,str,fname) :
#        x = { "block" : 1, "position" : 1 , "name" : str }
#        block = x["block"]
#        position = x["position"]
#        name = x["name"];
#        position=x["position"];
#        block=x["block"];
#        self.fd = open(fname, "r")
#        data = self.fd.read()
        self.rununzip(fname)
#        self.fd.close()

    def process(self):
        data = []
        if (not os.path.isdir("cache")) :
            os.mkdir("cache");

        self.of=open ('results_new.txt' , 'w')
        letter_list = list(string.ascii_lowercase )

        for l in letter_list:
            for l2 in letter_list:
                for l3 in letter_list: 
                    str = 'xa%s%s%s' % (l,l2,l3)
                    print(str)
                    if str == "xachz" :
                        return 
                    fname = "%s/%s"  % ( "cache", str )
                    if (not os.path.isfile(fname)) :
                        print("missing data %s" % fname)
                    
                    self.processindexfile(str,fname)                    
        self.of.close()
 
def main():    
    i=Indexer()    
    i.process ()
 
main()
