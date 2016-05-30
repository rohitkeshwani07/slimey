import os
import errno
import time
import glob
import csv

def makedir_ifnotexist(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
		exit

def move_to_download_folder(downloadPath, newFileName, fileExtension,DOWNLOAD_PATH):
	newFileName = newFileName.strip()
	got_file = False
	#because part file creation is delayed
	partFound = False
	## Wait for it to create .part.
	while not got_file:
		currentFile = glob.glob(DOWNLOAD_PATH+"*"+".part")
		if len(currentFile) == 0 and partFound:
			print "File is downloaded "
			got_file = True
		elif len(currentFile) != 0 and not partFound:
			print "Part file is created"
			partFound = True
		elif partFound:
			print "File has not finished downloading"
			time.sleep(10)
		else:
			print "none case"
	## Create new file name
	currentFile = glob.glob(DOWNLOAD_PATH+"*"+fileExtension)
	fileDestination = "".join((downloadPath,newFileName,fileExtension))
	os.rename(currentFile[0], fileDestination)
	return
def page_opened_or_not(containsString, driver):
	innerHtml = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
	if containsString not in innerHtml:
		return False
	else:
		return True
def writeStatus(fileName,row):
	f_write = open(fileName,'ab+')
	csv_w = csv.writer(f_write)
	csv_w.writerow(row)		
	f_write.close()
def selectElement(browser, selector):
	c=0
	while True:
		try:
			return browser.find_element_by_css_selector(selector)
		except:
			c = c+1
			if c == 5:
				raise
			time.sleep(10)
			continue