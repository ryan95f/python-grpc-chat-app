# Python gRPC Chat App

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

Once virtualenv has been installed. Create the virutal environment for the application:

```bash
python -m venv env
```

Then activate the virtual environment:

```bash
source env/bin/activate
```

Finally use the `Makefile` to  install the relevant dependencies for the application:

```bash
make init
```

## Running the server

To start the chat server:

```bash
make server
```

## Running the chat client

To start the chat client application:

```bash
make client
```

**Note**: You can create multiple instances of the client to simulate multiple users

## Compiling the Protocol Buffers

To compile the protocol buffers found in the `protos/` directory, run:

```bash
make protoc
```

This will output two Python files called `chat_pb2.py` and `chat_pb2_grpc.py`. These files will be located in the `src/server/` package.

## Unit Tests

To run all the unit tests in the project, use:

```bash
make tests
```

## Coding Standards

This project follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python coding standard. In order to validate the code against PEP 8, run the `pycodestyle` tool. This can be executed with:

```bash
make lint
```
