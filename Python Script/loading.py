# -*- coding: utf-8 -*-

#### 모듈을 import하는 세가지 방법
dir() # 모듈 import 전 
# 1. 모듈 직접 호출(권장)
import os
dir() # 모듈 import 후
os
os.getcwd()
# 2. 모듈에 포함된 임의의 함수 호출(프로그래밍 시 변수선언 충돌)
from os import listdir
dir()
listdir()
# 3. 모듈 전체 호출
from os import *
dir()
getcwd()

#### JSON 데이터
# 웹 브라우저와 다른 어플리케이션이 HTTP 요청으로 데이터를 보낼 때 사용하는 파일 형식 중 하나
# python dict와 유사, 객체의 key값은 문자열
import pandas as pd 
import numpy as np
obj = {'name': 'wes', 'places_lived': ['United States','Spain','Germany'], 'pet':np.nan,
       'siblings':[{'name':'scott','age':25,'pet':'Zuko'},{'name':'katie','age':33,'pet':'Cisco'}]}
import json
result = json.dumps(obj) # 파이선 객체를 json 형태로 변환
result2 = json.loads(result) # json 형태를 python 객체로 변환, load(파일을 불러올 때)
siblings = pd.DataFrame(result2['siblings'],columns=['name','age','pet'])


#### HTML yahoo_finance(웹 데이터 크롤링) 
import requests
from lxml.html import parse
from io import StringIO

# parsing 
text = requests.get('http://finance.yahoo.com/q/op?s=AAPL+Options').text # Yahoo Finance사이트(AAPL, S&P 500)
parsed = parse(StringIO(text))
doc = parsed.getroot() # doc객체에 모든 HTML 태그가 추출(table태그 포함)
links = doc.findall('.//a') # 외부 연결 URL은 a태그로 지정, HTML 엘리먼트를 표현하는 객체일 뿐
# 하나씩 호출
"""
lnk = links[27] 
lnk1 = links1[27]
lnk.get('href') # URL과 링크 이름을 갖고올려면 각 엘리먼트에 대해 get 매서드(link의 url)를 호출
lnk.text_content() # text 매서드를 사용해서 링크 이름 가져오기
"""
urls = [lnk.get('href') for lnk in doc.findall('.//a')] # html 문서에서 url목록을 가져오기
tables = doc.findall('.//table')
calls = tables[0] # 옵션 만기일에 특정 상품을 정해진 가격대로 샇 수 있는 권리
puts = tables[1] # 옵션 만기일에 특정 상품을 정해진 가격대로 팔 수 있는 권리
rows = calls.findall('.//tr')

# 셀안에 있는 텍스트 추출
def unpack(row, kind='td'):
    elts = row.findall('.//%s' % kind)
    return [val.text_content().strip().split('\n')[0] for val in elts] # strip: 주어진 문자열에서 양쪽 끝 공백,'\n' 기호 삭제, split: 텍스트간 구분자 설정
unpack(rows[0], kind='th') # th셀 안에 헤더
unpack(rows[2], kind='td') # td셀 안에 데이터

# 웹에서 긁어온 데이터 DataFrame으로 변환
from pandas.io.parsers import TextParser
def parse_option_data(table):
    rows = table.findall('.//tr')
    header = unpack(rows[0], kind='th')
    data = [unpack(r) for r in rows[1:]]
    return TextParser(data, names=header).get_chunk() 
call_data = parse_option_data(calls)
put_data = parse_option_data(puts)

a=pd.read_html('C:\\Users\\CYJ\\Desktop\\FUNDPRO.html') # 간단한 method
b=pd.read_html('https://finance.naver.com/item/main.nhn?code=005930',encoding='euc-kr')
call_data=a[0]
put_data=a[1]


#### Naver에서 주식데이터 크롤링
a=pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0) # 코스피, 코스탁 전종목(KRX)
a=a[0][['회사명','종목코드']]
a.종목코드=a.종목코드.map('{:06d}'.format)
a.columns=['name','code']
# 종목별 코드로 일일 주가데이터 불러오기(url)
def get_url(item_name,a):
    a1 = a.query('name=="{}"'.format(item_name))['code'].to_string(index=False) # query(조건 설정)
    url='https://finance.naver.com/item/sise_day.nhn?code={}'.format(a1)
    print('url= {}'.format(url))
    return url
# 종목별 일자데이터 불러오기
item_name=['CJ','삼성카드','카카오','넷마블']
url=[]
for i in item_name:
    url.append(get_url(i,a))
df=[]
for i in range(len(item_name)):
    df.append(pd.DataFrame())
    for j in range(1,30):   # 기간설정
        pg_url = '{}&page={}'.format(url[i],j)
        df[i]=df[i].append(pd.read_html(pg_url, header=0)[0],ignore_index=True)
    df[i]=df[i].dropna() # 영업일 아닌 날짜 제거
    df[i]['수익률']=0  
    df[i]['수익률']=df[i]['종가'].pct_change()
for i in range(len(df)):
    df[i]=df[i].fillna('')
    df[i].columns=['DATE','CLOSE','DIFF','OPEN','HIGH','LOW','VOLUME','RETURN_PCT']
    df[i]['DATE']=pd.to_datetime(df[i]['DATE'])
    df[i]=df[i].sort_values(by='DATE').reset_index(drop=True)
    for j in range(len(df[i])):
        for k in range(len(df[i].columns)):
            if k == 0:
                df[i].iloc[j,k]="to_date('{}','yyyy-mm-dd hh24:mi:ss')".format(df[i].iloc[j,0])
            else:
                df[i].iloc[j,k]=str(df[i].iloc[j,k])
# DB table 생성 및 import                
import cx_Oracle
con= cx_Oracle.connect('11834/11834@192.168.1.139:1521/FIMS2005')
cur= con.cursor()
for i in range(len(item_name)):
#  cur.execute("DROP TABLE {} PURGE".format(a.query('name=="{}"'.format(item_name[i]))['code'].to_string(index=False))
   cur.execute("CREATE TABLE STOCK_{} ({},{},{},{},{},{},{},{})".format(a.query('name=="{}"'.format(item_name[i]))['code'].to_string(index=False), '"{}" DATE'.format(df[i].columns[0])
   , '"{}" NUMBER(8)'.format(df[i].columns[1]), '"{}" NUMBER(8)'.format(df[i].columns[2]), '"{}" NUMBER(8)'.format(df[i].columns[3]), '"{}" NUMBER(8)'.format(df[i].columns[4])
   , '"{}" NUMBER(8)'.format(df[i].columns[5]), '"{}" NUMBER(8)'.format(df[i].columns[6]), '"{}" NUMBER(20,12)'.format(df[i].columns[7])))
   cur.execute("COMMENT ON TABLE STOCK_{} IS '{}'".format(a.query('name=="{}"'.format(item_name[i]))['code'].to_string(index=False),item_name[i]))
   for j in range(len(df[i])):
        cur.execute("INSERT INTO {} VALUES {}".format('STOCK_{}'.format(a.query('name=="{}"'.format(item_name[i]))['code'].to_string(index=False)),tuple(df[i].iloc[j])).replace("\"",""))
con.commit()
con.close()
cur.close()


#### XML 파싱
# 예제(완성도 떨어짐)
from lxml import objectify
path = 'C:\\Users\\CYJ\\Desktop\\Test\\Performance_XML_Data\\Performance_LIBUS.xml' # 파일 경로
root = objectify.parse(open(path)).getroot()

data=[]
skip_fields=['INDICATOR_SEQ','PARENT_SEQ','DESIRED_CHANGE','DECIMAL_PLACES','INDICATOR_UNIT']
for i in root.INDICATOR:
    datas={}
    for j in i.getchildren():   # 각 INDICATOR의 XML데이터 
        if j.tag in skip_fields:
            continue
        else:
            datas[j]= j.pyval
    data.append(datas)

## 샘플데이터
import xml.etree.ElementTree as elemTree
# path = 'C:\\Users\\CYJ\\Desktop\\Test\\Performance_XML_Data\\Performance_LIBUS.xml' # 파일 경로
path = '//192.168.233.101/default_utils/Study/#조용진/Performance_LIBUS.xml'
tree = elemTree.parse(path).getroot()
tree2 = tree.findall('./INDICATOR')
# XML문서 칼럼명
a=[]
for i in range(len(tree2[0].getchildren())):
    a.append(tree2[0].getchildren()[i].tag) # tag: 부모인자
# XML문서 데이터   
data=[]
for i in range(len(tree2)):
    datas=[]
    for j in range(len(tree2[i].getchildren())):
        if tree2[i][j].text == None:
            tree2[i][j].text=''
            datas.append(tree2[i][j].text)
        else:
            datas.append(tree2[i][j].text)
    data.append(datas)
df=pd.DataFrame(data,columns=a)


## 엑셀로 저장 후 불러오기
# XML파일 엑셀 시트에 끌어오기(수동으로)
df2=pd.read_excel('C:/Users/CYJ/Desktop/Test/Performance_XML_Data/Performance_LIBUS.xlsx')
df2=df2.fillna('')
df==df2
