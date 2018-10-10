# -*- coding: utf-8 -*-



#### 9.1 Group By 메카닉
## key1 으로 grouping 하고 data1의 평균구하기
import pandas as pd
import numpy as np
df= pd.DataFrame({'key1':['a','a','b','b','c'], 'key2': ['one','two','one','two','one'], 
                  'data1': np.random.random(5), 'data2': np.random.random(5)})
df
# groupby 객체(통계 메서드 추가)
grouped = df['data1'].groupby(df['key1'])
grouped.mean()     # series 객체 생성

## key1,key2으로 grouping 하고 data1의 평균구하기
means = df['data1'].groupby([df['key1'],df['key2']]).mean()
means.unstack() # dataframe 객체 변환
states = np.array(['Ohio','California','California','Ohio','Ohio'])
years = np.array([2005, 2005, 2006, 2005, 2006])
df['data1'].groupby([states, years]).mean()     # 객체 길이만 일치하면 상관없음

# 통계함수 적용시 숫자 데이터가 아닌 Column은 자동으로 제외
df.groupby('key1').mean()
df.groupby(['key1','key2']).mean()
df.groupby(['key1','key2']).size()


### 9.1.1 그룹간 순회하기
for name, group in df.groupby('key1'):
    print(name)
    print(group)

for (k1, k2), group in df.groupby(['key1','key2']):
    print((k1,k2))
    print(group)

# 그룹별 데이터 사전형으로 변환
pieces = dict(list(df.groupby('key1')))    
pieces['b']

# 데이터 type별로 그룹핑
df.dtypes
grouped = df.groupby(df.dtypes, axis=1)
dict(list(grouped))

### 9.1.2 칼럼 또는 칼럼의 일부만 선택하기
df.groupby(['key1','key2'])[['data2']].mean()
s_grouped = df.groupby(['key1','key2'])['data2']
s_grouped.mean()

### 9.1.3 사전과 Series에서 그룹핑
people = pd.DataFrame(np.random.rand(5,5), columns=['a','b','c','d','e'], index=['Joe','Steve','Wes','Jim','Travis'])
people.ix[2:3, ['b','c']] = np.nan
people
# sum
mapping = {'a':'red', 'b':'red', 'c':'blue', 'd':'blue', 'e':'red', 'f':'orange'} # dict 객체
by_column = people.groupby(mapping, axis=1)
by_column.sum()

map_series = pd.Series(mapping) # series 객체
people.groupby(map_series, axis=1).count()

### 9.1.4 함수로 묶기
people.groupby(len).sum() # index 길이로 그룹핑
key_list = ['one','one','one','two','two']
people.groupby([len, key_list]).min()

### 9.1.5 색인 단계로 묶기
columns = pd.MultiIndex.from_arrays([['US','US','US','JP','JP'],[1,3,5,1,3]],names=['cty','tenor'])
hier_df = pd.DataFrame(np.random.rand(4,5), columns=columns)
hier_df.groupby(level='cty',axis=1).count()
hier_df.groupby(level='cty',axis=1).sum()



#### 9.2 데이터 수집
df
grouped = df.groupby('key1')
grouped['data1'].quantile(0.9) # Return values at the given quantile over requested axis, a la numpy.percentile.

# 기초통계량
def peak_to_peak(arr):
    return arr.max() - arr.min()

grouped.agg(peak_to_peak)
grouped.describe().T

# 통계값 칼럼 추가
tips = pd.read_csv("C:/Users/CYJ/Desktop/Test/py_sample/ch08/tips.csv")
tips['tip_pct']= tips['tip'] / tips['total_bill']
tips

### 9.2.1 칼럼에 여러 가지 함수 적용하기
grouped = tips.groupby(['sex','smoker'])
grouped_pct = grouped['tip_pct']

grouped_pct.agg('mean')
grouped_pct.agg(['mean', 'std', peak_to_peak]) # 칼럼명: 함수이름
grouped_pct.agg([('foo', 'mean'),('bar', np.std)])
functions = ['count', 'mean', 'max']
result = grouped['tip_pct', 'total_bill'].agg(functions)
result
result['tip_pct']

ftuples = [('Durchschnitt', 'mean'), ('Abweichung', np.var)]
grouped['tip_pct','total_bill'].agg(ftuples) 



### 9.3 그룹별 연산과 변형
# 비교
df
k1_means = df.groupby('key1').mean().add_prefix('mean_')
k1_means
pd.merge(df, k1_means, left_on='key1', right_index=True)

key = ['one', 'two', 'one', 'two', 'one']
people.groupby(key).mean()
people.groupby(key).transform(np.mean)

def demean(arr):
    return arr - arr.mean()
demeaned = people.groupby(key).transform(demean)
demeaned
demeaned.groupby(key).mean()

## 9.3.1 apply: 분리-적용-병합
def top(df, n=5, column='tip_pct'):
    return df.sort_values(by=column)[-n:]

top(tips, n=6)
tips.groupby('smoker').apply(top)
tips.groupby(['smoker','day']).apply(top, n=1, column='total_bill')
result = tips.groupby('smoker')['tip_pct'].describe()
result.stack()
result.T

tips.groupby('smoker', group_keys=False).apply(top)

## 9.3.2 변위치 분석과 버킷 분석
frame = pd.DataFrame({'data1': np.random.randn(1000),
                      'data2': np.random.randn(1000)})
factor = pd.cut(frame.data1, 4) # cut: 데이터 인터벌 그룹 4개 생성
def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}
grouped = frame.data2.groupby(factor)
grouped.apply(get_stats).unstack()



