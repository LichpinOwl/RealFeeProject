from bs4 import BeautifulSoup
import datetime
import plotly as py
import plotly.graph_objs as go
import os
import sqlite3
import Config


class Mesghal:

    def CreateTable(self, DBName, TableName):
        try:
            con = sqlite3.connect(Config.cwd + DBName)
            con.execute(
                'CREATE TABLE IF NOT EXISTS Table_' + TableName + '(ID INTEGER PRIMARY KEY AUTOINCREMENT, DateTime TEXT, ' + TableName + ' INT)')
            con.close()
        except Exception as e:
            print 'error in create db or table : '.title() + str(e)

    def InsertToTable(self, DBName, TableName, ColumnsList, ValuesList):
        try:
            con = sqlite3.connect(Config.cwd + DBName)
            con.execute(
                'INSERT INTO ' + TableName + ' (' + (', ').join(ColumnsList) + ') VALUES (\'' + ('\', \'').join(
                    ValuesList) + '\')')
            con.commit()
            con.close()
        except Exception as e:
            print 'error in inserting to table : '.title() + str(e)

    def UpdateTable(self, DBName, TableName, ColumnName, ColumnValue, ID):
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

    def find_nth(self, haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start + len(needle))
            n -= 1
        return start

    def CurrencyPriceListCreator(self, inputHtml, delimiter1, delimiter2, OutputFile):
        try:
            DateTimeList = []
            PriceList = []
            TempList = []

            with open(inputHtml, 'r') as HtmlFile:
                html_doc = HtmlFile.read()
            # Parse the html file
            soup = BeautifulSoup(html_doc, 'html.parser')
            with open(OutputFile, 'w') as o:
                for t in soup.findAll("div", {"class": "text"}):
                    if delimiter2 in str(
                            t) and '\xD8\xB3\xD8\xA8\xD8\xB2\xD9\x87\x20\xD9\x85\xDB\x8C\xD8\xAF\xD9\x88\xD9\x86' not in str(
                        t):
                        TempList.append(str(t))
                        with open(Config.cwd + 'templist.html', 'a') as temp:
                            temp.write(str(t))
                for item in TempList:
                    if '\xD9\x82\xDB\x8C\xD9\x85\xD8\xAA\x20\xD9\x84\xD8\xAD\xD8\xB8\xD9\x87\x20\xD8\xA7\xDB\x8C' in item \
                            and delimiter1 in item:
                        # and delimiter2 in item:
                        # and '\xD9\x85\xD8\xAB\xD9\x82\xD8\xA7\xD9\x84' not in item:
                        o.write(str(item)[19:int(self.find_nth(item, '<br/><br/>', 2)) - 12] + '\n')
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
                        try:
                            DateTimeList.append(
                                datetime.datetime.strptime(i[97:107] + '-' + i[112:120], "%Y-%m-%d-%H:%M:%S"))
                            PriceList.append(i[int(i.rfind('>')) + 2:-1])
                        except:
                            pass
                    except TypeError:
                        continue
                    except Exception as e:
                        print 'Error in CurrencyPriceListCreator Module : '.title + str(e)
            return DateTimeList, PriceList

        except Exception as e:
            print str(e)

    def SupplyTable(self, Delimiter1, Delimiter2, FileName):
        OutputFile = Config.cwd + 'OutputHtmls\\' + str(FileName) + '_' + str(Delimiter1[0]) + '_' + str(
            Delimiter2[0]) + '.html'
        self.CreateTable(Config.DBName, str(Delimiter1[0]) + '_' + str(Delimiter2[0]))
        TimeList, ValuesList = self.CurrencyPriceListCreator(
            Config.cwd + 'ExportedData\\messages' + str(FileName) + '.html',
            Delimiter1[1], Delimiter2[1], OutputFile)
        for time, value in zip(TimeList, ValuesList):
            self.InsertToTable(Config.DBName, 'Table_' + str(Delimiter1[0]) + '_' + str(
                Delimiter2[0]), ['DateTime', str(Delimiter1[0]) + '_' + str(Delimiter2[0])], [str(time), value])
        print 'len timeList : ' + str(len(TimeList))
        print 'len valueList : ' + str(len(ValuesList))
        conn = sqlite3.connect(Config.cwd + Config.DBName)
        cursor = conn.execute('select count(*) from Table_' + str(Delimiter1[0]) + '_' + str(
            Delimiter2[0]))
        for row in cursor:
            print str(Delimiter1[0]) + '_' + str(
                Delimiter2[0]) + ' rows count :' + str(row[0]) + '\n'
        conn.close()
        print '-' * 50


if __name__ == "__main__":
    os.system('cls')
    # m = Mesghal()
    # for FileName in range(10, 48):
    #     print '*' * (14 + len(str(FileName)))
    #     print 'File Number : ' + str(FileName)
    #     print '*' * (14 + len(str(FileName)))
    #     m.SupplyTable(Config.Naghdi, Config.Harat, FileName)
        # m.SupplyTable(Config.Naghdi, Config.Soleimanieh, FileName)
        # m.SupplyTable(Config.Dollar, Config.Kaghazi, FileName)

    conn = sqlite3.connect(Config.cwd + Config.DBName)
    cursor = conn.execute("select * from Table_Naghdi_Harat")
    x=[]
    y=[]
    for row in cursor:
        x.append(row[1])
        y.append(row[2])
    conn.close()
    # fig = go.Figure([go.Scatter(x=x, y=y)])
    # py.offline.plot(fig)

    '''
    # if not os.path.isfile(Config.cwd + Config.DBName):
    #     for n in Config.DelimitersList.keys():
    #         CreateTable(Config.DBName, n)
    # else:
    #     pass

    # DATETIME LIST
    TimeList = []
    # CURRENCY VALUES LIST
    ValuesList = []
    for FileName in range(20, 40):
        print '*' * (14 + len(str(FileName)))
        print 'File Number : ' + str(FileName)
        print '*' * (14 + len(str(FileName)))
        for UnicodeKey, UnicodeValue in Config.DelimitersList.iteritems():
            print 'processing : ' + UnicodeKey
            if UnicodeValue != Config.DelimitersList['NaghdiDollar']:
                OutputFile = Config.cwd + 'OutputHtmls\\' + str(FileName) + '-' + UnicodeKey + '.html'
                # print OutputFile
                TimeList, ValuesList = CurrencyPriceListCreator(Config.cwd + 'messages' + str(FileName) + '.html',
                                                                Config.DelimitersList['NaghdiDollar'], UnicodeValue,
                                                                OutputFile)
                print 'len timeList : ' + str(len(TimeList))
                print 'len valueList : ' + str(len(ValuesList))
            for time, value in zip(TimeList, ValuesList):
                InsertToTable(Config.DBName, 'Table' + UnicodeKey, ['DateTime', UnicodeKey], [str(time), value])
            conn = sqlite3.connect(Config.cwd + Config.DBName)
            cursor = conn.execute("select count(*) from Table" + str(UnicodeKey))
            for row in cursor:
                print str(UnicodeKey) + " rows count :" + str(row[0]) + '\n'
            conn.close()
            print '-' * 50
    # fig = go.Figure([go.Scatter(x=x, y=y)])
    # py.offline.plot(fig)
'''
