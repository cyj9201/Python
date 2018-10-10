# -*- coding: utf-8 -*-


#### R(ggplot2, trellis 패키지와 유사)
#### 아이티 지진 데이터 시각화하기
# data 불러오기
import numpy as np
import pandas as pd
data = pd.read_csv('C:/Users/CYJ/Desktop/Test/ch08/Haiti.csv')
data.info()

# data 타임스탬프, 위치정보 포함
data[['INCIDENT DATE','LATITUDE','LONGITUDE']]
# massage 종류
data['CATEGORY']

# data 요약후 위도, 경도 튀는값 제거(아이티 위도 경도 벗어난 값)
data.describe()
data= data[(data.LATITUDE > 18) & (data.LATITUDE < 20)
        &(data.LONGITUDE > -75) & (data.LONGITUDE < -70) & data.CATEGORY.notnull()].reset_index(drop=True)

# Category 별 분석 and 시각화(사용자 정희 함수 생성{코드와 영어이름으로 분리})
def to_cat_list(catstr):
    stripped = (x.strip() for x in catstr.split(','))   # strip: 공백제거
    return [x for x in stripped if x]

def get_all_categories(cat_series):
    cat_sets = (set(to_cat_list(x)) for x in cat_series) # set: 중복제거
    return sorted(set.union(*cat_sets))

def get_english(cat):
    code, names = cat.split('.')
    if '|' in names:
        names = names.split(' | ')[1]
    return code, names.strip()

to_cat_list(data['CATEGORY'][0]) #구분자(,)
get_all_categories(data['CATEGORY']) # 카테고리 중복값 제거
get_english(to_cat_list(data['CATEGORY'][0])[0]) #구분자(.)

# code와 code name mapping
all_cats = get_all_categories(data.CATEGORY)
# generator 표현
english_mapping = dict(get_english(x) for x in all_cats) 
english_mapping['2']
english_mapping['6c']

# 식별용(혹은 dummy) column을 각 Category에 하나씩 추가
def get_code(seq):
    return [x.split('.')[0] for x in seq if x]

all_codes = get_code(all_cats)
code_index = pd.Index(np.unique(all_codes))
dummy_frame = pd.DataFrame(np.zeros((len(data),len(code_index))),index=data.index, columns=code_index)
dummy_frame.info()

# data와 dummy_frame join
for row, cat in zip(data.index, data.CATEGORY):
    codes = get_code(to_cat_list(cat))
    dummy_frame.ix[row. codes] = 1

data= data.join(dummy_frame.add_prefix('category_')) # add_prefix: 테이터프레임 outer 조인

# 도표 생성(흑백 아이티 지도 그리는 사용자 정의함수)
# https://www.lfd.uci.edu/~gohlke/pythonlibs/에서 basemap 패키지 다운로드(Python version 및 bit 체크)
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
def basic_haiti_map(ax=None, lllat=17.25, urlat=20.25, lllon=-75, urlon=-71):
    # create polar stereographic Basemap instance(위치 정보 반환)
    m = Basemap(ax=ax, projection='stere',lon_0=(urlon + lllon)/2, 
                lat_0=(urlat + lllat)/2,
                llcrnrlat=lllat, urcrnrlat=urlat,
                llrenlon=lllon, urcrnlon=urlon, resolution='i')
    # draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    return m

fig, axes = plt.subplots(norws=2, ncols=2, figsize=(12,10))
fig.subplots(hspace=0.05, wspace=0.05)
to_plot = ['2a', '1', '3c', '7a']
lllat=17.25; urlat=20.25; lllon=-75; urlon=-71

for code,ax in zip(to_plot, axes.flat):
    m= basic_haiti_map(ax, lllat=lllat, urlat=urlat, lllon=lllon, urlon=urlon)

    cat_data = data[data['category_%s' %code]==1]
    # compute map proj coordinates.
    x,y = m(cat_data.LONGITUDE, cat_data.LATITUDE.values)
    
    m.plot(x, y, 'k.', alpha=0.5)
    ax.set_title('%s: %s' %(code,english_mapping[code]))
plt.show()

# http://cegrp.cga.harvard.edu/haiti/?q=resources_data(추가적인 지도 데이터 덮어쓰기)
shapefile_path = 'ch08/PortAuprince_Roads/PortAuPrince_Roads'
m.readshapefile(shapefile_path, 'roads')
    
