import pandas as pd


def detect_categorical_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect unexpected values in categorical columns.
    """

    categorical_columns = [
        "Marital status",
        "Application mode",
        "Course",
        "Daytime/evening attendance",
        "Previous qualification",
        "Nationality",
        "Mothers qualification",
        "Fathers qualification",
        "Mothers occupation",
        "Fathers occupation",
        "Displaced",
        "Educational special needs",
        "Debtor",
        "Tuition fees up to date",
        "Gender",
        "Scholarship holder",
        "International",
        "Target"
    ]
    EXPECTED_CATEGORIES = {
        "Gender": ["Male", "Female"],
        "Target": ["Dropout", "Graduate", "Enrolled"],
        "Debtor": ["Yes", "No"],
        "Scholarship holder": ["Yes", "No"],
        "Displaced": ["Yes", "No"],
        "Educational special needs": ["Yes", "No"],
        "Tuition fees up to date": ["Yes", "No"],
        "International": ["Yes", "No"],
    }

    anomalies = []

    for column, expected_values in EXPECTED_CATEGORIES.items():

        invalid_mask = ~df[column].isin(expected_values)

        invalid_values = df.loc[invalid_mask, column]

        for index, value in invalid_values.items():
            anomalies.append({
                "row_index": index,
                "column": column,
                "value": value,
                "anomaly_type": "unexpected_category"
            })

    return pd.DataFrame(anomalies)

def detect_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect completely duplicated rows.
    """

    duplicate_mask = df.duplicated(keep=False)

    duplicates = df.loc[duplicate_mask].copy()

    result = pd.DataFrame({
        "row_index": duplicates.index,
        "anomaly_type": "duplicate_row"
    })

    return result

def detect_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect missing values in the DataFrame.
    """

    anomalies = []

    for column in df.columns:

        missing_rows = df[df[column].isna()].index

        for index in missing_rows:
            anomalies.append({
                "row_index": index,
                "column": column,
                "value": None,
                "anomaly_type": "missing_value"
            })

    return pd.DataFrame(anomalies)