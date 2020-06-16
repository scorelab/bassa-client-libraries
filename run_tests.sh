#! /bin/sh

docker-compose up &
cd python-lib
pip install -r requirements.txt
python -m unittest test_bassa.py