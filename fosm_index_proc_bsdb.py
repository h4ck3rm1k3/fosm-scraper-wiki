import bz2
import distutils.dir_util
import io
import re
import os
import string
import struct
import sys
import logging
import tarfile  
import zipfile 
#import bsddb3 as bsddb
from bsddb3 import db, dbtables, dbutils, dbshelve, hashopen, btopen, rnopen, dbobj


def lastitem() : "xachz"

class Indexer :

    def openDB(self):
        self.dbBuckets = dbobj.db.DB()
        self.dbBuckets.open("buckets.bsdb", db.DB_HASH, db.DB_CREATE)

        self.dbBlocks = dbobj.db.DB()
        self.dbBlocks.open("blocks.bsdb", db.DB_HASH, db.DB_CREATE)

        self.dbNodes = dbobj.db.DB()
        self.dbNodes.open("nodes.bsdb", db.DB_HASH, db.DB_CREATE)


# this function unpacks a binary node idex, add the data to the results.txt
    def readnodes (self,bucketfilename,member, data, block) :    
        datalen = sys.getsizeof(data)
        f = io.BytesIO(data)
        pos=0
        byte = f.read(4)
        count=0
        while byte != b'':
            len = sys.getsizeof(byte)
 #           print("got len:%d byte:%s pos:%d datalen:%d" % (len, byte, pos, datalen ) )
            if len == 37 or len == 44:
                value = struct.unpack('i', byte)
                if (value[0]>0) :
                    val = "%d" % value[0]
                    split = '/'.join(list(val))
                    dirpath= '/mnt/index/nodes/%s' % split                
                    self.dbNodes.put(byte,block)
                    count = count + 1
#            else:
                #print("error, did not get 37 %d %s %d %d" % (len, byte, pos, datalen ) )
#                break
            pos=pos+4
            byte = f.read(4)
        #print ("%s %d" % (block, count))

    def readindex(self,bucketfilename,zipfilename,block):
        data = self.indexfile.read()
        myfileobj = io.BytesIO(data)
        mytarfile = tarfile.open(mode="r:bz2", fileobj =myfileobj)
        for member in mytarfile.getnames():
            if member.endswith("node_ids.bin") :
                nodes=mytarfile.extractfile(member).read()
                self.readnodes(bucketfilename,member,nodes,block)

    def rununzip(self,bucketfilename, bucketname):
        zf = zipfile.ZipFile(bucketfilename, mode='r')
        self.zipfile=zf
        il= zf.infolist()
        for zi in il :
            m = re.search("\/(\d+)_i.tbz",zi.filename)
            if (m):
                block = m.group(1)
                self.dbBlocks.put(bytes(block, "ascii"),bucketname) # block number -> bucketname
                #print ("blocks %s -> %s" % (block,bucketname))
            else:
                print ("wtf:%s" % zi.filename)
            d = zf.open(zi)
            self.indexfile=d
            self.readindex (bucketfilename,zi.filename, block)

    def process(self):
        data = []
        if (not os.path.isdir("cache")) :
            os.mkdir("cache");
        letter_list = list(string.ascii_lowercase )
        for l in letter_list:
            for l2 in letter_list:
                for l3 in letter_list: 
                    bucketname = 'xa%s%s%s' % (l,l2,l3)
                    print(bucketname)
                    if bucketname == lastitem() :
                        return 
                    bucketfilename = "%s/%s"  % ( "cache", bucketname )
                    if (not os.path.isfile(bucketfilename)) :
                        print("missing data %s" % bucketfilename)
                        return 

                    self.dbBuckets.put(bytes(bucketname, "ascii"),bucketfilename) # bucket name -> filename 
                    print ("bucket %s -> %s" % (bucketname,bucketfilename))
                    print ("bucketname %s bucketfilename %s" % (bucketname, bucketfilename))
                    self.rununzip(bucketfilename,bucketname)                 

def main():    
    i=Indexer()    
    i.openDB()
    i.process ()
    i.dbBuckets.close()
 
main()
