#encoding=utf-8
#����
import os
import sys
import time
import urllib
import urllib2
import httplib
import linecache
import function as f
import config as config
from ftplib import FTP

os.chdir('../')


# addrIP="138.128.217.186"
# addrFolder="NBFuck/bjeea"



'''
Test
'''
#f.package('.Update','.Package\\upd.zip')
#makeUpdDir()
#dropUpdDir()
#cpVersion()
#rmVersion()
#makeUpdPackage()
#uploadUpdPackage()
#pause()
'''
/Test
'''
print('��������Ŀ¼����'),
f.makeUpdDir()
print('DONE')
print('�����汾�ļ�����'),
f.cpVersion()
print('DONE')
print('�������°�����'),
f.makeUpdPackage()
print('DONE')
print('�ϴ����°�����'),
f.uploadUpdPackage()
print('DONE')
print('�������ݿ⡭��'),
f.uploadUpdDatabase()
print('DONE')
print('���°����ϴ���ϣ�Ŀǰֻ�в���ģʽ�ſɸ��¡������Ҫ������ʽ�棬��ִ��_applyUpdate.py��')
f.pause()