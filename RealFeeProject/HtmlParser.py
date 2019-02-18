from bs4 import BeautifulSoup
import urllib2
import re
import fileinput
import datetime
import plotly as py
import plotly.graph_objs as go
import os

cwd = os.path.dirname(os.path.realpath(__file__)) + '\\'


def CurrencyPriceListCreator(inputHtml, delimiter):
	try:
		DateTimeList = []
		PriceList = []
		cwd = os.path.dirname(os.path.realpath(__file__)) + '\\'

		with open(inputHtml, 'r') as HtmlFile:
			html_doc = HtmlFile.read()
		# Parse the html file
		soup = BeautifulSoup(html_doc, 'html.parser')
		with open(cwd + 'Output.html', 'w') as o:
			for i in  soup.findAll("div", {"class": "text"}):
				if delimiter in str(i) and '\xD8\xB3\xD8\xA8\xD8\xB2\xD9\x87\x20\xD9\x85\xDB\x8C\xD8\xAF\xD9\x88\xD9\x86'\
				not in str(i) and '\xD8\xB3\xDA\xA9\xD9\x87' not in str(i): #and '\xD9\x82\xDB\x8C\xD9\x85\xD8\xAA\x20\xD9\x84\xD8\xAD\xD8\xB8\xD9\x87\x20\xD8\xA7\xDB\x8C\x20\x3C' in str(i):
					o.write(str(i) + '\n')

		with open(cwd + 'Output.html', 'r') as f:
			for i in f.readlines():
				if "<div" not in i :
					if "</div" not in i:
						try:
						# remove tags : re.sub(r'<.+?>', '', i)
							DateTimeList.append((datetime.datetime.strptime(i[36:46] + '-' + i[51:59], "%Y-%m-%d-%H:%M:%S")))
							PriceList.append(i[214:219])
						except:
							DateTimeList.append((datetime.datetime.strptime(i[97:107] + '-' + i[112:120], "%Y-%m-%d-%H:%M:%S")))
							PriceList.append(i[274:280])
		return (DateTimeList, PriceList)



	except Exception as e:
		print str(e)





USDKaghazi = '\xDA\xA9\xD8\xA7\xD8\xBA\xD8\xB0\xDB\x8C'
x = []
y = []




for FileName in range(29,47) :
	print FileName
	a, b = CurrencyPriceListCreator(cwd + 'messages' + str(FileName) + '.html',USDKaghazi)
	for i in a:
		x.append(i)
	for j in b:
		y.append(j)
	print 'len x : ' +  str(len(x))
	print 'len y : ' +  str(len(y))




# for i in x :
# 	 print i

# for i in y :
# 	 print i

fig = go.Figure([go.Scatter(x = x, y = y)])
py.offline.plot(fig)