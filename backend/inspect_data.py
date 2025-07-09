# import os
# import pandas as pd
# import fastparquet

# # Define the path to the dataset file
# dataset_path = os.path.join(os.getcwd(), 'dataset', 'ember', 'test_ember_2018_v2_features.parquet')

# # Load the dataset using pandas (requires pyarrow or fastparquet installed)
# try:
#     df = pd.read_parquet(dataset_path, engine='fastparquet')
# except Exception as e:
#     print("Error loading dataset:", e)
#     exit(1)

# # Print basic info about the dataset
# print("Dataset loaded!")
# print("Shape:", df.shape)
# print("Columns:", df.columns.tolist())
# print("First few rows:")
# print(df.head())

