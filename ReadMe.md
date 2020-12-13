# Python GRPC Chat App

![Build Status](https://github.com/Ryan95Z/python-grpc-chat-app/workflows/build/badge.svg)

A Python gRPC chat application using Tkinter.

## Requirements

The following are required to develop or execute the project:

* Python 3
* PIP (Python package manager)

## Setting up the environment

To set up the environment, ensure the virtualenv package has been installed. This can be added to your Python instance with:

```bash
pip install virtualenv
```

Once virtualenv has been installed. Use the `Makefile` to  install the relevant dependencies for the application:

```bash
make init
```

This will do the following:

* Create the Python virtual environment
* Activate the virtual environment
* Install the relevant packages

## Running the server

To start the gRPC server:

```bash
python server.py
```

## Running the chat client

To start the chat application:

```bash
python main.py
```

**Note**: You can create multiple instances of the client to simulate multiple users

## Unit Tests

To run all the unit tests in the project, use:

```
python -m unittest
```

## Coding Standards

This project follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python coding standard. In order to validate the code against PEP 8, run the pycodestyle tool. This can be executed with:

```bash
make lint
```