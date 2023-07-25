# cogram-whisper

## Usage

### Running locally

Build and start the project with `docker-compose`:

```sh
docker-compose up
```

### Making test requests

When you run `docker-compose`, the server container will be available at `http://localhost:8000/`. You can make requests to this address.

If you want to test local mp3 files, you need to make them available via web requests. There is a pre-made script that exposes your file using the `dummy` server and makes a request to the running server.
You can invoke the script specifying the path to the input mp3 file:

```sh
./scripts/test_request.sh /path/to/file.mp3
```

## Development

### Requirements

This project requires Python version 3.11 and [`poetry`](https://python-poetry.org/) for dependency management. Make sure you have those installed

The project currently runs on linux machines only because of the [openai whisper](https://github.com/openai/whisper) dependency. If you have MacOS or Windows, consider using virtual machines for development.

### Set up

#### Install project dependencies

```sh
poetry install
```

#### Install pre-commit hooks

```sh
pre-commit install
```

### Running tests

Run all tests

```sh
pytest
```

Start continuous test runner

```sh
ptw .
```
