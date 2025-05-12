import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Strip whitespace & unify text columns
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip().str.lower()

    # Coerce types: example for numeric
    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                continue

    # Handle missing values: fill numeric with median
    for col in df.select_dtypes(include="number"):
        df.fillna({col: df[col].median()}, inplace=True)
    # Fill object columns with 'unknown'
    for col in df.select_dtypes(include="object"):
        df.fillna({col: "unkown"}, inplace=True)

    # TODO: dedup, advanced logic (schema validation, external lookups)
    df.drop_duplicates(inplace=True)
    return df
