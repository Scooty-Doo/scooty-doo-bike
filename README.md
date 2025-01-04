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

You can set up the bike with the following environment variables: 
```
BIKE_ID
TOKEN
BACKEND_URL
LONGITUDE
LATITUDE
```

To make things easy, there is an [.env.example](.env.example) for you to use. Just rename it to copy it to a new .env and you're good to go.

## Start the bike

To start the bike run:

```bash
# From project root
python -m src.main
```

## Run tests

To run the tests use:
```bash
python -m pytest
```
