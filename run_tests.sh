#! /bin/sh

docker-compose up &
wait
ls
ls -a
cd python-lib
pip install -r requirements.txt
python -m unittest test_bassa.py