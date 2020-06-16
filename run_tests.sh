#! /bin/sh

sudo chmod -R a+rwx $TRAVIS_BUILD_DIR
docker-compose up &
wait
cd $TRAVIS_BUILD_DIR/python-lib
pip install -r requirements.txt
python -m unittest test_bassa.py