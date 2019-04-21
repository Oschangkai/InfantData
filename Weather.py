# -*- coding: utf-8 -*-
import env
# import copy
import requests
from bs4 import BeautifulSoup

# 註冊會員並取得 KEY: https://opendata.cwb.gov.tw/devManual/insrtuction
# 資料集: https://opendata.cwb.gov.tw/dataset/climate
# file_url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/" + dataid + "?Authorization="+ env.CWBKEY + "&format=json"
# API Doc: https://opendata.cwb.gov.tw/dist/opendata-swagger.html
# Location: https://e-service.cwb.gov.tw/wdps/obs/state.htm


def api_url(dataid):
	return "https://opendata.cwb.gov.tw/api/v1/rest/datastore/" + dataid + "?Authorization="+ env.CWBKEY + "&format=json"

# Read Local XML
def get_rain_data(year):
	if(year not in range(2010,2019)):
		print("Year must be between 2010-2018")
		return
	if(isinstance(year, str) or isinstance(year, int)):
		return open("./dataset/C-B0026-002/mn_Report_"+str(year)+".xml", encoding='utf8')
	else:
		print("Year must be a str or int")
	

if __name__ == "__main__":
	# parse XML
	soup = BeautifulSoup(get_rain_data(2017).read(), "xml")

	# Verify
	# data_count_by_month = []
	# for t in soup.find_all("time"):
	# 	data_count_by_month.append(len(t.find_all("location")))
	# print(data_count_by_month)

	month = [t.getText() for t in soup.find_all("dataTime")]
	
	locations = [loc.getText() for loc in soup.find_all("locationName")]
	
	avg_temp = []
	humidity = []
	for el in soup.find_all("weatherElement"):
		if(el.elementName.get_text() == "平均溫度"):
			avg_temp.append(el.elementValue.value.get_text())
		elif(el.elementName.get_text() == "平均相對濕度"):
			humidity.append(el.elementValue.value.get_text())