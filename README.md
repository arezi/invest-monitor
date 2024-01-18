# InvestMonitor

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


## Overview
A monitor for your investments.
This project uses python 3, and some libraries like `flask` and `requests`

![screen demo](docs/screenshot_demo.png?raw=true "Screenshot demo")

## Quickstart (run demo)
```bash
pip3 install -r requirements.txt

./run-web.sh
```
Open http://localhost:4000


## setup my database
```bash
export INVEST_MONITOR_DB=/home/my_user/invest/invest.db

python3 migrate.py

./run-web.sh
```
Open http://localhost:4000

## running tests
```bash
./tests.sh
```


## TODO
. use uvicorn in server
