#!/bin/bash

# Usage: 
# >> bash convert_nb2md.sh Organizing_Hyperparameter_Sweeps_in_PyTorch_with_W\&B.ipynb

# Check if a filename is provided as argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Get the filename from the first argument
filename="$1"

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "Error: File '$filename' not found."
    exit 1
fi

# Run the Python script with the provided filename
jupyter nbconvert --to markdown "$filename"

# Check if conversion was successful
if [ $? -ne 0 ]; then
    echo "Error: Conversion to Markdown failed."
    exit 1
fi

# Get the markdown file name created from the previous step
output_md="${filename%.ipynb}.md"  

# Post process markdown
python post_process_notebook.py "$output_md"

# Check if markdown file needs to be renamed 
python rename_notebook.py "$output_md"