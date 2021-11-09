# CSV Column Generator

A Python executable for generating new columns on a CSV file using a map CSV with shared key columns.

## Dependencies

Python 3 (version 3.6 or greater) is required to run this project.

## Installation

You can either install the scripts required dependencies globally:

```sh
python3 -m pip install -r requirements.txt
```
And run it using:
```sh
python3 ./generate-columns.py -h
```

Or you can use Pipenv for dependency management:

```sh
python3 -m pip install --user pipenv
pipenv install
```
And run it using:
```sh
pipenv run ./generate-columns.py -h
```

## Usage

The CSV Column Generator executable can be run in two ways.

You can either use it to generate a single column by passing it the necessary details as arguments: 
```sh
python3 ./generate-columns.py single -sp source.csv -mp map.csv -sic id -mic map_id -mvc map_name -tp target.csv -tvc name
```
Or multiple columns by passing it a config file (see the `example-config.json` for an example of how the config file must be formatted):
```sh
python3 ./generate-columns.py multiple ./config.json
```

## Help!

The main command and each sub-command have help menus which can be accessed using the `-h` option:
```sh
python3 ./generate-columns.py -h
python3 ./generate-columns.py single -h
python3 ./generate-columns.py multiple -h
```
