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

# Read the source and map CSV files into Pandas DataFrames, and add the
# specified map value columns to the source CSV.
def generate(source_csv: pd.DataFrame, map_csv: pd.DataFrame, column_sets: [typing.Dict]) -> pd.DataFrame:
    # Extend the source CSV file with the new value columns.
    for column_set in column_sets:
        # Extract the target value column for this column set into a variable
        # for easier reference.
        target_value_column = column_set['target_value_column']
        # Initialize the new value column being migrated on the target CSV file
        # if it doesn't already exist.
        if target_value_column not in source_csv.columns:
            source_csv[target_value_column] = pd.Series(dtype=str)
        # Generate a random temporary column ID for map column migration.
        temp_column = uuid.uuid4()
        # Extend the source CSV file with the given map value column.
        for map_id_column, map_value_column in column_set['map_columns'].items():
            # Ensure ID columns are iterable.
            if type(map_id_column) == str:
                map_id_column = [map_id_column]
            source_id_column = column_set['source_id_column']
            if type(column_set['source_id_column']) == str:
                source_id_column = [column_set['source_id_column']]

            # Extract the map CSV file's ID and value column pair, and update
            # the map CSV file's index to match the shared ID column.
            map_pair = map_csv[[*map_id_column, map_value_column]].copy()
            # Rename the map value column to the temporary column ID.
            map_pair.rename(columns={map_value_column: temp_column}, inplace=True)
            # Extract a list of all source CSV columns.
            source_cols = source_csv.columns
            # Merge the map value column into the target CSV using the current
            # ID column.
            source_csv = source_csv.merge(map_pair, how='left', left_on=source_id_column, right_on=map_id_column, suffixes=(False, False))
            # Fill any missing values in the target value column using the map
            # value column.
            source_csv[target_value_column] = source_csv[target_value_column].mask(pd.isnull, source_csv[temp_column])
            # Remove the temporary ID column and any map ID columns added during
            # the merge.
            source_csv.drop([temp_column, *{*map_id_column} - {*source_cols}], axis=1, inplace=True)
        # Apply the specified transformations for this column set to it's target
        # value column.
        if column_set.get('transformers'):
            source_csv[target_value_column] = transform(source_csv[target_value_column], column_set.get('transformers'))

    return source_csv

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
