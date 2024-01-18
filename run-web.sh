#!/usr/bin/env sh


cd $(dirname "$0")

if [ ! -e .venv ]; then
  echo "Error: need venv! Run:  python3 -m venv .venv   &&   .venv/bin/pip install -r requirements.txt"
  exit 1
fi

. .venv/bin/activate 

#unset INVEST_MONITOR_DB # test with demo.db

export FLASK_ENV=development

if [ ! $INVEST_MONITOR_DB ] && [ ! -f demo.db ]; then
    echo "Creating demo.db"
    python3 migrate.py 
fi

python3 invest-monitor-web.py
# or
#FLASK_APP=run.py flask run
