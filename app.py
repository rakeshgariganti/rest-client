__author__='rakesh'

import sys
import requests
from ui import *
from PySide.QtGui import *
from PySide.QtCore import *
import config
from threading import Thread
try:
	from bs4 import BeautifulSoup as bs
except ImportError:
	pass

class Window(QMainWindow,Ui_MainWindow):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.initiate)
		self.pathedit.setText('http://localhost:8000/')
		self.proxies = {} #{'http': 'http://98.143.144.58:80'}

		# configuration
		if config.proxy != "":
			if config.proxy.startswith('http'):
				self.proxies['http'] = config.proxy
			elif config.proxy.startswith('https'):
				self.proxies['https'] = config.proxy
			elif config.proxy.startswith('socks'):
				self.proxies['socks'] = config.proxy

	def sendrequest(self):
		host = self.pathedit.text()
		method = self.methodcombobox.currentIndex()

		headers = {}
		if self.reqheaders.toPlainText() != "":
			try:
				for i in self.reqheaders.toPlainText().split('\n'):
					headers[i.split(':')[0]] = i.split(':')[1]
			except:
				pass

		query = ""
		if self.getparams.toPlainText() != "":
			query = "?"
			q = str(self.getparams.toPlainText())
			q.replace('\n', '&')
			query += q

		postdata = ""
		if self.posttext.toPlainText() != "":
			q = self.posttext.toPlainText()
			q.replace('\n', '&')
			postdata += q


		postfile = self.postfile.text()

		print "host:"+host
		print "query:"+query
		print "POST DATA:"+postdata
		print "method:"+str(method)
		print "headers:"+str(headers)
		print "POST FILE:"+postfile

		self.cleanui()
		self.setStatusTip('Sending request..')

		if method == 0:
			# send a get request to host
			try:
				req = requests.get(host+query, headers=headers, proxies=self.proxies)
				for i in req.headers:
					self.responseheaderstb.append(i+":"+req.headers[i])
				for i in req.cookies:
					self.cookiestb.append(i+":"+req.headers[i])
				self.responsetb.setPlainText(self.prettify(req.text))
			except:
				print 'Something went wrong'

		elif method == 1:
			# send a post request to host
			files = {}
			if postfile != "":
				try:
					fcontents = open(postfile.split(',')[1], 'rb')
				except:
					fcontents = ""
				files[postfile.split(',')[0]] = fcontents
			try:
				req = requests.post(host+query, data=postdata, headers=headers, proxies=self.proxies)
				for i in req.headers:
					self.responseheaderstb.append(i+":"+req.headers[i])
				for i in req.cookies:
					self.cookiestb.append(i+":"+req.headers[i])
				self.responsetb.setPlainText(self.prettify(req.text))
			except :
				print 'Something went wrong'

		elif method == 2:
			# send a put request to host
			files = {}
			if postfile != "":
				try:
					filecontents = open(postfile.split(',')[1],'rb')
				except:
					filecontents = ""
				files[postfile.split(',')[0]] = filecontents
			try:
				req = requests.put(host, data=postdata, files=files, headers=headers, proxies=self.proxies)
				for i in req.headers:
					self.responseheaderstb.append(i+":"+req.headers[i])
				for i in req.cookies:
					self.cookiestb.append(i+":"+req.headers[i])
				self.responsetb.setPlainText(self.prettify(req.text))
			except :
				print 'Something went wrong'

		elif method == 3:
			# send a delete request to host
			try:
				req = requests.delete(host, data=postdata, headers=headers, proxies=self.proxies)
				for i in req.headers:
					self.responseheaderstb.append(i+":"+req.headers[i])
				for i in req.cookies:
					self.cookiestb.append(i+":"+req.headers[i])
				self.responsetb.setPlainText(self.prettify(req.text))
			except:
				print 'Something went wrong'

		elif method == 4:
			# send a head request to host
			try :
				req = requests.head(host, headers=headers, proxies=self.proxies)
				for i in req.headers:
					self.responseheaderstb.append(i+":"+req.headers[i])
				for i in req.cookies:
					self.cookiestb.append(i+":"+req.headers[i])
			except:
				print 'Something went wrong'
		elif method == 5:
			# send a options request to host
			try:
				req = requests.options(host, headers=headers, proxies=self.proxies)
				for i in req.headers:
					self.responseheaderstb.append(i+":"+req.headers[i])
				for i in req.cookies:
					self.cookiestb.append(i+":"+req.headers[i])
				self.responsetb.setPlainText(req.text)
			except:
				print 'Something went wrong'

		self.tabwidget.setCurrentIndex(2)
		self.setStatusTip('Done')

	def cleanui(self):
		self.cookiestb.clear()
		self.responsetb.clear()
		self.responseheaderstb.clear()

	def initiate(self):
		self.sendrequest()

	def prettify(self, text):
		if bs:
			text = bs(text).prettify()
		return text

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	window.show()
	app.exec_()
