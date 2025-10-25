# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

#!/usr/bin/env python3
import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print(f"Error: File '{filepath}' is empty.")
        return pd.DataFrame()



def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.
    """
    if remove_duplicates:
        df = df.drop_duplicates()
    df = df.replace(sentinel_value, np.nan)
    # Normalize 'site' column values to a consistent format if present
    if 'site' in df.columns:
        # Replace underscores with spaces, collapse multiple spaces, strip, and title-case
        df['site'] = (
            df['site']
            .astype(str)
            .str.replace('_', ' ', regex=False)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
            .str.title()
        )

    # Normalize 'intervention_group' values (collapse spaces, strip, title-case, fix common typos)
    if 'intervention_group' in df.columns:
        ig = (
            df['intervention_group']
            .astype(str)
            .str.replace('_', ' ', regex=False)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
        )

        # Lowercase form for mapping
        ig_lower = ig.str.lower()

        # Mapping of common misspellings/variants to canonical names (lowercase keys)
        mapping = {
            'contrl': 'Control',
            'conrtl': 'Control',
            'conrol': 'Control',
            'control': 'Control',
            'treatment a': 'Treatment A',
            'treatment b': 'Treatment B',
            'treatmen a': 'Treatment A',
            'treatmen b': 'Treatment B',
            'treatmenta': 'Treatment A',
            'treatmentb': 'Treatment B'
        }

        df['intervention_group'] = ig_lower.map(lambda x: mapping.get(x, x.title()))

    # Normalize 'enrollment_date' to datetime dtype
    if 'enrollment_date' in df.columns:
        # Coerce empty strings and obvious placeholders to NaN, strip whitespace
        ed = (
            df['enrollment_date']
            .astype(str)
            .str.strip()
            .replace({'': None, 'NA': None, 'N/A': None, 'nan': None})
        )

        # First pass: let pandas try to parse common formats
        parsed = pd.to_datetime(ed, errors='coerce')

        # If some values remain unparsed, try common explicit formats on the remaining
        if parsed.isna().any():
            remaining = ed[parsed.isna()]
            # Try common US style with slashes and dashes
            for fmt in ('%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y'):
                try_parsed = pd.to_datetime(remaining, format=fmt, errors='coerce')
                # update parsed Series with any newly parsed values (aligns by index)
                parsed.update(try_parsed)
                remaining = ed[parsed.isna()]
                if remaining.empty:
                    break

            # As a last resort try with dayfirst=True for ambiguous cases
            if parsed.isna().any():
                try_parsed = pd.to_datetime(remaining, errors='coerce', dayfirst=True)
                parsed.update(try_parsed)

        # Keep the parsed datetime in a helper column for analysis
        df['enrollment_date_dt'] = parsed

        # Set the main enrollment_date column to ISO-formatted strings YYYY-MM-DD (or None)
        df['enrollment_date'] = (
            df['enrollment_date_dt']
            .dt.strftime('%Y-%m-%d')
        )
        # Replace NaT/NaN formatted strings with None
        df.loc[df['enrollment_date_dt'].isna(), 'enrollment_date'] = None

    # Normalize 'sex' column (map common short codes and variants to canonical values)
    if 'sex' in df.columns:
        s = df['sex'].astype(str).str.strip()
        s_lower = s.str.lower()
        sex_map = {
            'f': 'Female',
            'female': 'Female',
            'woman': 'Female',
            'F': 'Female',
            'm': 'Male',
            'male': 'Male',
            'man': 'Male',
            'M':'Male',
                   }
        df['sex'] = s_lower.map(sex_map).fillna(s_lower).str.title()

    return df


def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.
    """
    return df.isnull().sum()


def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.
    """
    if column not in df.columns:
        print(f"Warning: Column '{column}' not found in DataFrame.")
        return df

    if strategy == 'mean':
        fill_value = df[column].mean()
        df[column] = df[column].fillna(fill_value)
    elif strategy == 'median':
        fill_value = df[column].median()
        df[column] = df[column].fillna(fill_value)
    elif strategy == 'ffill':
        df[column] = df[column].ffill()
    else:
        print(f"Warning: Strategy '{strategy}' must be 'mean', 'median', or 'ffill'.")
        return df

    return df
    

def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.
    """
    filter_df = df.copy()

    for f in filters:
        col = f.get('column')
        cond = f.get('condition')
        val = f.get('value')

        if col not in filter_df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame.")
            continue

        if cond == 'equals':
            filter_df = filter_df[filter_df[col] == val]
        elif cond == 'not_equals':
            filter_df = filter_df[filter_df[col] != val]
        elif cond == 'greater_than':
            filter_df = filter_df[filter_df[col] > val]
        elif cond == 'less_than':
            filter_df = filter_df[filter_df[col] < val]
        elif cond == 'in_range' and isinstance(val, list) and len(val) == 2:
            filter_df = filter_df[(filter_df[col] >= val[0]) & (filter_df[col] <= val[1])]
        elif cond == 'in_list' and isinstance(val, list):
            filter_df = filter_df[filter_df[col].isin(val)]
        else:
            print(f"Warning: Unsupported condition '{cond}' or invalid value for column '{col}'.")
    return filter_df

    """Examples:
        >>> # Single filter
        >>> filters = [{'column': 'site', 'condition': 'equals', 'value': 'Site A'}]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Multiple filters applied in order
        >>> filters = [
        ...     {'column': 'age', 'condition': 'greater_than', 'value': 18},
        ...     {'column': 'age', 'condition': 'less_than', 'value': 65},
        ...     {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
        ... ]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Range filter example
        >>> filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 65]}]
        >>> df_filtered = filter_data(df, filters)
    """


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.
    """
    for col, target_type in type_map.items():
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame.")
            continue

        try:
            if target_type == 'datetime':
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif target_type == 'numeric':
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif target_type == 'category':
                df[col] = df[col].astype('category')
            elif target_type == 'string':
                df[col] = df[col].astype(str)
            else:
                print(f"Warning: Unsupported target type '{target_type}' for column '{col}'.")
        except Exception as e:
            print(f"Error converting column '{col}' to type '{target_type}': {e}")
    return df
    
    """
    Example:
        >>> type_map = {
        ...     'enrollment_date': 'datetime',
        ...     'age': 'numeric',
        ...     'site': 'category'
        ... }
        >>> df_typed = transform_types(df, type_map)
    """


def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().
    """
    if column not in df.columns:
        print(f"Warning: Column '{column}' not found in DataFrame.")
        
    if new_column is None:
        new_column = f"{column}_binned"
    df[new_column] = pd.cut(df[column], bins=bins, labels=labels, include_lowest=True)
    return df
    """
    Example:
        >>> df_binned = create_bins(
        ...     df,
        ...     column='age',
        ...     bins=[0, 18, 35, 50, 65, 100],
        ...     labels=['<18', '18-34', '35-49', '50-64', '65+']
        ... )
    """


def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.
    """
    if group_col not in df.columns:
        print(f"Warning: Group column '{group_col}' not found in DataFrame.")
        return pd.DataFrame()

    if agg_dict is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        agg_dict = {col: ['mean', 'std'] for col in numeric_cols}

    grouped_df = df.groupby(group_col).agg(agg_dict)
    return grouped_df
"""
    Examples:
        >>> # Simple summary
        >>> summary = summarize_by_group(df, 'site')
        >>>
        >>> # Custom aggregations
        >>> summary = summarize_by_group(
        ...     df,
        ...     'site',
        ...     {'age': ['mean', 'std'], 'bmi': 'mean'}
        ... )
    """



#OPTIONAL TEST IF MODULE IS RUN DIRECTLY
if __name__ == '__main__':
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")
    
    # Simple test cases can be added here to validate functionality
    test_df = pd.DataFrame({'age': [25, 30, 35], 'bmi': [22, 25, 28]})
    print("Test DataFrame created:", test_df.shape)
    cleaned_df = clean_data(test_df)
    print("Test_ Cleaned_DataFrame:", cleaned_df)
    print("Test detect_missing:", detect_missing(test_df))