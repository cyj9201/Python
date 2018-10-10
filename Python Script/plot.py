# -*- coding: utf-8 -*-

#### 8.1 matplotlib API 간략하게 살펴보기
## 8.1.1 Figure와 subplot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.random import random

# plot Figure 생성
fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1) # (행, 렬, 1번째)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
fig
_ = ax1.hist(np.random.random(100),bins=20,color='k',alpha=0.3)
ax2.scatter(np.arange(30),np.arange(30)+3 *np.random.random(30))
ax3.plot(np.random.random(50).cumsum(), 'k--') # cumsum:각 원소의 누적합 표시, k--:스타일옵션(검은 점선)
fig.show() # Figure 창 크게 보기

fig, axes = plt.subplots(2,3)
axes[0,0]

# subplot간 간격 조절
# plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None) # 간격조절
fig, axes = plt.subplots(2,2,sharex=True, sharey=True)
for i in range(2):
    for j in range(2):
        axes[i,j].hist(np.random.random(500), bins=50, color='k', alpha=0.5)
plt.subplots_adjust(wspace=0,hspace=0)

## 8.1.2 색상,마커 선 스타일
data = np.random.random(30).cumsum()
plt.plot(data, 'k--', label='Default')
plt.plot(data, 'k-', drawstyle='steps-post', label='steps-post')
plt.legend(loc='best') # 범례에 표시

## 8.1.3 눈금, 라벨, 범례
fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
ax.plot(random(1000).cumsum())
# x축 눈금 설정
ticks = ax.set_xticks([0, 250, 500, 750, 1000])
labels = ax.set_xticklabels(['one','two','three','four','five'],rotation=30, fontsize='small')
ax.set_title('My first matplotlib plot')
ax.set_xlabel('Stages')
# 범례 추가 하기
fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
ax.plot(random(1000).cumsum(), 'k', label= 'one')
ax.plot(random(1000).cumsum(), 'k--', label= 'two')
ax.plot(random(1000).cumsum(), 'k.', label= 'three')
ax.legend(loc='bext')

## 8.1.4 주석과 그림 추가
# ax.text(x,y,'Hello world!',family='monospace', fontsize=10)
import cx_Oracle
con= cx_Oracle.connect('11834/11834@192.168.1.139:1521/FIMS2005')
cur= con.cursor()
a = ['STOCK_001040','STOCK_029780','STOCK_035720','STOCK_251270']
b=[]
for i in range(len(a)):    
    b.append(pd.read_sql("SELECT * FROM {}".format(a[i]),con,index_col=None))
    print(cur.execute("SELECT COMMENTS FROM DBA_TAB_COMMENTS WHERE TABLE_NAME='{}'".format(a[i])).fetchall())
cur.close()
con.close()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
close = b[2]['CLOSE']
close.plot(ax=ax, style='k-')
ax.set_title('Kakao')

b[2][['DATE','CLOSE']].plot(x='DATE', y='CLOSE',color='g',title='Kakao',alpha=0.8)

c=pd.concat([b[0]['CLOSE'],b[1]['CLOSE'],b[2]['CLOSE'],b[3]['CLOSE']],axis=1)
c.columns=['CJ','SAMSUNG_CARD','KAKAO','NETMABLE']
c.index=b[0]['DATE']
c.plot(subplots=True, layout=(2,2),title='Stock Price')   
c.plot(title='Stock Price')

# 산포도



