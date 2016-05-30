from selenium import webdriver
import time
import csv
import helpers
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

doc_load_time = 10
statusLog = 'status.csv'
DOWNLOAD_PATH = 'null'
filesSupported = "text/csv, application/csv, application/vnd.ms-excel, application/msword, application/zip, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
routes = []

class Route:
	'Routing Class containing function Name and Arguments'

	method_name = 'null'
	arguments = []

class Parser:
	'Common parser for all Pages'
	
	url = "null"
	arr = []
	currentRule = 0
	maxRules = 0

	def __init__(self, url):
		#url to Parse
		self.url = url

	def configBrowser(self):
		global browser, start_time
		start_time = time.time()
		#browser configuration
		profile = webdriver.FirefoxProfile()
		profile.set_preference('browser.download.folderList', 2) # custom location
		profile.set_preference('browser.download.manager.showWhenStarting', False)
		profile.set_preference("general.useragent.override","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36")
		profile.set_preference('browser.download.dir', DOWNLOAD_PATH)
		profile.set_preference('browser.helperApps.neverAsk.saveToDisk', filesSupported)
		browser = webdriver.Firefox(profile)

	def filter(self,string):
		return string.replace("/","-").replace("&amp;","&").strip(" ").encode('utf-8','ignore')

	def clickElement(self, selector, load_time, key=None):
		global doc_load_time, statusLog, DOWNLOAD_PATH, filesSupported, profile, browser
		if key == None:
			browser.find_element_by_css_selector(selector).click()
			time.sleep(load_time)
		else:
			browser.find_element_by_css_selector(selector)[key].click()
			time.sleep(load_time)

	def getHtmlElement(self, selector, key=None):
		if key == None:
			return browser.find_element_by_xpath(selector).get_attribute('innerHTML').encode('utf-8','ignore')
		else:
			return browser.find_elements_by_xpath(selector)[key].get_attribute('innerHTML').encode('utf-8','ignore')

	def getTable(self, selector, key=None):
		if key == None:
			return "<meta http-equiv='content-type' content='application/vnd.ms-excel; charset=UTF-8'><table>"+self.getHtmlElement(selector)+"</table>"
		else:
			return "<table>"+self.getHtmlElement(selector,key)+"</table>"

	def download(self, filePath, HTML):
		file = open(filePath,'w')
		file.write(HTML)
		file.close()

	#For Link 1
	def getData(self):
		global doc_load_time, statusLog, DOWNLOAD_PATH, filesSupported, profile, browser,row,depth,routes
		print "opening page..."
		browser.get(self.url)
		print "page opened"
		DOWNLOAD_PATH = "data/country/"
		helpers.makedir_ifnotexist(DOWNLOAD_PATH)
		self.maxRules = len(routes)
		try:
			f = open(statusLog)
			reader = csv.reader(f)
			for row in reader:
				continue
			for index in range(3-len(row)):
				row.append('null')
			depth = [0,0,0]
		except:
			depth = [0,0,0]
			row=['null','null','null']
		finally:			
			depth[0] = 0 if row[0] == 'null' or row[0] == '' else 1
			depth[1] = 0 if row[1] == 'null' or row[1] == '' else 1
			depth[2] = 0 if row[2] == 'null' or row[2] == '' else 1
			print depth[0],depth[1],depth[2]
			try:
				print row
				routes[self.currentRule].method_name(*routes[self.currentRule].arguments)
			except:
				raise
				print "exception"
			finally:
				browser.close()
				helpers.writeStatus("time.csv",[time.time() - start_time])

	def rule1(self,xPath,stringFromNextPage,i,maxRule):
		global doc_load_time, statusLog, DOWNLOAD_PATH, filesSupported, profile, browser,row,depth
		i=int(i)
		maxRule = int(maxRule)
		States = browser.find_elements_by_xpath(xPath)
		for keyState,state in enumerate(States):
			States = browser.find_elements_by_xpath(xPath)
			stateName = self.filter(States[keyState].text)
			print stateName
			if not self.arr:
				helpers.makedir_ifnotexist(DOWNLOAD_PATH+stateName)
			else:
				helpers.makedir_ifnotexist(DOWNLOAD_PATH+"/".join(self.arr)+"/"+stateName)
			if stateName == row[i] and depth[i] != 0:
				#case till where we have processed
				depth[i] = 0
			elif depth[i] != 0:
				#case if we have processed
				continue
			bodyBeforeClick = browser.find_element_by_tag_name("body").get_attribute("innerHTML")
			States[keyState].click()
			print "page loaded"
			time.sleep(1)
			#check
			if browser.find_element_by_tag_name("body").get_attribute("innerHTML") == bodyBeforeClick:
				self.arr.extend([stateName,"not a link"])
				helpers.writeStatus(statusLog,self.arr)
				continue
			if not helpers.page_opened_or_not(stringFromNextPage,browser):
				self.arr.extend([stateName,"page faulty"])
				helpers.writeStatus(statusLog,self.arr)
				browser.back()
				continue
			self.arr.extend([stateName])
			print stateName
			print row[i]
			currentRule = self.currentRule
			if self.currentRule+1 < self.maxRules:
				self.currentRule = self.currentRule + 1
				routes[self.currentRule].method_name(*routes[self.currentRule].arguments)
				self.currentRule = currentRule
			if not stateName == row[i]:
				#writestatus
				helpers.writeStatus(statusLog,self.arr)
			self.arr.pop()
			browser.back()
			time.sleep(1)
		self.currentRule = self.currentRule+maxRule+1

	def rule2(self,xPathTable):
		global statusLog, DOWNLOAD_PATH		
		#download
		self.download(DOWNLOAD_PATH+"/".join(self.arr)+"/"+self.arr[len(self.arr)-1]+".xls", self.getTable(xPathTable))
		if self.currentRule+1 < self.maxRules:
			self.currentRule = self.currentRule + 1
			routes[self.currentRule].method_name(*routes[self.currentRule].arguments)
