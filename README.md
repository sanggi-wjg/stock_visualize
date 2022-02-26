# Stock Visualize
Not everyone should be allowed to vote

## Development Environment
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![MySQL 8.0](https://img.shields.io/badge/MySQL-8.0-blue.svg)]()

```shell
SQLAlchemy, finance-datareader

requriements.txt
```

## Usage
```shell
1. command / register_markets  
    DB에 Market 등록 (Kospi, Kosdaq, ...)

2. command / register_stocks  
    DB에 Stock 등록 (삼성전자, NAVER ...)   

3. command / register_stock_prices
    DB에 StockPrice 등록
    
4. command / craete_stock_chart
```


## Structure
```shell
app / commands / ...  : Executable service code
    / lib      / ...  : Library service code 
    / service  / ...  : Model service
    / database        : SqlAlchemy and Entities
    / exceptions      : Exceptions
    / utils           : Util code
    / vo              : Value Objects
    / constants       : Constants

docker / ... : Dockerfile or docker-compose file 

tests / ... : Test source code
(command line 으로 전체 다 테스트 해보고 싶다면
database engine 이 사용중인 db 말고 다른 db로 선택한 후에 
python -m unittest discover)
```


### Lint
```shell
1. pip install flake8
2. .flake8 작성

# 실행
flake8 .
```


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


