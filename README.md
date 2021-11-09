# CSV Column Generator

A Python executable for generating new columns on a CSV file using a map CSV with shared key columns.

## Dependencies

Python 3 (version 3.6 or greater) is required to run this project.

## Installation

You can install the script using:

```sh
python3 setup.py install
```

And run it using:
```sh
csv-join -h
```

## Usage

The CSV Column Generator executable can be run in two ways.

You can either use it to generate a single column by passing it the necessary details as arguments: 
```sh
csv-join single -sp source.csv -mp map.csv -sic id -mic map_id -mvc map_name -tp target.csv -tvc name
```
Or multiple columns by passing it a config file (see the `example-config.json` for an example of how the config file must be formatted):
```sh
csv-join multiple ./config.json
```

## Help!

The main command and each sub-command have help menus which can be accessed using the `-h` option:
```sh
csv-join -h
csv-join single -h
csv-join multiple -h
```
