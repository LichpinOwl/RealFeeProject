# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup, NavigableString, Tag
import os, re
import Config
from os import listdir
from os.path import isfile, join
import sqlite3


class Mesghal:
    def TagChanger(self, htmlfile):
        FileName = os.path.basename(htmlfile)
        with open(htmlfile, 'r') as f:
            with open(Config.cwd + 'ExportedData2\\' + FileName, 'w') as txt:
                lines = f.readlines()
                for line in lines:
                    if '<a' or 'a>' in line:
                        TempLine = line.replace('<a', '<b')
                        TempLine = TempLine.replace('a>', 'b>')
                    txt.write(TempLine)

    def html_to_text(self, inputHtml):
        "Creates a formatted text email message as a string from a rendered html template (page)"
        with open(inputHtml, 'r') as HtmlFile:
            html = HtmlFile.read()
        soup = BeautifulSoup(html, 'html.parser')
        # soup.encode("utf-8")
        # Ignore anything in head
        body, text = soup.body, []
        for element in body.descendants:
            # We use type and not isinstance since comments, cdata, etc are subclasses that we don't want
            if type(element) == NavigableString:
                parent_tags = (t for t in element.parents if type(t) == Tag)
                hidden = False
                for parent_tag in parent_tags:
                    # Ignore any text inside a non-displayed tag
                    # We also behave is if scripting is enabled (noscript is ignored)
                    # The list of non-displayed tags and attributes from the W3C specs:
                    if (not (not (parent_tag.name in ('area', 'base', 'basefont', 'datalist', 'head', 'link',
                                                      'meta', 'noembed', 'noframes', 'param', 'rp', 'script',
                                                      'source', 'style', 'template', 'track', 'title',
                                                      'noscript')) and not parent_tag.has_attr('hidden') and not (
                            parent_tag.name == 'input' and parent_tag.get('type') == 'hidden'))):
                        hidden = True
                        break
                if hidden:
                    continue

                # remove any multiple and leading/trailing whitespace
                string = ' '.join(element.string.split())
                if string:
                    if element.parent.name == 'a':
                        a_tag = element.parent
                        # replace link text with the link
                        string = a_tag['href']
                        # concatenate with any non-empty immediately previous string
                        if (type(a_tag.previous_sibling) == NavigableString and
                                a_tag.previous_sibling.string.strip()):
                            text[-1] = text[-1] + ' ' + string
                            continue
                    elif element.previous_sibling and element.previous_sibling.name == 'a':
                        text[-1] = text[-1] + ' ' + string
                        continue
                    elif element.parent.name == 'p':
                        # Add extra paragraph formatting newline
                        string = '\n' + string
                    text += [string]
        doc = '\n'.join(text)
        return doc

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
                'INSERT INTO Table_' + TableName + ' (' + (', ').join(ColumnsList) + ') VALUES (\'' + ('\', \'').join(
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

    def CurrencyPriceExtractor(self, Delimiter1, Delimiter2):
        AllHtmlFiles2 = [f for f in listdir(Config.cwd + 'ExportedData2') if
                         isfile(join(Config.cwd + 'ExportedData2', f))]
        for j in AllHtmlFiles2:
            PostSeperatorLineList = []
            print Config.cwd + 'ExportedData2\\' + j
            with open(Config.cwd + 'ExportedData2\\' + j, 'r') as f:
                for num, line in enumerate(f, 1):
                    if 'قیمت لحظه ای مثقال' in line:
                        PostSeperatorLineList.append(num)
                for index in PostSeperatorLineList:
                    pass
            with open(Config.cwd + 'ExportedData2\\' + j, 'r') as f:
                lines = f.readlines()
                for l in range(1, len(PostSeperatorLineList) - 1):
                    SinglePost = lines[PostSeperatorLineList[l]: PostSeperatorLineList[l + 1]]
                    # print SinglePost
                    # print any('گزارش' in s for s in SinglePost)
                    if not any('گزارش' in s for s in SinglePost):
                        if any(Delimiter1 in s for s in SinglePost) and any(
                                Delimiter2 in s for s in SinglePost):
                            self.CreateTable('CurrencyDB.db', 'DollarNaghdi')
                            try:
                                if '#مثقال' not in SinglePost[1][:-1]:
                                    self.InsertToTable('CurrencyDB.db', 'DollarNaghdi', ['DateTime', 'DollarNaghdi'], [SinglePost[1][:-1] + ' ' + SinglePost[2][:-1], SinglePost[[i for i, s in enumerate(SinglePost) if 'نسبت به قیمت قبل' in s][0] - 1][:-12] + '\n'])
                                else:
                                    self.InsertToTable('CurrencyDB.db', 'DollarNaghdi', ['DateTime', 'DollarNaghdi'],
                                                       [SinglePost[2][:-1] + ' ' + SinglePost[3][:-1], SinglePost[
                                                                                                           [i for i, s
                                                                                                            in
                                                                                                            enumerate(
                                                                                                                SinglePost)
                                                                                                            if
                                                                                                            'نسبت به قیمت قبل' in s][
                                                                                                               0] - 1][
                                                                                                       :-12] + '\n'])
                            except IndexError:
                                pass
                            print SinglePost[1][:-1] + ' ' + SinglePost[2][:-1]
                            try:
                                print 'price : ' + SinglePost[[i for i, s in enumerate(SinglePost) if
                                                               'نسبت به قیمت قبل' in s][0] - 1][:-12] + '\n'
                            except IndexError:
                                pass


if __name__ == '__main__':
    # AllHtmlFiles = [f for f in listdir(Config.cwd + 'ExportedData') if isfile(join(Config.cwd + 'ExportedData', f))]
    # for i in AllHtmlFiles:
    #     TagChanger(Config.cwd + 'ExportedData\\' + i)
    AllHtmlFiles2 = [f for f in listdir(Config.cwd + 'ExportedData2') if isfile(join(Config.cwd + 'ExportedData2', f))]
    # for j in AllHtmlFiles2:
    #     with open(Config.cwd + 'ExportedData2\\_' + j, 'w') as f:
    #         print 'write to ' + Config.cwd + 'ExportedData2\\_' + j
    #         f.write(html_to_text(Config.cwd + 'ExportedData2\\' + j).encode("utf-8"))
    m = Mesghal()
    m.CurrencyPriceExtractor('#دلار', '#نقدی')
