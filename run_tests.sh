#! /bin/sh

docker-compose up &
wait
cd $TRAVIS_BUILD_DIR/python_lib
pip install -r requirements.txt
python -m unittest test_bassa.py