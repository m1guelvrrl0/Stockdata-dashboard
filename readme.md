# STOCKDATA WITH DASH FLASK

This project was mostly a learning exercise with Dash and playing with async code. It was heavily inspired by [this](https://www.freelancer.com/projects/python/website-for-Financial-Stock-Market/).

## Features

* Dash frontend based on [this repo](https://github.com/Pierian-Data/Plotly-Dashboards-with-Dash).
* Database agnostic with SQLalchemy, simply change the DB URI in settings.
* Async Data Fetching

## Requirements
* python 3.7+
* Pipenv

## How to run 
Clone this repo and then
```bash
cd thisrepo/
pipenv install
pipenv shell
python get_symbols.py
python initdb.py
```
