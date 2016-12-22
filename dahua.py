#coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
from enum import Enum

import chardet

class WriteOSD:

	CameraType = Enum('CameraType', ('haikang', 'dahua', 'jinsanli'))
	camera_type = "dahua"
	osd_dict = dict()

	def getCameraType(self):
		return camera_type

	def getBrowser(self):
		profile = webdriver.FirefoxProfile("C:/Users/lenovo/AppData/Roaming/Mozilla/Firefox/Profiles/vnfpazs0.test")
		browser = webdriver.Firefox(profile, executable_path="C:/Program Files (x86)/Mozilla Firefox/geckodriver.exe")
		return browser

	#从excel表格中读取url和对应的字符叠加
	def getUrlsAndOSD(self):
		with open('osd.csv', 'r') as csvfile:
			reader = csv.reader(csvfile)
			rows = [row for row in reader]
			for i in range(len(rows)):
				url = rows[i][0]
				osd_title = rows[i][1].decode('gb2312')
				self.osd_dict[url] = osd_title

	def login(self, browser):
		try:
			if self.camera_type is "dahua":
				browser.find_element_by_id("username").clear()
				browser.find_element_by_id("username").send_keys("admin")
				browser.find_element_by_id("password").clear()
				browser.find_element_by_id("password").send_keys("admin")
				browser.find_element_by_id("b_login").click()
		except Exception,e:
			print "login fail: ", e

	def writeOSD_dahua(self, url, osdTitle, browser):
		
		browser.get(url)
		self.login(browser)
		browser.find_element_by_id("b_config").click()
		time.sleep(2)
		try:
			#加载设置
			WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "camera")))
			#加载视频设置
			element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "l_encode")))
			if element.is_displayed() == False:
				browser.find_element_by_id("camera").click()
			browser.find_element_by_id("l_encode").click()
			time.sleep(2)
			WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "video_OSD_tab")))
			browser.find_element_by_id("video_OSD_tab").click()
			time.sleep(2)

			WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "video_OSD_ConfigBtn2")))
			#点击配置
			browser.find_element_by_id('video_OSD_ConfigBtn2').click()
			element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "video_OSDChannel")))
			#输入通道
			element.clear()
			element.send_keys(osdTitle)
			#确定
			browser.find_element_by_id("video_OSD_confirm").click()
		except Exception, e:
			print "%s: write osd title fail: " % url, e


	def write_process(self):
		self.getUrlsAndOSD()
		urls = self.osd_dict.keys()
		osdTitles = self.osd_dict.values()
		if len(urls) != len(osdTitles):
			print "write_process faild:urls与osdTitles不匹配!"
		browser = self.getBrowser()
		for i in range(len(urls)):
			#url = urls[i]
			url = "http://10.46.2.20"
			osdTitle = osdTitles[i]
			print "writing osd title:%s" % url
			self.writeOSD_dahua(url, osdTitle, browser)

writeOSD = WriteOSD()
writeOSD.write_process()
