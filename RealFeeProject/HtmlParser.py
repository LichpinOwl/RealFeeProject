from bs4 import BeautifulSoup
import urllib2
import re
import fileinput
import datetime
import plotly as py
import plotly.graph_objs as go
import os
import sqlite3
import Config




def DBConfig(DBName, TableName):
    try:
        con = sqlite3.connect(Config.cwd + Config.DBName)
        print 'creating database'.title()
        con.execute('CREATE TABLE ' + Config.TableName + \
                    	   ''' (ID 			INTEGER PRIMARY KEY AUTOINCREMENT,
				DateTime 		TEXT,
			        HaratDollar       	INT ,
			        IstanbulDollar		INT ,
			        SoleimaniehDollar	INT ,
			        KaghaziDollar		INT 
			        );'''
                    )
        con.close()
    except Exception as e:
        print 'error in create db or table : '.title() + str(e)

def InsertTODB(DBName, TableName, ColumnsList, ValuesList):
    try:
    	print 'inserting data to database'.title()
        con = sqlite3.connect(Config.cwd + Config.DBName)
        con.execute(
            'INSERT INTO ' + Config.TableName + ' (' + (', ').join(ColumnsList) + ') VALUES (\'' + ('\', \'').join(ValuesList) + '\')')
        con.commit()
        con.close()
    except Exception as e:
        print 'error in inserting to table : '.title() + str(e)

def UpdateTable(DBName, TableName, ColumnName, ColumnValue, ID):
    try:
    	print 'Updating table'.title()
        con = sqlite3.connect(Config.cwd + Config.DBName)
        con.execute(
            'UPDATE ' + Config.TableName + ' SET ' + ColumnName + '= ' + ColumnValue + ' WHERE ID = ' + ID)
        con.commit()
        con.close()
    except Exception as e:
        print 'error in inserting to table : '.title() + str(e)	

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start

def CurrencyPriceListCreator(inputHtml, delimiter1, delimiter2):
    try:
        DateTimeList = []
        PriceList = []
        TempList = []
        Config.cwd = os.path.dirname(os.path.realpath(__file__)) + '\\'

        with open(inputHtml, 'r') as HtmlFile:
            html_doc = HtmlFile.read()
        # Parse the html file
        soup = BeautifulSoup(html_doc, 'html.parser')
        with open(Config.cwd + 'Output.html', 'w') as o:
            for t in soup.findAll("div", {"class": "text"}):
                TempList.append(str(t))
            for item in TempList:
                if '\xD9\x82\xDB\x8C\xD9\x85\xD8\xAA\x20\xD9\x84\xD8\xAD'+\
                '\xD8\xB8\xD9\x87\x20\xD8\xA7\xDB\x8C\x20\xD8\xAF\xD9\x84\xD8\xA7\xD8\xB1' \
                in item and delimiter1 in item and delimiter2 in item:
                    o.write(str(item)[19:int(find_nth(item, '<br/><br/>', 2)) - 12] + '\n')
        with open(Config.cwd + 'Output.html', 'r') as f:
            for i in f.readlines():
                try:
                    # remove tags : re.sub(r'<.+?>', '', i)
                    # print datetime.datetime.strptime(i[36:46] + '-' + i[51:59], "%Y-%m-%d-%H:%M:%S")
                    DateTimeList.append(datetime.datetime.strptime(i[36:46] + '-' + i[51:59], "%Y-%m-%d-%H:%M:%S"))
                    # print len(DateTimeList)
                    # print i[int(i.rfind('>')) + 2:]
                    PriceList.append(i[int(i.rfind('>')) + 2:])
                    # print len(PriceList)
                except ValueError:
                    continue
                except Exception as e:
                    print str(e)
        return DateTimeList, PriceList

    except Exception as e:
        print str(e)







if __name__ == "__main__":
	os.system('cls')

	if not os.path.isfile(Config.cwd + Config.DBName):
		DBConfig(Config.DBName, Config.TableName)
	else:
		pass

	#DATETIME LIST
	x = []

	#CURRENCYVALUESLIST
	y = []
	AllDataDict = {}
	for FileName in range(10, 11):
		print FileName
	        for UnicodeKey, UnicodeValue in Config.DelimitersList.iteritems():
	        	print 'process ' + UnicodeKey + ' : '
	        	if not UnicodeValue == Config.DelimitersList['NaghdiDollar'] :
		    		TimeList, ValuesList = CurrencyPriceListCreator(Config.cwd + 'messages' + str(FileName) + '.html', Config.DelimitersList['NaghdiDollar'], UnicodeValue)
			   	for i in TimeList:
			        	x.append(i)
			    	for j in ValuesList:
			        	y.append(j)
			        AllDataDict[UnicodeKey] = y
				for time, value in zip(x, y):
					for c in range(0, len(y) + 1) :
						UpdateTable(Config.DBName, Config.TableName, UnicodeKey, str(y[c]), str(c))

	# print 'len x : ' + str(len(x))
 #        print 'len y : ' + str(len(y))
 #        print '*****************************************'

	# fig = go.Figure([go.Scatter(x=x, y=y)])
	# py.offline.plot(fig)
	print '*'*100
	conn = sqlite3.connect(Config.cwd + 'CurrencyDB.db')
	cursor = conn.execute("SELECT ID, DateTime, HaratDollar, IstanbulDollar, SoleimaniehDollar, KaghaziDollar from " + Config.TableName)
	for row in cursor:
	   print "ID = ", row[0]
	   print "DateTime = ", row[1]
	   print "USD_Harat = ", row[2]
	   print "USD_Dubai = ", row[3],
	   print 'LIR = ', row[4], 
	   print 'EURO = ', row[5],"\n"

	print "Operation done successfully";
	conn.close()