install-dep:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	echo "Installed Dependencies"

start-bassa:
	cd ../
	docker-compose up &
	sleep 100
	echo "Started Bassa"

stop-bassa:
	cd ../
	docker-compose down
	echo "Stopped Bassa"

test:
	python -m unittest test_bassa.py -vv
	echo "Test Completed"

lint:
	pip install pylint
	pylint -E bassa/ || printf "pylint has found some errors!"
	echo "Done"

clean-pyc:
	find . -name "*.pyc" -exec rm -f {} \;
	echo "Clean Done"

build:
	pip install setuptools wheel twine
	python setup.py sdist bdist_wheel
	echo "Build Complete"

test-push:
	twine check dist/*
	twine upload --repository testpypi dist/*
	echo "pushed"

push:
	twine check dist/*
	twine upload dist/*	
	echo "pushed"

test-publish: build test-push
	echo "published"

publish: build push
	echo "published"
