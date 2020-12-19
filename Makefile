PYTHON := python

all: lint tests

.PHONY: init 
init:
	pip install -r requirements.txt

.PHONY: lint
lint:
	pycodestyle

.PHONY: tests
tests:
	coverage run -m unittest
	coverage html
	coverage report

.PHONY: protoc
protoc:
	${PYTHON} -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/src/server/*.proto

.PHONY: server
server:
	${PYTHON} server.py

.PHONY: client
client:
	${PYTHON} main.py

.PHONY: clean
clean:
	rm -r htmlcov
	rm .coverage
