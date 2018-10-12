# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import datetime

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
               AND A.STK_CD = '007070'\
               AND A.STK_CD = B.STK_CD"
gs       = pd.read_sql(sql_query, con_fims2005, index_col=None)
TRD_DT   = [datetime.datetime.strptime(gs.TRD_DT[i], "%Y%m%d") for i in range(len(gs))]
gs.index = TRD_DT
cur_fims2005.close()
con_fims2005.close()

gs.CLOSE_PRC.plot(figsize= (8, 5))


#### 6.2 금융자료
## 일간 종가에 기반한 로그수익률
# 1. pct_change 함수
gs['Return'] = gs.CLOSE_PRC.pct_change()

# 2. 빈 칼럼 생성후 for문으로 로그 수익률 하나씩 계산
#gs['Ret_Loop'] = ''
#for i in range(1, len(gs)):
#    gs['Ret_Loop'][i] = np.log(gs['CLOSE_PRC'][i] / gs['CLOSE_PRC'][i-1])
#gs[['CLOSE_PRC','Ret_Loop']]    

# 3. 백터화를 사용하여 반복문 없이 계산
#gs['Return'] = np.log(gs['CLOSE_PRC'] / gs['CLOSE_PRC'].shift(1))


## gs리테일 주가와 일간 로드 수익률
# 변동성 군집현상: 변동성은 시간에 따라 일정하게 유지되지 않는다.(변동성이 높게 유지되는 구간 or 변동성이 낮게 유지되는 구간)
# 레버리지 효과: 일반적으로 변동성과 주식 시장 수익률은 음의 상관관계
gs[['CLOSE_PRC','Return']].plot(subplots=True, style='b', figsize=(8, 5))

# 주식 트레이더(기술적 분석에 의지{추세선: 이동평균선})
gs['42d'] = gs['CLOSE_PRC'].rolling(window=42).mean() # (영업일 기준날짜의 주가 ~ 42일 전 주가)의 평균
gs['252d'] = gs['CLOSE_PRC'].rolling(window=252).mean()
gs[['CLOSE_PRC','42d','252d']].plot(figsize=(8, 5))

# 옵션 트레이더(로그 수익률의 이동 표준편차{이동 역사적 변동성})
# 교재의 DAX 지수는 레버리지 효과 가설(이동 변동성과 시장 주가는 음의 상관관계)을 뒷바침하나 주식 개별 종목에 관해서는??
import math
gs['Moving_Vol'] = gs['Return'].rolling(window=252).std()*math.sqrt(252)
gs[['CLOSE_PRC','Moving_Vol','Return']].plot(subplots=True, style='b', figsize=(8, 7))


#### 6.3 회귀분석
## pandas를 이용해 정식적인 통계적인 근거에 기반한 분석가능(최소 제곱법애 기반한 선형회귀분석)
## 레버리지 효과: S&P 500 and VIX지수(S&P500지수 옵션 가격의 향후 30일 동안의 변동성에 대한 시장의 기대를 나타내는 지수)의 상관관계로 검증
con_fims2005 = cx_Oracle.connect('fimsr/vudrk_read@192.168.1.130:1521/FIMS2005')
cur_fims2005 = con_fims2005.cursor()
sql_query1 = "SELECT GIJUN_YMD \
                   , BM_CD \
                   , BM_ENM \
                   , CUR \
                   , BM_JISU \
                   , BF_DEBI_RT \
                   , VOLUME \
                FROM TST502S1 \
                WHERE BM_ENM = 'CBOE S&P 500 Volatility Index' \
                ORDER BY GIJUN_YMD ASC"
sql_query2 = "SELECT GIJUN_YMD \
                   , BM_CD \
                   , BM_ENM \
                   , CUR \
                   , BM_JISU \
                   , BF_DEBI_RT \
                   , VOLUME \
                FROM TST502S1 \
                WHERE BM_ENM = 'S&P 500' \
                AND GIJUN_YMD >= '20060301' \
                ORDER BY GIJUN_YMD ASC"

vix         = pd.read_sql(sql_query1, con_fims2005, index_col=None)
sp500       = pd.read_sql(sql_query2, con_fims2005, index_col=None)
GIJUN_YMD   = [datetime.datetime.strptime(vix.GIJUN_YMD[i], "%Y%m%d") for i in range(len(vix))]
GIJUN_YMD2  = [datetime.datetime.strptime(sp500.GIJUN_YMD[i], "%Y%m%d") for i in range(len(sp500))]
vix.index   = GIJUN_YMD
sp500.index = GIJUN_YMD2
data        = pd.DataFrame({'SP500': sp500["BM_JISU"], 'VIX': vix["BM_JISU"]})
cur_fims2005.close()
con_fims2005.close()

# plot(시각적으로 확인)
data.plot(subplots=True, grid=True, style='b', figsize=(8, 6))

# 로그 수익률
data_return = data.pct_change()
data_return.plot(subplots=True, grid=True, style='b', figsize=(8, 6))

# 독립변수: S&P500수익률 & 종속변수: VIX수익률
# statsmodel package 설치 필요
import statsmodels.formula.api as sm
model = sm.OLS.from_formula("VIX ~ SP500", data=data_return).fit()
model.summary()
model.params

# 레버리지 효과 시각화
import matplotlib.pyplot as plt
plt.plot(data_return.SP500, data_return.VIX, 'r.')
ax = plt.axis()
x  = np.linspace(ax[0], ax[1] + 0.01)
plt.plot(x, model.params[0] + model.params[1]*x, 'b', lw=2)
plt.grid(True)
plt.axis('tight')
plt.xlabel('SP500 returns')
plt.ylabel('VIX returns')

# 두 시계열 값에서 상관계수
data_return.corr()

# 상관계수를 연 단위(252 매매일 기준)으로 계산
data_return['SP500'].rolling(window=252).corr(data_return['VIX']).plot(grid=True, style='b')

