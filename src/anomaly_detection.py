import pandas as pd


def detect_numeric_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect numeric outliers using the IQR method.
    """

    numeric_columns = [
        "Age at enrollment",
        "Curricular units 1st sem (credited)",
        "Curricular units 1st sem (enrolled)",
        "Curricular units 1st sem (evaluations)",
        "Curricular units 1st sem (approved)",
        "Curricular units 1st sem (grade)",
        "Curricular units 1st sem (without evaluations)",
        "Curricular units 2nd sem (credited)",
        "Curricular units 2nd sem (enrolled)",
        "Curricular units 2nd sem (evaluations)",
        "Curricular units 2nd sem (approved)",
        "Curricular units 2nd sem (grade)",
        "Curricular units 2nd sem (without evaluations)",
        "Unemployment rate",
        "Inflation rate",
        "GDP"
    ]

    numeric_df = df[numeric_columns].copy()

    columns = [
        "row_index",
        "column",
        "value",
        "lower_bound",
        "upper_bound",
        "anomaly_type",
        "anomaly_score"
    ]

    if numeric_df.empty:
        return pd.DataFrame(columns=columns)

    numeric_anomalies = []

    for col in numeric_df.columns:

        q1 = numeric_df[col].quantile(0.25)
        q3 = numeric_df[col].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_mask = (
            (numeric_df[col] < lower_bound) |
            (numeric_df[col] > upper_bound)
        )

        outliers = numeric_df[col][outlier_mask]



        for index, value in outliers.items():

            if value < lower_bound:
                anomaly_type = "low"
                anomaly_score = lower_bound - value
            else:
                anomaly_type = "high"
                anomaly_score = value - upper_bound


            numeric_anomalies.append({
                "row_index": index,
                "column": col,
                "value": value,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "anomaly_type": anomaly_type,
                "anomaly_score": anomaly_score
            })

    return pd.DataFrame(numeric_anomalies, columns=columns)