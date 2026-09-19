import pandas as pd

def profile_data(df):

    print("==== DATA PROFILE ====")


    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values")
    print(df.isnull().sum())

    print('\nUnique Values:')
    print(df.nunique())

if __name__ == "__main__":
    file_path = "D:/Project/AI_Excel_Analytics_Agent/data/student_cleaned.csv"

    df = pd.read_csv(file_path)

    profile_data(df)