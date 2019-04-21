# -*- coding: utf-8 -*-
import env
import csv
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
  
def data_cleaning(year):
  print("Parsing "+str(year), end='')
  # parse XML
  soup = BeautifulSoup(get_rain_data(year).read(), "xml")

  # Verify
  data_count_by_month = []
  for t in soup.find_all("time"):
    data_count_by_month.append(len(t.find_all("location")))

  month = [t.getText() for t in soup.find_all("dataTime")]
  station = [s.getText() for s in soup.find_all("stationId")]
  expanded_month = []
  for idx, val in enumerate(month):
    expanded_month += [val]*data_count_by_month[idx]
  print(", data count: "+ str(len(expanded_month)))
  
  
  locations = [loc.getText() for loc in soup.find_all("locationName")]
  

  avg_temp = []
  humidity = []
  for el in soup.find_all("weatherElement"):
    if(el.elementName.get_text() == "平均溫度"):
      avg_temp.append(el.elementValue.value.get_text())
    elif(el.elementName.get_text() == "平均相對濕度"):
      humidity.append(el.elementValue.value.get_text())

  return [{'time': mon, 'station': sta, 'average_temperature': avgt, 'humidity': hum} for mon, sta, avgt, hum in zip(expanded_month, station, avg_temp, humidity)]



if __name__ == "__main__":
  data = []
  for i in range(2010,2019):
    data += data_cleaning(i)

  print("\n\nTotal data count: "+str(len(data)))
  print("Writing data to csv...")
  keys = data[0].keys()
  with open("./output/weather.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(data)
  