# -*- coding: utf-8 -*-
import pandas as pd
import xml.etree.ElementTree as elemTree
path = 'C:/Users/CYJ/Desktop/Test/XML_Data/price_feed_supplemental_002385.xml'
tree = elemTree.parse(path)

# XML 문서의 최상단 루트 태그
tree2 = tree.getroot()


## USA_LTSF
# Data 계층구조 파악
# 29종목(주식, 편드)의 시계열 데이터(각 종목별로 기간 다름 ~2018.04.27)
tree2.getchildren()[0].getchildren()[0].getchildren()[0].attrib
tree2.getchildren()[0].getchildren()[0].getchildren()[0].getchildren()[0].text


# Find ID_CODE & the longest Period 
period=[]
for i in range(len(tree2.getchildren())):
    period.append(dict(list(tree2.getchildren()[i].attrib.items()) + list(tree2.getchildren()[i].getchildren()[0].attrib.items())))
p1=[]
for i in range(len(tree2.getchildren()[0].getchildren()[0].getchildren())):
    p1.append(tree2.getchildren()[0].getchildren()[0].getchildren()[i].attrib['Date'])
p4=[]
for i in range(len(tree2.getchildren()[17].getchildren()[0].getchildren())):
    p4.append(tree2.getchildren()[0].getchildren()[0].getchildren()[i].attrib['Date'])


# ID classcification
b=[]
c=[]
for i in range(len(tree2.getchildren())):
    if tree2.getchildren()[i].attrib['Id'].startswith('1') == True:
        b.append(tree2.getchildren()[i].attrib['Id'])
    else:
        c.append(tree2.getchildren()[i].attrib['Id'])


# NAV = 순자산가치(포트폴리오에 있는 주식의 총가격(부채 제외) / 주식수)
# Offer = ask price(매도가)
data=[]
data4=[]
Type=['Mid','Nav']
for i in range(len(b)):
    datas=[]
    for j in range(len(tree2.getchildren()[i].getchildren()[0].getchildren())):
        if any(x in tree2.getchildren()[i].getchildren()[0].getchildren()[j].getchildren()[0].attrib['Type'] for x in Type):
            datas.append(tree2.getchildren()[i].getchildren()[0].getchildren()[j].getchildren()[0].text)
    data.append(datas)

for i in range(len(b),len(b+c)):
    datas4=[]
    for j in range(len(tree2.getchildren()[i].getchildren()[0].getchildren())):
        if any(x in tree2.getchildren()[i].getchildren()[0].getchildren()[j].getchildren()[0].attrib['Type'] for x in Type):
            datas4.append(tree2.getchildren()[i].getchildren()[0].getchildren()[j].getchildren()[0].text)
    data4.append(datas4)    


# Input Price Data into DataFrame
df = pd.DataFrame(data).T
df.index = p1
df.columns = b

df2 = pd.DataFrame(data4).T
df2.index = p4
df2.columns = c


print(*data4)

