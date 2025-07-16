import pandas as pd
import os
import random
import json


'''
This script is used to convert the parquet file to a jsonl file.
The output file is saved to the data folder as test.jsonl.
The input file is the full-00000-of-00001.parquet file.
'''
def from_parquet_to_jsonl(file_name: str):
    """
    Reads a parquet file and saves its content to a JSONL file.
    
    Args:
        file_name (str): Name of the parquet file to convert
    """
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test.jsonl')
    
    df = pd.read_parquet(data_file)
    # Convert dataframe to JSONL format and save
    with open(output_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            # Convert row to dictionary and write as JSON line
            json_line = row.to_dict()
            f.write(json.dumps(json_line) + '\n')
    
    print(f"Successfully converted {file_name} to test.jsonl")
    print(f"Output saved to: {output_path}")
    print(f"Total rows converted: {len(df)}")


if __name__ == "__main__":
    from_parquet_to_jsonl('full-00000-of-00001.parquet') 