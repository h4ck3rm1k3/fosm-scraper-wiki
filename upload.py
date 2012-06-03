import boto
from boto.s3.key import Key

conn = boto.connect_s3(host='s3.us.archive.org', is_secure=False)
name="fosm-20120401130001-node-index"
bucket = conn.get_bucket(name)
k = Key(bucket)
file = "/mnt/target/node_index/node_index1.zip"
k.key = file
hdrs = {}
hdrs['x-archive-queue-derive'] = '0'
# add('x-archive-auto-make-bucket', 1)
#add('x-archive-ignore-preexisting-bucket', 1)
hdrs['x-archive-meta-mediatype']= "texts"
hdrs['x-archive-meta-collection']="opensource"
hdrs['x-archive-meta-title']="fosm node index starting with 1"
hdrs['x-archive-meta-description']="fosm index object"
hdrs['x-archive-meta-creator']="james michael dupont<jamesmikedupont@gmail.com>"
hdrs['x-archive-meta-subject']="fosm,osm"
hdrs['x-archive-meta-licenseurl']='http://creativecommons.org/licenses/by-nc/3.0/'

print hdrs

k.set_contents_from_filename(file,headers=hdrs)
