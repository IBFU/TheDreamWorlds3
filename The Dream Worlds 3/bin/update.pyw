#encoding=utf-8
#����
import os,os.path
import sys
import zipfile
import xml.dom.minidom
import urllib
import urllib2
import time
import datetime

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

def Schedule(a,b,c):
    '''''
    a:�Ѿ����ص����ݿ�
    b:���ݿ�Ĵ�С
    c:Զ���ļ��Ĵ�С
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    #sys.stdout.write('%.2f%%\r' %(per))
    outPercent('%.2f%%\r' %(per))

def outState(oc):
	outLog('outState: %s' %(oc))
	if oc!='':
		try:
			f=file('bin/updateState',"w")
			f.write('&false=&upds=%s' %(oc))
			f.close()
		except Exception,e:
			outLog('***Catched bugs:***')
			outLog('***Exception: %s Error: %s***' %(Exception,e))
		# print cmd('echo &false=&upds=%s>bin\\updateState' %(oc))
	else:
		try:
			os.remove('bin/updateState')
		except Exception,e:
			outLog('***Catched bugs:***')
			outLog('***Exception: %s Error: %s***' %(Exception,e))

def outPercent(oc):
	# print('outPercent: %s' %(oc))*3000
	if oc!='':
		try:
			f=file('bin/updatePercent',"w")
			f.write('&false=&p=%s' %(oc))
			f.close()
		except Exception,e:
			outLog('***Catched bugs:***')
			outLog('***Exception: %s Error: %s***' %(Exception,e))
		# print cmd('echo &false=&upds=%s>bin\\updateState' %(oc))
	else:
		try:
			os.remove('bin/updatePercent')
		except Exception,e:
			outLog('***Catched bugs:***')
			outLog('***Exception: %s Error: %s***' %(Exception,e))

def outLog(oc):
	# print 'outLog: %s' %(oc)
	if oc!='':
		now=datetime.datetime.now()
		try:
			f=file('bin/updateLog.log',"a")
			f.write('%s -> %s\n' %(now.strftime('%Y-%m-%d %H:%M:%S'),oc))
			f.close()
		except Exception,e:
			cmd('echo ***Catched bugs:***>>bin\\updateLog.log')
			cmd('echo ***Exception: %s Error: %s***>>bin/updateLog.log' %(Exception,e))
		# print cmd('echo &false=&upds=%s>bin\\updateState' %(oc))
	else:
		try:
			f=file('bin/updateLog.log',"a")
			f.write('\n')
			f.close()
		except Exception,e:
			cmd('echo ***Catched bugs:***>>bin/updateLog.log')
			cmd('echo ***Exception: %s Error: %s***>>bin/updateLog.log' %(Exception,e))

def package(dirname,zipfilename):#´ò°ü£¬²ÎÊý£ºÎÄ¼þ£¨¼Ð£©Ãû£¬°üÃû¡£dirnameÁô¿Õ±íÊ¾½«µ±Ç°Ä¿Â¼ÄÚÈÝÌí¼ÓÈëzip°ü
	outLog('Package File')
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
	outLog('#dirname: %s\\ #zipfilename: %s' %(dirname,zipfilename))
	try:
		zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
		fileNumber=0
		for tar in filelist:
			#arcname = tar[len(dirname):]
			arcname = tar
			outLog('#Package File: %s' %(arcname))
			#print 'tar: %s len(dirname): %s arcname: %s' %(tar,len(dirname),arcname)
			zf.write(tar,arcname)
			fileNumber+=1
		zf.close()
		outLog('#Package File number: %s' %(fileNumber))
		return True
	except Exception,e:
		outLog('***Catched bugs:***')
		outLog('***Exception: %s Error: %s***' %(Exception,e))
		# print '#ERROR: %s - %s' %(Exception,e)
		return False

def unpackage_zip(zipfilename, unziptodir):#½â°ü£¬²ÎÊý£º°üÃû£¬ÎÄ¼þ¼ÐÃû¡£unziptodirÁô¿Õ±íÊ¾½â°üµ½µ±Ç°Ä¿Â¼
	outLog('unPackage File')
	if unziptodir!='' and not os.path.exists(unziptodir):
		os.mkdir(unziptodir)
	else:
		unziptodir='.'
		# unziptodir='update'
	outLog('#zipfilename: %s #unziptodir: %s\\' %(zipfilename,unziptodir))
	try:
		zfobj = zipfile.ZipFile(zipfilename)
		fileNumber=0
		outLog('#FileList: %s' %(zfobj.namelist()))
		for name in zfobj.namelist():
			name = name.replace('\\','/')
			# name = name.replace('/','\\')
			outLog('#Unpackage File: %s' %(name))
			if name.endswith('/'):
				outLog('#Unpackage File Mkdir: %s' %(os.path.join(unziptodir, name)))
				os.mkdir(os.path.join(unziptodir, name))
			else:
				ext_filename = os.path.join(unziptodir, name)
				ext_dir= os.path.dirname(ext_filename)
				outLog('#EXT_Dir: %s' %(ext_dir))
				outLog('#EXT_Filename: %s' %(ext_filename))
				if not os.path.exists(ext_dir):
					# os.mkdir(ext_dir)
					outLog('#Unpackage Path Mkdir: %s' %(ext_dir))
					cmd('md %s\\' %(ext_dir.replace('/','\\')))
				outfile = open(ext_filename, 'wb')
				outfile.write(zfobj.read(name))
				outfile.close()
				fileNumber+=1

				# print '#ERROR: %s - %s' %(Exception,e)
		outLog('Unpackage File number: %s' %(fileNumber))
		return True
	except Exception,e:
		outLog('***Catched bugs:***')
		outLog('***Exception: %s Error: %s***' %(Exception,e))
		# print '#ERROR: %s - %s' %(Exception,e)
		return False

def unpackage(zipfilename, unziptodir):
	outLog('#TEST: FileName: %s toDir: %s' %(zipfilename, unziptodir))
	cmd('%s' %(zipfilename))
	return True

def download(local,nfile):
	#addrServer=("http://%s/%s/" %(addrIP,addrFolder))
	addrServer='%s%s' %(config['coreServer'],config['updateDir'])
	outLog('Download Files addrServer: %s' %(addrServer))
	outLog('Server File: %s%s' %(addrServer,nfile))
	outLog('Local File: %s%s'%(local,nfile))
	try:
		# rtn = urllib.urlretrieve("%s%s" %(addrServer,nfile), "%s%s" %(local,nfile),Schedule)#ÏÂÔØÎÄ¼þ
		rtnData=urllib2.urlopen("%s%s" %(addrServer,nfile)).read()
		rtnFile=file("%s%s" %(local,nfile),'wb')
		rtnFile.write(rtnData)
		rtnFile.close()
		rtn=True;
		outLog('Return: %s'%(rtn))
		if rtn != None:
			return rtn
		else:
			return -1
	except Exception,ex:
		outLog('***Catched bugs:***')
		outLog('***Exception: %s Error: %s***' %(Exception,e))
		# print Exception,ex
		return -2

def getVersion():
	global versionList
	outLog('getVersion')
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
	outLog('Version String: %s' %(versionStr))
	return versionStr

def getPackageList():
	global packageList
	outLog('getPackageList')
	getVersion()
	outLog('getVersionURL: %supd_getpackage.php?istest=%s&mainVersion=%s&buildVersion=%s&dateVersion=%s&versionName=%s' %(addrAddress,isTest,versionList['mainVersion'],versionList['buildVersion'],versionList['dateVersion'],versionList['versionName'].replace(' ','%20')))
	strHtml = urllib2.urlopen('%supd_getpackage.php?istest=%s&mainVersion=%s&buildVersion=%s&dateVersion=%s&versionName=%s' %(addrAddress,isTest,versionList['mainVersion'],versionList['buildVersion'],versionList['dateVersion'],versionList['versionName'].replace(' ','%20'))).read()
	outLog('ServerState: %s' %(strHtml))
	if strHtml=='0' or strHtml=='-1' or strHtml=='-2':
		outLog('noUpdate')
		outState('noUpdate')
	else:
		packageList=strHtml.split('|')
		outLog('updating')
		outLog('updlist: %s' %(packageList))
		outState('updating&updlist=%s' %(packageList))
		#wait(10)
		downloadPackage()
		wait(2)
		applyPackage()

def downloadPackage():
	outLog('downloadPackage')
	for pl in packageList:
		ustr=download('./',pl)
		outLog('Package download: %s %s' %(pl,ustr))

def applyPackage():
	outLog('applyPackage')
	for pl in packageList:
		ustr=unpackage(pl,'')
		outLog('Package apply: %s %s' %(pl,ustr))
		# updS=False
		# if os.path.exists('Version.%s.upd' %(pl)):
		# 	updS=True
		# else:
		# 	updS=False
		# outLog('Unpackage state: %s' %(updS))
		if ustr==True:
			cmd('del %s' %(pl))
			# cmd('del "Version.%s.upd"' %(pl))
			outLog('Package Applyed. drop: %s' %(pl))
		else:
			outLog('Package Apply failed. notdrop: %s' %(pl))
			#dropPackage()
	if ustr:
		outLog('updFinish')
		outState('updFinish')
	else:
		outLog('updFailed')
		outState('updFailed')

def dropPackage():
	outLog('dropPackage')
	for pl in packageList:
		cmd('del %s' %(pl))
		outLog('Package drop: %s' %(pl))

def main():
	#package('','savedata.pyw.zip')
	#unpackage('savedata.pyw.zip','')
	outLog('===Update start===')
	outLog('TestMode: %s' %(isTest))
	getPackageList()
	#wait(5)#test
	#downloadPackage()
	#wait(5)#test
	#applyPackage()
	wait(5)
	outState('')
	# outPercent('')
	outLog('===Update end===')
	outLog('')
main()