## TODO:

* Index, IndexPrice (Dollar, Kospi, Nasdaq, WTI, ...) 구현
* [X] Entity
* [X] Service
* [X] Commands


* create_chart 수정
* [X] Index 추가


* RADEME.md 파일 수정
* [X] commands 자세히
* [X] usage 자세히

### Coverage

```shell
1. pip install coverage
2. .coveragerc 작성

coverage run --source='.' -m unittest discover tests/ test_*.py

# 통계
coverage report
# Html 로
coverage html
# 이전 기록 삭제
coverage erase
```

#### Create Coverage Badge

```shell
pip install coverage-badge
coverage-badge -o coverage.svg
```

Not everyone should be allowed to vote!

### 참고

```shell
# SqlAlchemy
https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying

https://hackersandslackers.com/sqlalchemy-data-models

https://dongwooklee96.github.io/post/2021/03/18/sqlalchemy%EC%97%90%EC%84%9C-%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98-%EC%82%AC%EC%9A%A9%EB%B2%95.html

# Finance data reader
https://github.com/FinanceData/FinanceDataReader
```