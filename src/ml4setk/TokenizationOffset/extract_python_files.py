import pandas as pd
import os
import re

# Read parquet file
df = pd.read_parquet('datasets/python.parquet')

# Create output directory
output_dir = 'extracted_python_files'
os.makedirs(output_dir, exist_ok=True)

# Process each row of data
for index, row in df.iterrows():
    task_id = row['task_id']
    prompt = row['prompt']
    solution = row['canonical_solution']
    test = row['test']
    entry_point = row['entry_point']
    
    # Create filename (using task_id as filename)
    safe_filename = re.sub(r'[^\w\-_.]', '_', task_id) + '.py'
    file_path = os.path.join(output_dir, safe_filename)
    
    # Combine content
    content = f"""# Task ID: {task_id}
# Entry Function: {entry_point}

# Problem Description:
\"\"\"
{prompt}
\"\"\"

# Solution:
{solution}

# Tests:
{test}

# If run as a standalone script, execute tests
if __name__ == "__main__":
    import unittest
    unittest.main()
"""
    
    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"File created: {file_path}")

print(f"Total of {len(df)} Python files created in '{output_dir}' directory")