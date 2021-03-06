#!/usr/bin/env python3

import argparse
import csvjoin as cj
import json

def main() -> None:
    args = parse_args()
    # Initialize an empty commands list for storing commands describing how the
    # map value column can be joined and transformed onto the target CSV.
    commands = []
    # If the `single` subcommand was called, construct a single column
    # transformation command using the supplied arguments.
    if args.subcommand == 'single':
        commands = [{
            'source_path': args.source_path,
            'map_path': args.map_path,
            'target_path': args.target_path or args.source_path,
            'column_sets': [{
                'source_id_column': args.source_id_column,
                'map_columns': {args.map_id_column: args.map_value_column},
                'target_value_column': args.target_value_column,
                'transformers': args.transformers,
            }],
        }]
    # Otherwise, if the `multiple` subcommand was called, read the
    # transformation commands described in the supplied config file.
    elif args.subcommand == 'multiple':
        with open(args.config_path, 'r') as config_file:
            commands = json.loads(config_file.read())
    # Execute the generated commands.
    for command in commands:
        print('Processing file "%s"...' % command['source_path'], end=' ', flush=True)
        # Read the source CSV file.
        source_csv = read_source(command['source_path'])
        # Collect all of the necessary columns which will need to be extracted from
        # the map CSV file.
        map_columns = []; [[map_columns.extend(column_pair) for column_pair in columns['map_columns'].items()] for columns in command['column_sets']]
        # Read the necessary columns from the map CSV file.
        map_csv = read_map(map_path, map_columns)
        # Perform the merge and write the output.
        target = cj.generate(source_csv, map_csv, command['column_sets'])
        write(target, command['target_path'] or command['source_path'])
        print('Done!')

# Read the source CSV file.
def read_source(source_path: str) -> pd.DataFrame:
    return pd.read_csv(source_path, dtype=str, keep_default_na=False)

# Read the specified columns from the map CSV file.
def read_map(map_path: str, map_columns: [str]) -> pd.DataFrame:
    return pd.read_csv(map_path, usecols=map_columns, dtype=str, keep_default_na=False)

# Write the supplied Pandas DataFrame to a CSV file using the given file path
# and ID column name.
def write(target: pd.DataFrame, file_path: str) -> None:
    target.to_csv(file_path, index=False)

# Construct argument parser.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='This script generates columns in a CSV file based on a shared ID with another CSV file.')
    subparsers = parser.add_subparsers(dest='subcommand')
    single_parser = subparsers.add_parser('single', help='Generate a single column based on the supplied arguments.')
    single_parser.add_argument('-sp', '--source_path', required=True, help='path to the CSV file which the new column is being created on')
    single_parser.add_argument('-mp', '--map_path', required=True, help='path to the reference CSV file used for determining what values to place in the new column based on the shared column')
    single_parser.add_argument('-sic', '--source_id_column', required=True, help='the name of the ID column on the `source_path` file shared with the `map_path` file')
    single_parser.add_argument('-mic', '--map_id_column', required=True, help='the name of the ID column on the `map_path` file shared with the `source_path` file')
    single_parser.add_argument('-mvc', '--map_value_column', required=True, help='the name of the value column being copied from the `map_path` file')
    single_parser.add_argument('-tvc', '--target_value_column', required=True, help='the new column name on the `target_path` file; if no column is supplied, `source_column` is used')
    single_parser.add_argument('-tp', '--target_path', help='path to the new CSV file generated by this command; if no path is supplied, `source_path` is overwritten')
    single_parser.add_argument('-tfs', '--transformers', nargs='+', help='a list of space-separated transformations to apply to the target value column; available transformations: ' + (', '.join(cj.TRANSFORMERS.keys())))
    multiple_parser = subparsers.add_parser('multiple', help='Generate multiple columns based on the supplied configuration file.')
    multiple_parser.add_argument('config_path', help='path to the JSON config file used to configure the behavior of this command')
    return parser.parse_args()

# If this script is being called directly, parse the supplied arguments and run
# the main function.
if __name__ == '__main__':
    main()
