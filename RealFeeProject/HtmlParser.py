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
import ntpath


def CreateTable(DBName, TableName):
    try:
        con = sqlite3.connect(Config.cwd + DBName)
        print 'creating Table: Table'.title() + str(TableName) + '\n'
        con.execute('CREATE TABLE Table' + TableName + '(ID INTEGER PRIMARY KEY AUTOINCREMENT, DateTime TEXT, ' + TableName + ' INT)')
        con.close()
    except Exception as e:
        print 'error in create db or table : '.title() + str(e)


def InsertToTable(DBName, TableName, ColumnsList, ValuesList):
    try:
        con = sqlite3.connect(Config.cwd + DBName)
        con.execute(
            'INSERT INTO ' + TableName + ' (' + (', ').join(ColumnsList) + ') VALUES (\'' + ('\', \'').join(
                ValuesList) + '\')')
        con.commit()
        con.close()
    except Exception as e:
        print 'error in inserting to table : '.title() + str(e)


def UpdateTable(DBName, TableName, ColumnName, ColumnValue, ID):
    try:
        print 'Updating table'.title()
        con = sqlite3.connect(Config.cwd + DBName)
        print 'UPDATE ' + TableName + ' SET ' + ColumnName + '= ' + ColumnValue + ' WHERE ID = ' + ID
        con.execute(
            'UPDATE ' + TableName + ' SET ' + ColumnName + '= ' + ColumnValue + ' WHERE ID = ' + ID)
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


def CurrencyPriceListCreator(inputHtml, delimiter1, delimiter2, OutputFile):
    try:
        DateTimeList = []
        PriceList = []
        TempList = []
        Config.cwd = os.path.dirname(os.path.realpath(__file__)) + '\\'

        with open(inputHtml, 'r') as HtmlFile:
            html_doc = HtmlFile.read()
        # Parse the html file
        soup = BeautifulSoup(html_doc, 'html.parser')
        with open(OutputFile, 'w') as o:
            for t in soup.findAll("div", {"class": "text"}):
                TempList.append(str(t))
            for item in TempList:
                if '\xD9\x82\xDB\x8C\xD9\x85\xD8\xAA\x20\xD9\x84\xD8\xAD' + \
                        '\xD8\xB8\xD9\x87\x20\xD8\xA7\xDB\x8C\x20\xD8\xAF\xD9\x84\xD8\xA7\xD8\xB1' \
                        in item and delimiter1 in item and delimiter2 in item:
                    o.write(str(item)[19:int(find_nth(item, '<br/><br/>', 2)) - 12] + '\n')
        with open(OutputFile, 'r') as f:
            for i in f.readlines():
                try:
                    # remove tags : re.sub(r'<.+?>', '', i)
                    # print datetime.datetime.strptime(i[36:46] + '-' + i[51:59], "%Y-%m-%d-%H:%M:%S")
                    DateTimeList.append(datetime.datetime.strptime(i[36:46] + '-' + i[51:59], "%Y-%m-%d-%H:%M:%S"))
                    # print len(DateTimeList)
                    # print i[int(i.rfind('>')) + 2:]
                    PriceList.append(i[int(i.rfind('>')) + 2:-1])
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
        for n in Config.DelimitersList.keys():
            CreateTable(Config.DBName, n)
    else:
        pass

    # DATETIME LIST
    TimeList = []
    # CURRENCY VALUES LIST
    ValuesList = []
    AllDataDict = {}
    for FileName in range(10, 40):
        print '*' * (14 + len(str(FileName)))
        print 'File Number : ' + str(FileName)
        print '*' * (14 + len(str(FileName)))
        for UnicodeKey, UnicodeValue in Config.DelimitersList.iteritems():
            print 'processing : ' + UnicodeKey
            if UnicodeValue != Config.DelimitersList['NaghdiDollar']:
                OutputFile = Config.cwd + 'OutputHtmls\\' + str(FileName) + '-' + UnicodeKey + '.html'
                print OutputFile
                TimeList, ValuesList = CurrencyPriceListCreator(Config.cwd + 'messages' + str(FileName) + '.html',
                                                                Config.DelimitersList['NaghdiDollar'], UnicodeValue, OutputFile)
                print 'len timeList : ' + str(len(TimeList))
                print 'len valueList : ' + str(len(ValuesList))
            for time, value in zip(TimeList, ValuesList):
                InsertToTable(Config.DBName, 'Table' + UnicodeKey, ['DateTime', UnicodeKey], [str(time), value])
    # fig = go.Figure([go.Scatter(x=x, y=y)])
    # py.offline.plot(fig)
            conn = sqlite3.connect(Config.cwd + Config.DBName)
            # print "SELECT ID, DateTime, " + UnicodeKey +  " from " + 'Table' + UnicodeKey
            cursor = conn.execute("select count(*) from Table" + str(UnicodeKey))
            for row in cursor:
                print str(UnicodeKey) + " rows count :" + str(row[0])    + '\n'
            # for row in cursor:
            #     print "ID = ", row[0]
            #     print "DateTime = ", row[1]
            #     print UnicodeKey + ' = ', row[2]
            # print "Operation done successfully"
            conn.close()
        print '-'*50