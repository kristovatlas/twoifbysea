init:
	pip install -r requirements.txt

test:
	python -m unittest discover -p "test_*.py"

start:
	python twoifbysea/webserver.py

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.db' -delete
	python ./twoifbysea/clean_user_db.py #deletes user database!

.PHONY: init test start clean
