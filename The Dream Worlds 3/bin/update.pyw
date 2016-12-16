#encoding=utf-8
#����
import os,os.path
import sys
import zipfile
import xml.dom.minidom
import urllib
import urllib2
import time

config={
	'engineServer':		'http://dreamui.ibfu.org/',
	'coreServer':		'http://dr.ibfu.org/index/tdw3/',
	'updateDir':		'update/',
	'binDir':			'bin/',
'':''}
versionList={}
packageList=[]
isTest=0
try:
	isTest=sys.argv[1]
except:
	isTest=0
#test
addrAddress=config['coreServer']+config['updateDir']

def cmd(c):
	return os.popen(c).read()

def pause():
	cmd("pause")

def wait(t):
	time.sleep(t)

def outState(oc):
	print 'outState: %s' %(oc)
	if oc!='':
		f=file('bin/updateState',"w")
		f.write('&false=&upds=%s' %(oc))
		f.close()
		# print cmd('echo &false=&upds=%s>bin\\updateState' %(oc))
	else:
		os.remove('bin/updateState')

def package(dirname,zipfilename):#´ò°ü£¬²ÎÊý£ºÎÄ¼þ£¨¼Ð£©Ãû£¬°üÃû¡£dirnameÁô¿Õ±íÊ¾½«µ±Ç°Ä¿Â¼ÄÚÈÝÌí¼ÓÈëzip°ü
	filelist = []
	if os.path.isfile(dirname):
		filelist.append('.\\%s' %(dirname))
		#print 'Include File: .\\%s' %(dirname)
	else :
		dirname='.'
		for root, dirs, files in os.walk(dirname):
			for name in files:
				filelist.append(os.path.join(root, name))
				#print 'Include File: %s' %(os.path.join(root, name))
	#print filelist
	#print '';
	print '#dirname: %s\\ #zipfilename: %s' %(dirname,zipfilename)
	try:
		zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
		fileNumber=0
		for tar in filelist:
			#arcname = tar[len(dirname):]
			arcname = tar
			print '#Package File: %s' %(arcname)
			#print 'tar: %s len(dirname): %s arcname: %s' %(tar,len(dirname),arcname)
			zf.write(tar,arcname)
			fileNumber+=1
		zf.close()
		print '#Package File number; %s' %(fileNumber)
		return True
	except Exception,e:
		print '#ERROR: %s - %s' %(Exception,e)
		return False

def unpackage(zipfilename, unziptodir):#½â°ü£¬²ÎÊý£º°üÃû£¬ÎÄ¼þ¼ÐÃû¡£unziptodirÁô¿Õ±íÊ¾½â°üµ½µ±Ç°Ä¿Â¼
	if unziptodir!='' and not os.path.exists(unziptodir):
		os.mkdir(unziptodir)
	else:
		unziptodir='.'
	print '#zipfilename: %s #unziptodir: %s\\' %(zipfilename,unziptodir)
	try:
		zfobj = zipfile.ZipFile(zipfilename)
		fileNumber=0
		for name in zfobj.namelist():
			name = name.replace('\\','/')
			print '#Unpackage File: %s' %(name)
			if name.endswith('/'):
				os.mkdir(os.path.join(unziptodir, name))
			else:
				ext_filename = os.path.join(unziptodir, name)
				ext_dir= os.path.dirname(ext_filename)
				if not os.path.exists(ext_dir):
					os.mkdir(ext_dir)
				outfile = open(ext_filename, 'wb')
				outfile.write(zfobj.read(name))
				outfile.close()
				fileNumber+=1
		print 'Unpackage File number: %s' %(fileNumber)
		return True;
	except Exception,e:
		print '#ERROR: %s - %s' %(Exception,e)
		return False

def download(local,nfile):
	#addrServer=("http://%s/%s/" %(addrIP,addrFolder))
	addrServer='%s%s' %(config['coreServer'],config['updateDir'])
	try:
		rtn = urllib.urlretrieve("%s%s" %(addrServer,nfile), "%s%s" %(local,nfile))#ÏÂÔØÎÄ¼þ
		if rtn != None:
			return rtn
		else:
			return -1
	except Exception,ex:
		print Exception,ex
		return -1

def getVersion():
	global versionList
	dom = xml.dom.minidom.parse('config\\version.xml')
	root = dom.documentElement
	for c in root.childNodes:
		try:
			# versionKey.append(c.getAttribute("key"))
			# versionValue.append(c.getAttribute("value"))
			versionList[c.getAttribute("key")]=c.getAttribute("value")
		except:
			pass
	#print root.firstChild.attributes('key')
	versionStr='%s.%s.%s' %(versionList['mainVersion'],versionList['buildVersion'],versionList['dateVersion'])
	return versionStr

def getPackageList():
	global packageList
	getVersion()
	print 'getVersionURL: %supd_getpackage.php?istest=%s&mainVersion=%s&buildVersion=%s&dateVersion=%s&versionName=%s' %(addrAddress,isTest,versionList['mainVersion'],versionList['buildVersion'],versionList['dateVersion'],versionList['versionName'])
	strHtml = urllib2.urlopen('%supd_getpackage.php?istest=%s&mainVersion=%s&buildVersion=%s&dateVersion=%s&versionName=%s' %(addrAddress,isTest,versionList['mainVersion'],versionList['buildVersion'],versionList['dateVersion'],versionList['versionName'])).read()
	print packageList
	if strHtml=='0' or strHtml=='-1' or strHtml=='-2':
		outState('noUpdate')
	else:
		packageList=strHtml.split('|')
		outState('updating&updlist=%s' %(packageList))
		#wait(10)
		downloadPackage()
		wait(2)
		applyPackage()

def downloadPackage():
	for pl in packageList:
		ustr=download('./',pl)
		print 'Package download: %s %s' %(pl,ustr)

def applyPackage():
	for pl in packageList:
		ustr=unpackage(pl,'')
		print 'Package apply: %s %s' %(pl,ustr)
		# if ustr!=False:
		cmd('del %s' %(pl))
		print 'Package drop: %s' %(pl)
			#dropPackage()
	outState('updFinish')

def dropPackage():
	for pl in packageList:
		cmd('del %s' %(pl))
		print 'Package drop: %s' %(pl)

def main():
	#package('','savedata.pyw.zip')
	#unpackage('savedata.pyw.zip','')
	print 'TestMode: %s' %(isTest)
	getPackageList()
	#wait(5)#test
	#downloadPackage()
	#wait(5)#test
	#applyPackage()
	wait(5)
	outState('')
main()