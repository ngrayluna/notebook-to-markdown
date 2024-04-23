#!/bin/bash

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

# Run Jupyter nbconvert to convert the notebook to Markdown
output_md="${filename%.ipynb}.md"  

python post_process_notebook.py "$output_md"

# Run the Python script with the Markdown filename
python rename_notebook.py "$output_md"