import pandas as pd
import sys
import typing
import uuid

# A dictionary of string indexed functions which can be applied to the generated
# CSVs value columns.
TRANSFORMERS: typing.Dict[str, typing.Callable[[str], str]] = {
    # transform "last, first" into "first last"
    'flip_names' : (lambda s : ' '.join(s.split(', ')[::-1])),
}

# Read the source CSV file.
def read_source(source_path: str) -> pd.DataFrame:
    return pd.read_csv(source_path, dtype=str)

# Read the specified columns from the map CSV file.
def read_map(map_path: str, map_columns: [str]) -> pd.DataFrame:
    return pd.read_csv(map_path, usecols=map_columns, dtype=str)

# Read the source and map CSV files into Pandas DataFrames, and add the
# specified map value columns to the source CSV.
def generate(source_path: str, map_path: str, column_sets: [typing.Dict[str, str]]) -> pd.DataFrame:
    # Read the source CSV file.
    target_csv = read_source(source_path)

    # Collect all of the necessary columns which will need to be extracted from
    # the map CSV file.
    map_columns = []; [[map_columns.extend(column_pair) for column_pair in columns['map_columns'].items()] for columns in column_sets]
    # Read the necessary columns from the map CSV file.
    map_csv = read_map(map_path, map_columns)

    # Extend the source CSV file with the new value columns.
    for column_set in column_sets:
        # Update the source CSV file's index to match the shared ID column.
        target_csv = target_csv.set_index(column_set['source_id_column'], drop=False)
        # Extract the target value column for this column set into a variable
        # for easier reference.
        target_value_column = column_set['target_value_column']
        # Initialize the new value column being migrated on the target CSV file.
        target_csv[target_value_column] = pd.Series(dtype='float64')
        # Generate a random temporary column ID for map column migration.
        temp_column = uuid.uuid4()
        # Extend the source CSV file with the given map value column.
        for map_id_column, map_value_column in column_set['map_columns'].items():
            # Extract the map CSV file's ID and value column pair, and update
            # the map CSV file's index to match the shared ID column.
            map_pair = map_csv[[map_id_column, map_value_column]].set_index(map_id_column)
            # Rename the map value column to the temporary column ID.
            map_pair.rename(columns={map_value_column: temp_column}, inplace=True)
            # Merge the map value column into the target CSV using the current
            # ID column.
            target_csv = target_csv.join(map_pair)
            # Fill any missing values in the target value column using the map
            # value column.
            target_csv[target_value_column] = target_csv[target_value_column].mask(pd.isnull, target_csv[temp_column])
            # Remove the temporary ID column.
            target_csv.pop(temp_column)
        # Apply the specified transformations for this column set to it's target
        # value column.
        if column_set.get('transformers'):
            target_csv[target_value_column] = transform(target_csv[target_value_column], column_set.get('transformers'))

    return target_csv

# Apply the supplied list of transformers to the given dataframe and return the
# result.
def transform(target: pd.DataFrame, applicable_transformers: [str]) -> pd.DataFrame:
    for t in applicable_transformers:
        if t in TRANSFORMERS:
            target = target.apply(TRANSFORMERS[t])
        else:
            sys.stderr.write('error: transformer "%s" does not exist\n' % t)
            sys.exit(2)
    return target

# Write the supplied Pandas DataFrame to a CSV file using the given file path
# and ID column name.
def write(target: pd.DataFrame, file_path: str) -> None:
    target.to_csv(file_path, index=False)
