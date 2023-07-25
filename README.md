# cogram-whisper

## Usage

### Running locally

Build and start the project with `docker-compose`:

```sh
docker-compose up
```

### Making test requests

```sh
./scripts/test_request.sh /path/to/file.mp3
```

## Development

### Requirements

This project requires Python version 3.11 and [`poetry`](https://python-poetry.org/) for dependency management. Make sure you have those installed

The project currently runs on linux machines only because of the [openai whisper](https://github.com/openai/whisper) dependency. If you have MacOS or Windows, considering using virtual machines for development.

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
