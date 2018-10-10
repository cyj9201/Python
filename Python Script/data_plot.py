# -*- coding: utf-8 -*-

## 금융 분석과 개발
## 5.1 2차원 플롯
## 5.1.1 1차원 자료
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
%matplotlib auto

np.random.seed(1000)
y = np.random.standard_normal(20)

# ndarray 객체로 넘기는 경우 plot 함수가 이를 자동으로 처리(x값)
x = range(len(y))

plt.plot(x, y)
plt.plot(y)

plt.plot(y.cumsum())
plt.grid(True) # 그리드 추가
plt.axis('tight') # 축 간격을 더 조밀하게 조정

# plot style 추가
plt.plot(y.cumsum())
plt.grid(True)
plt.xlim(-1, 20)
plt.ylim(np.min(y.cumsum()) -1,
         np.max(y.cumsum()) +1)

# plot style 추가2
plt.figure(figsize=(7, 4))
plt.plot(y.cumsum(), 'b', lw = 1.5)
plt.plot(y.cumsum(), 'ro')
plt.grid(True)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A Simple Plot')


## 5.1.2 2차원자료    
np.random.seed(2000)          
y = np.random.standard_normal((20, 2)).cumsum(axis = 0)

plt.figure(figsize = (7, 4))
plt.plot(y, lw=1.5)
plt.plot(y, 'ro')
plt.grid(True)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A simple Plot')

# 가독성을 높이기 위한 주석기호 추가1
plt.figure(figsize = (7, 4))
plt.plot(y, lw=1.5)   # 2 개의 선을 그린다.
plt.plot(y, 'ro')     # 두 개의 점으로 된 선을 그린다.
plt.grid(True)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A simple Plot')

# 가독성을 높이기 위한 주석기호 추가2
plt.figure(figsize=(7, 4))
plt.plot(y[:, 0], lw=1.5, label='1st')
plt.plot(y[:, 1], lw=1.5, label='2nd')
plt.plot(y, 'ro')
plt.grid(True)
plt.legend(loc=0)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A simple Plot')

# 만약 데이터의 크기가 다르면?
# 시각적으로 자료의 정보가 손실
y[:, 1] = y[:, 1] * 100
plt.figure(figsize = (7, 4))
plt.plot(y[:, 0], lw=1.5, label='1st')
plt.plot(y[:, 1], lw=1.5, label='2nd')
plt.plot(y, 'ro')
plt.grid(True)
plt.legend(loc=0)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A simple Plot')

# 두 subplot을 같이 plotting(y축을 하나 더 추가)
fig, ax1 = plt.subplots()
plt.plot(y[:, 0], 'b', lw=1.5, label='1st')
plt.plot(y[:, 0], 'ro')
plt.grid(True)
plt.legend(loc = 8)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value 1st')
plt.title('A simple Plot')
ax2 = ax1.twinx()
plt.plot(y[:, 1], 'g', lw=1.5, label='2nd')
plt.plot(y[: ,1], 'ro')
plt.legend(loc = 0)
plt.ylabel('value 2nd')

# 두 subplot을 구분해서 plotting(y축을 하나 더 추가)
plt.figure(figsize = (7, 5))
plt.subplot(211)
plt.plot(y[:, 0], 'b', lw=1.5, label='1st')
plt.plot(y[:, 0], 'ro')
plt.grid(True)
plt.legend(loc = 0)
plt.axis('tight')
plt.ylabel('value')
plt.title('A simple Plot')
plt.subplot(212)
plt.plot(y[:, 1], 'g', lw=1.5, label='1st')
plt.plot(y[:, 1], 'ro')
plt.grid(True)
plt.legend(loc = 0)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')

# 서로 다른 plot 형식 제공(line/point plot & bar chart)
plt.figure(figsize = (9, 4))
plt.subplot(121)
plt.plot(y[:, 0], lw=1.5, label='1st')
plt.plot(y[:, 0], 'ro')
plt.grid(True)
plt.legend(loc = 0)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('1st Data Set')
plt.subplot(122)
plt.bar(np.arange(len(y)) ,y[:, 1], width=0.5, color='g', label='2nd')
plt.grid(True)
plt.legend(loc = 0)
plt.axis('tight')
plt.xlabel('index')
plt.title('2nd Data Set')


## 5.1.3 기타 플롯 유형
# plot을 이용한 scatter plot 생성
y = np.random.standard_normal((1000, 2))
plt.figure(figsize=(7, 5))
plt.plot(y[:, 0], y[:, 1], 'ro')
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

# 별도의 scatter 함수
plt.figure(figsize = (7, 5))
plt.scatter(y[:,0], y[:, 1], marker='o')
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

# scatter 함수(세 번째 차원을 추가)
c = np.random.randint(0, 10, len(y))
plt.figure(figsize = (7, 5))
plt.scatter(y[:, 0], y[:, 1], c=c, marker='o')
plt.grid(True)
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

# histgram (주로 금융자산 수익률을 나타내는 데 사용)
plt.figure(figsize = (7,4))
plt.hist(y, label=['1st','2nd'], bins=25)
plt.grid(True)
plt.legend(loc=0)
plt.xlabel('value')
plt.ylabel('frequency')
plt.title('Histogram')

# histgram2 (두 자료)
plt.figure(figsize=(7, 4))
plt.hist(y, label=['1st','2nd'], color=['b', 'g'], stacked=True, bins=25)
plt.grid(True)
plt.legend(loc = 0)
plt.xlabel('value')
plt.ylabel('value')
plt.title('Histogram')

# boxplot
fig, ax = plt.subplots(figsize=(7, 4))
plt.boxplot(y)
plt.grid(True)
plt.setp(ax, xticklabels=['1st', '2nd'])
plt.xlabel('data set')
plt.ylabel('value')
plt.title('Boxplot')

# 함수의 상한 하한 사이의 면적 = 해당 함수의 정적분 값
# 1. 함수 정의
from matplotlib.patches import Polygon
def func(x):
    return 0.5 * np.exp(x) + 1

# 2. 적분 구간 정의, 그 구간의 함수의 값
a, b = 0.5, 1.5 # 적분구간
x = np.linspace(0, 2)
y = func(x)

# 3. 함수 plotting
fig, ax = plt.subplots(figsize=(7, 5))
plt.plot(x, y, 'b', linewidth = 2)
plt.ylim(ymin=0)

# 4. Ploygon 함수를 이용하여 적분 구간의 면적 그리기
Ix = np.linspace(a, b)
Iy = func(Ix)
verts = [(a, 0)] + list(zip(Ix, Iy)) + [(b, 0)]
poly = Polygon(verts, facecolor='0.7', edgecolor='0.5')
ax.add_patch(poly)

# 5. plt.text, plt.figtext 함수를 이용하여 수학식과 축 라벨 추가
plt.text(0.5*(a + b), 1, r"$\int_a^b f(x)\mathrm{d}x$", horizontalalignment='center', fontsize=20)
plt.figtext(0.9, 0.075, '$x$')
plt.figtext(0.075, 0.9, "$f(x)$")

# 6. x축과 y축의 틱 값을 표시((a, f(a)) & (b, f(b)) 
ax.set_xticks((a, b))
ax.set_xticklabels(('$a$','$b$'))
ax.set_yticks([func(a), func(b)])
ax.set_yticklabels(('$f(a)$', '$f(b)$'))
plt.grid(True)


# 5.2 금융 관련 plot
# DB data import
import cx_Oracle
import os
os.environ['LD_LIBRARY_PATH']=':/ORACLE/db/12c/lib'

con_fims2005 = cx_Oracle.connect('fimsr/vudrk_read@192.168.1.130:1521/FIMS2005')
cur_fims2005 = con_fims2005.cursor()
sql_query = "SELECT   A.STK_CD AS STK_CD \
           , A.STK_NM_KOR AS STK_NM \
           , B.TRD_DT AS TRD_DT \
           , B.OPEN_PRC AS OPEN_PRC \
           , B.HIGH_PRC AS HIGH_PRC \
           , B.LOW_PRC  AS LOW_PRC \
           , B.CLOSE_PRC AS CLOSE_PRC \
           , B.TRD_QTY AS TRD_QTY \
           , B.LIST_STK_CNT AS LIST_STK_CNT \
           , B.MKT_VAL AS MKT_VAL \
           , B.IP_DATE AS IP_DATE \
               FROM TSTW100 A \
                   , TSTW102 B \
               WHERE TRD_DT BETWEEN '20130101' AND '20181004'\
               AND A.STK_CD = '068270'\
               AND A.STK_CD = B.STK_CD"
seltrion = pd.read_sql(sql_query, con_fims2005, index_col=None)
cur_fims2005.close()
con_fims2005.close()

# 시계열 데이터 plot
# candlestick(plotly 패키지 사용)
import plotly.graph_objs as go
import plotly.offline as offline
import datetime
trace  = go.Candlestick(x = seltrion.IP_DATE, open = seltrion.OPEN_PRC, high = seltrion.HIGH_PRC,
                        low = seltrion.LOW_PRC, close= seltrion.CLOSE_PRC)
data   = [trace]
layout = go.Layout(title = 'seltrion candlestick chart')
fig    = go.Figure(data = data, layout = layout)
offline.plot(fig, filename='candlestick')

# candlestick(matploblib 패키지 사용)
import mpl_finance as mpf
fig, ax = plt.subplots(figsize = (8, 5))
fig.subplots_adjust(bottom = 0.2)
quotes = [tuple([seltrion.IP_DATE[i].timestamp(), seltrion.OPEN_PRC[i], seltrion.HIGH_PRC[i],
                 seltrion.LOW_PRC[i], seltrion.CLOSE_PRC[i]]) for i in range(len(seltrion))]
mpf.candlestick_ohlc(ax, quotes, width=0.6, colorup='b', colordown='r')

# plot_dat_summary(candlestick과 유사하지만 시가와 종가를 두개의 작은 수평선으로 나타냄)
fig, ax = plt.subplots(figsize = (8, 5))
quotes2 = [tuple([seltrion.IP_DATE[i], seltrion.OPEN_PRC[i], seltrion.HIGH_PRC[i],
                 seltrion.LOW_PRC[i], seltrion.CLOSE_PRC[i]]) for i in range(5)]
mpf.plot_day_summary_ohlc(ax, quotes2, colorup='b', colordown='r')
plt.grid(True)
ax.xaxis_date()
plt.title('seltrion')
plt.ylabel('index level')
plt.setp(plt.gca().get_xticklabels(), rotation=30)

