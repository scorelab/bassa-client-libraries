#! /bin/bash

function start_bassa
{
    docker-compose up & > /dev/null
}

function stop_bassa
{
    docker-compose down
}
function run_tests
{
    cd ./python_lib
    pip install -r requirements.txt
    python -m unittest test_bassa.py
}

start_bassa
sleep 20
run_tests
sleep 10
stop_bassa