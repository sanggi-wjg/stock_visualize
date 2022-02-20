# Stock Visualize

### 구조
```shell
app / commands : Executable soruce code
    / service : Model service
    / database : SqlAlchemy and entities
    / exceptions : exceptions

tests / ... : Test source code
```

### Lint
1. pip install flake8
2. .flake8 작성
```shell
# 실행
flake8 .
```

### Coverage
1. pip install coverage
2. .coveragerc 작성
```shell
coverage run --source='.' -m unittest discover tests/ test_*.py

# 통계
coverage report
# Html 로
coverage html
# 이전 기록 삭제
coverage erase
```

### 참고
```shell
# SqlAlchemy
https://hackersandslackers.com/sqlalchemy-data-models

https://dongwooklee96.github.io/post/2021/03/18/sqlalchemy%EC%97%90%EC%84%9C-%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98-%EC%82%AC%EC%9A%A9%EB%B2%95.html

# Finance data reader
https://github.com/FinanceData/FinanceDataReader
```