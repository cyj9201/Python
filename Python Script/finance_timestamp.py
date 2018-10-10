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
gs = pd.read_sql(sql_query, con_fims2005, index_col=None)
TRD_DT = [datetime.datetime.strptime(gs.TRD_DT[i], "%Y%m%d") for i in range(len(gs))]
gs.index = TRD_DT
cur_fims2005.close()
con_fims2005.close()

gs.CLOSE_PRC.plot(figsize= (8, 5))

# 일간 종가에 기반한 로그수익률
# 1. pct_change 함수
%%time
gs.CLOSE_PRC.pct_change()

# 2. 빈 칼럼 생성후 for문으로 로그 수익률 하나씩 계산
%%time
gs['Ret_Loop'] = ''
for i in range(1, len(gs)):
    gs['Ret_Loop'][i] = np.log(gs['CLOSE_PRC'][i] / gs['CLOSE_PRC'][i-1])
gs[['CLOSE_PRC','Ret_Loop']]    

# 3. 백터화를 사용하여 반복문 없이 계산
%%time
gs['Return'] = np.log(gs['CLOSE_PRC'] / gs['CLOSE_PRC'].shift(1))

