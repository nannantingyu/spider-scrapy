# -*- coding: utf-8 -*-
import redis, os, contextlib, urllib2

r = redis.Redis(host='127.0.0.1')

def next_file():
    global r
    fileinfo = r.spop('downfile_queue_ex')
    if fileinfo is not None:
        return fileinfo

while True:
    file = next_file()
    if file is None:
        print "crawler close"
        break

    fileinfo = file.split('_____')
    file_url = fileinfo[0]
    file_save_path = fileinfo[1]

    save_dir = os.path.dirname(file_save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        with contextlib.closing(urllib2.urlopen(file_url)) as fimg:
            with open(file_save_path, 'wb') as bfile:
                bfile.write(fimg.read())
    except Exception, e:
        r.sadd('downfile_error', file)
