import pandas as pd
import json
import os
import numpy as np

def convert_to_serializable(obj):
    """Convert numpy arrays and other non-serializable objects to serializable format"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    else:
        return obj

def convert_parquet_to_jsonl(parquet_file, output_file):
    """
    Read the content of the completion_file column in the parquet file,
    and convert it to a jsonl file in the HumanEval.jsonl format
    """
    
    # Read the parquet file
    print(f"reading {parquet_file}...")
    df = pd.read_parquet(parquet_file)
    
    print(f"The dataset contains {len(df)} rows of data")
    print(f"Column names: {list(df.columns)}")
    
    # Check if the completion_file column exists
    if 'completion_file' not in df.columns:
        print("Error: 'completion_file' column not found")
        print(f"Available columns: {list(df.columns)}")
        return
    
    # Check the structure of the first few samples
    print("\nCheck the structure of the first few completion_file samples:")
    for i in range(min(3, len(df))):
        completion_file = df.iloc[i]['completion_file']
        print(f"The type of the completion_file in the {i}th row: {type(completion_file)}")
        if isinstance(completion_file, dict):
            print(f"  Keys: {list(completion_file.keys())}")
        elif hasattr(completion_file, 'keys'):
            print(f"  Keys: {list(completion_file.keys())}")
        else:
            print(f"  Content: {str(completion_file)[:200]}...")
    
    # Prepare the output data
    output_data = []
    
    for idx, row in df.iterrows():
        completion_file = row['completion_file']
        
        # Try different ways to get the content
        content = None
        
        if isinstance(completion_file, dict):
            if 'content' in completion_file:
                content = completion_file['content']
            else:
                # If there is no content field, try other possible fields
                for key in ['text', 'code', 'body', 'data']:
                    if key in completion_file:
                        content = completion_file[key]
                        break
        elif hasattr(completion_file, 'get'):
            content = completion_file.get('content')
        elif isinstance(completion_file, str):
            content = completion_file
        
        if content is not None:
            # Build data in the HumanEval.jsonl format
            jsonl_entry = {
                "task_id": f"lca_task_{idx}",
                "prompt": "",  # Can add prompt if needed
                "canonical_solution": str(content),  # Convert content to a string
                "test": "",  # Can add test if needed
                "entry_point": "",  # Can add entry point if needed
            }
            
            # Add other fields, ensure they are serializable
            for col in df.columns:
                if col != 'completion_file':
                    value = row[col]
                    jsonl_entry[col] = convert_to_serializable(value)
            
            output_data.append(jsonl_entry)
        else:
            print(f"Warning: The {idx}th row cannot extract content")
    
    # Write to the jsonl file
    print(f"\nwriting to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in output_data:
            # Ensure all data are serializable
            serializable_entry = convert_to_serializable(entry)
            f.write(json.dumps(serializable_entry, ensure_ascii=False) + '\n')
    
    print(f"Conversion completed! Processed {len(output_data)} records")
    print(f"Output file: {output_file}")

def main():
    # Input and output file paths
    parquet_file = "lca_small_context.parquet"
    output_file = "lca_small_context.jsonl"
    
    # Check if the input file exists
    if not os.path.exists(parquet_file):
        print(f"Error: File {parquet_file} not found")
        return
    
    # Execute the conversion
    convert_parquet_to_jsonl(parquet_file, output_file)

if __name__ == "__main__":
    main()