from bs4 import BeautifulSoup
import urllib2
import re
import fileinput
import datetime
import plotly as py
import plotly.graph_objs as go
import os
import sqlite3



cwd = os.path.dirname(os.path.realpath(__file__)) + '\\'


def DBConfig(DBName, TableName):
	try:
		con = sqlite3.connect(cwd + DBName)
		con.execute('CREATE TABLE ' + TableName + \
			        ''' (ID 	INT PRIMARY KEY NOT NULL,
			        USD_Harat       INT NOT NULL,
			        USD_Dubai	INT NOT NULL,
			        EURO		INT NOT NULL,
			        LIR		INT NOT NULL
			        );'''
			      )
		con.close()
	except Exception as e:
		print str(e)

def InsertTODB(DBName, TableName, ColumnsList, ValuesList):
	try:
		con = sqlite3.connect(cwd, DBName)
		print 'INSERT INTO ' + TableName + ' (' + (', ').join(ColumnsList)+ ') VALUES (' + (', ').join(ValuesList)+ ')'
		con.execute('INSERT INTO ' + TableName + ' (' + (', ').join(ColumnsList)+ ') VALUES (' + (', ').join(ValuesList)+ ')')
		con.commit()
		con.close()
	except Exception as e:
		print 'error in inserting to table'.title() + str(e)


DBConfig('CurrencyDB.db', 'Currencies')
InsertTODB('CurrencyDB', 'Currencies', ['USD_Harat'], [100])


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def CurrencyPriceListCreator(inputHtml, delimiter1, delimiter2):
	try:
		DateTimeList = []
		PriceList = []
		TempList = []
		cwd = os.path.dirname(os.path.realpath(__file__)) + '\\'

		with open(inputHtml, 'r') as HtmlFile:
			html_doc = HtmlFile.read()
		# Parse the html file
		soup = BeautifulSoup(html_doc, 'html.parser')
		with open(cwd + 'Output.html', 'w') as o:
			for t in  soup.findAll("div", {"class": "text"}):
				TempList.append(str(t))
			for item in TempList:
				if '\xD9\x82\xDB\x8C\xD9\x85\xD8\xAA\x20\xD9\x84\xD8\xAD\xD8\xB8\xD9\x87\x20\xD8\xA7\xDB\x8C\x20\xD8\xAF\xD9\x84\xD8\xA7\xD8\xB1' in item and delimiter1 in item and delimiter2 in item :
					o.write(str(item)[19:int(find_nth(item, '<br/><br/>', 2)) - 12] + '\n')
		
		with open(cwd + 'Output.html', 'r') as f:
			for i in f.readlines():
				# print i.rfind('>')
				try:
					# remove tags : re.sub(r'<.+?>', '', i)
					# if (i[36:46]).isdigit():
					print datetime.datetime.strptime(i[36:46] + '-' + i[51:59], "%Y-%m-%d-%H:%M:%S")
					DateTimeList.append((datetime.datetime.strptime(i[36:46] + '-' + i[51:59], "%Y-%m-%d-%H:%M:%S")))
					print len(DateTimeList)
					print i[int(i.rfind('>')) + 2:]
					PriceList.append(i[int(i.rfind('>')) + 2:])
					print len(PriceList)
				except ValueError:
					continue
				except Exception as e:
					print str(e)
		return (DateTimeList, PriceList)

	except Exception as e:
		print str(e)


x = []
y = []

HaratDollar = '\xD9\x87\xD8\xB1\xD8\xA7\xD8\xAA'
NaghdiDollar = '\xD9\x86\xD9\x82\xD8\xAF\xDB\x8C'
SoleimaniehDollar= '\xD8\xB3\xD9\x84\xDB\x8C\xD9\x85\xD8\xA7\xD9\x86\xDB\x8C\xD9\x87'
KaghaziDollar = '\xDA\xA9\xD8\xA7\xD8\xBA\xD8\xB0\xDB\x8C'


for FileName in range(10, 11) :
	print FileName
	a, b = CurrencyPriceListCreator(cwd + 'messages' + str(FileName) + '.html', NaghdiDollar, HaratDollar)
	for i in a:
		x.append(i)
	for j in b:
		y.append(j)
	print 'len x : ' +  str(len(x))
	print 'len y : ' +  str(len(y))
	print '*****************************************'




fig = go.Figure([go.Scatter(x = x, y = y)])
py.offline.plot(fig)