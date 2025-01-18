[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-bike/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-bike/?branch=main)
[![Code Coverage](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-bike/badges/coverage.png?b=main)](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-bike/?branch=main)
[![Build Status](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-bike/badges/build.png?b=main)](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-bike/build-status/main)
# scooty-doo-bike
Program controlling e-scooters for the Scooty Doo bike renting application

## Setup

### Virtual environment
```bash
# Create virtual environment (from project root)
python3 -m venv .venv

# Activate virtual environment (from project root)
source .venv/bin/activate   # Linux/MacOS

# Install dependencies (from project root)
pip install -r requirements.txt
```

### .env file

You can set up the bike .env file with the environment variables found in .env.example.

There is an [.env.example](.env.example) for you to use. Just rename it to copy it to a new .env and you're good to go.

## Start the bike

To start the bike run:

```python
# From project root
python -m src.main
```

NOTE: Currently, in order to run src/main.py using "python -m src.main" you need to setup the backend first, 
since the application will crash once reports fail to be sent to the backend.
It is recommended to start the application in the scooty-doo master repository where the backend and bike is set up in the same network.

## Run tests

To run the tests use:
```python
python -m pytest
```

# Generate documentation

```python
python -m pydoc -p 8000
```

Go to http://localhost:8000/ to inspect the documentation.