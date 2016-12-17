#encoding=utf-8
import sys
import os.path
import win32api
import win32clipboard as w
import win32con
import string

config={
	'engineIP':			'138.128.217.186',
	'engineServer':		'http://dreamui.ibfu.org/',
	'coreServer':		'http://dr.ibfu.org/index/tdw3/',
	'coreFolder':		'dreamui/dreamgames/',
	'updateDir':		'update/',
	'noUpdFolder':		['.backup','.Update','.Develop','.Package'],
'':''}