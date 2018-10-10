# -*- coding: utf-8 -*-


#### 7.4 문자열 다루기
val = 'a,b, guido'
val.split(',')

# strip(공백문자 제거)
pieces = [x.strip() for x in val.split(',')]
'+'.join(pieces)

# 부분 문자열 위치
'guido' in val
val.index('a')
val.find(':')   #문자열 없는 경우 -1값 봔환

# 문자열 치환
val.replace(',','')

## 정규표현식(문자열 패턴 찾기)
import re  # 패턴 매칭, 치환, 분리 
text = "foo    bar\t baz \tqux"
re.split('\s+',text)  # '\s+' 하나이상의 공백문자 의미

# 직접 정규표현식 compile
regex = re.compile('\s+')
regex.split(text)
regex.findall(text) # 모든 패턴의 목록

## e-mail 주소를 검사하는 정규표현식
text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com
Cyj cyj9201@naver.com
"""
# Matches any character from a-z or 0-9, Matches exactly one character from a-z but length must be 2~4
# pattern = 사용자+메일주소
pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
regex = re.compile(pattern, flags=re.IGNORECASE)
regex.findall(text)
m=regex.search(text)
print(regex.sub('패턴발견',text)) # 찾은 패턴을 주어진 문자열로 치환


