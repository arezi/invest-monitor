

cd $(dirname "$0")

#unset INVEST_MONITOR_DB # test with demo.db

export FLASK_ENV=development

if [ ! $INVEST_MONITOR_DB ] && [ ! -f demo.db ]; then
    echo "Creating demo.db"
    python3 migrate.py 
fi

python3 invest-monitor-web.py
# or
#FLASK_APP=run.py flask run
