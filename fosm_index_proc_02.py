 
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


def readnodes (bucket,zipfile,member,position,block, data) :    
    f = StringIO.StringIO(data)
#    f = BytesIO(nodesindex)
    #f = open(mode="r:b", fileobj =myfileobj)
    pos=0
    try:
        byte = f.read(4)
        while byte != "":
#            print byte
            value = struct.unpack('i', byte)
            if (value[0]>0) :
                #print ("%d" % value[0]);
                #bucket_files_nodes (project int, position int, block int, bpos int, node int)
                cmd ="%s,%s,,%s, %s,%s,%s,%s"  % (bucket,zipfile,member,position,block,pos,value[0]);
                #print (position,block,pos,value[0])
                print cmd

                print 
                pos=pos+4
        # Do stuff with byte.
            byte = f.read(4)
    finally:
        print "done";
#        f.close()



def readindex(bucket,zipfile,position,block,f):
        data = f.read()
#        print data
#        myfileobj=StringIO(data)
        myfileobj = StringIO.StringIO(data)
        #output.write(data)
        mytarfile = tarfile.open(mode="r:bz2", fileobj =myfileobj)
        for member in mytarfile.getnames():
            print member
            if member.endswith("node_ids.bin") :
                nodes=mytarfile.extractfile(member).read()
                #print nodes
                readnodes(bucket,zipfile,member,position,block,nodes)
            #print tar.extractfile(member).read()
 
#        darray = data.rsplit("\n")
        #print darray
        #for y in darray :
        #    if y.endswith("_i.tbz"):
                #cmd ="insert or replace into bucket_files values (1,?,?)" 

def rununzip(bucket,position,block,data):
    #unzip the data
    output = StringIO.StringIO()
    output.write(data)
    zf = zipfile.ZipFile(output, mode='r')
    print zf
    il= zf.infolist()
    for zi in il :
        print zi.filename
        d = zf.open(zi)
        #readnodes (1,1, d)
        readindex (bucket,zi.filename,position,block,d)

        #for l in d :
#            print l

def onefile(str) :
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
    br.set_handle_robots(False)
    data = br.open(uri_overview).read()
    rununzip(name,position,block,data)


def process():

    data = []

#    for x in data :
    print list(string.lowercase )
    print string.lowercase
    for l in list(string.lowercase ):
#        print l
        for l2 in list(string.lowercase):
#            print "%s%s" % (l, l2)
            for l3 in list(string.lowercase) : 
                str = 'xa%s%s%s' % (l,l2,l3)
                print str
                onefile(str)
  
 
def main():
    
    print "test"
    
    #print genletters (lastitem())
 
    process ()

 
main()
